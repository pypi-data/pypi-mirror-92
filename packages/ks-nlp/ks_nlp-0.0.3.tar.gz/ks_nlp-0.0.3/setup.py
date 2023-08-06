import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ks_nlp", # Replace with your own username
    version="0.0.3",
    author="Armand du Parc Locmaria",
    author_email="adpl33@gmail.com",
    description="NLP Hackathon toolbox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Armandpl/ks_nlp",
    install_requires=[
        'tweepy',
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
