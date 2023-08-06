import twint
import os

def scrape_tweets(class_name: str, query=None, username=None, limit=100):
    if " " in class_name:
        print("Class names can't contains spaces")
        return

    if query is None and username is None:
        print("You must specify a query and/or an username")
        return

    # Configure
    c = twint.Config()

    if username is not None:
        c.Username = username

    if query is not None:
        c.Search = query

    c.Limit = limit
    print("Limit: ", limit)
    c.Output = "tmp.txt"

    # Run
    twint.run.Search(c)

    os.makedirs("data", exist_ok=True)
    with open("tmp.txt", "r") as f:
        lines = f.readlines()

    with open(os.path.join("/content/data", class_name + ".txt"), "w") as f:
        for l in lines:
            idx = l.find(">")
            tweet = l[idx+2:-1]
            f.write(tweet+"\n")

    os.remove("tmp.txt")

def remove_class(name):
    os.system("rm content/"+name+".txt")

