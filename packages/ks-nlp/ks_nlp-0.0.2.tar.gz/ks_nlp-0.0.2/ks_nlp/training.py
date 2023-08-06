import random
import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
import os

from transformers import (
    AdamW,
    T5ForConditionalGeneration,
    T5Tokenizer,
    get_linear_schedule_with_warmup
)

def set_seed(seed):
  random.seed(seed)
  np.random.seed(seed)
  torch.manual_seed(seed)

set_seed(42)

class T5:
  def __init__(self):
    self.tokenizer = T5Tokenizer.from_pretrained('t5-base')
    self.t5_model = T5ForConditionalGeneration.from_pretrained('t5-base')

  def train(self, dataset, learning_rate=3e-4, epochs=10):
    # optimizer
    no_decay = ["bias", "LayerNorm.weight"]
    optimizer_grouped_parameters = [
        {
            "params": [p for n, p in self.t5_model.named_parameters() if not any(nd in n for nd in no_decay)],
            "weight_decay": 0.0,
        },
        {
            "params": [p for n, p in self.t5_model.named_parameters() if any(nd in n for nd in no_decay)],
            "weight_decay": 0.0,
        },
    ]
    optimizer = AdamW(optimizer_grouped_parameters, lr=learning_rate, eps=1e-8)

    self.t5_model.train()

    for epoch in range(epochs):
      print ("epoch ",epoch)
      for input,output in dataset.data:
        input_sent = "{task}: {input} </s>".format(task=dataset.task, input=input)
        ouput_sent = output+" </s>"

        tokenized_inp = self.tokenizer.encode_plus(input_sent,  max_length=96, pad_to_max_length=True,return_tensors="pt")
        tokenized_output = self.tokenizer.encode_plus(ouput_sent, max_length=96, pad_to_max_length=True,return_tensors="pt")


        input_ids  = tokenized_inp["input_ids"]
        attention_mask = tokenized_inp["attention_mask"]

        lm_labels= tokenized_output["input_ids"]
        decoder_attention_mask=  tokenized_output["attention_mask"]


        # the forward function automatically creates the correct decoder_input_ids
        output = self.t5_model(input_ids=input_ids, lm_labels=lm_labels,decoder_attention_mask=decoder_attention_mask,attention_mask=attention_mask)
        loss = output[0]
        print("Loss: ", loss.item())

        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

  def predict(self, text, task, num_seq=3):
    test_sent = '{task}: {text} </s>'.format(task=task, text=text)
    test_tokenized = self.tokenizer.encode_plus(test_sent, return_tensors="pt")

    test_input_ids  = test_tokenized["input_ids"]
    test_attention_mask = test_tokenized["attention_mask"]

    self.t5_model.eval()
    beam_outputs = self.t5_model.generate(
        input_ids=test_input_ids,attention_mask=test_attention_mask,
        max_length=64,
        early_stopping=True,
        num_beams=10,
        num_return_sequences=num_seq,
        no_repeat_ngram_size=0
    )

    res = []
    for beam_output in beam_outputs:
        sent = self.tokenizer.decode(beam_output, skip_special_tokens=True,clean_up_tokenization_spaces=True)
        res.append(sent)
    return res

class nlp_dataset:
  def __init__(self, task):
    self.task = task
    self.data = []

  def add(self, input, output):
    self.data.append((input, output))
  
  def show(self, limit=50):
    count = 0
    for pair in self.data:
      print(pair)
      count +=1 
      if count > limit:
        break
    
  def load_from_twitter(self):
    for fname in os.listdir("content/data"):
      class_name = fname.replace(".txt", "")
      with open(os.path.join("content/data/", fname), "r") as f:
        for line in f.readlines():
          self.add(line, class_name)
