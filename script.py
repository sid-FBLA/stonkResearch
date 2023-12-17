#installing OpenAi
import openai
#This module allows us to interact with and access other files in the directory
import os 
#Provides access to some python libraries we will use 
import sys
#Scraping .json files
import requests
#Pandas dataframe                                                                   
import pandas as pd
#some helpful functions
import functions
#Our API Key
import constants
#getting SEC filings
#import secFilings
from company import Company
import getFilings


"""Work for tomorrow:
- Make sure the 10k filing is complete (seems to start on page 7 for AAPL)
- Ensure you have the right company description
- Connect the filing to langchain API and start making GPT Queries 
- User types in stock ticker then you output description--work with company tickers filing (index command--reframe data)"""

#Importing LangChain Functions
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator  
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI 
import pickle
import numpy as np #for vector storage in this case—not math


os.environ["OPENAI_API_KEY"] = constants.APIKEY
print(constants.APIKEY)

# Specify the model name
model_name = "gpt-3.5-turbo"  # Replace with your desired model

# Create an instance of ChatOpenAI with the specified model
chat_model = ChatOpenAI(model_name=model_name)

#sys.argv[1] takes the user input in the command line and stores it in the query variable
print("Submit Ticker:")
query = functions.user_input()
print(query)


#Creating an instance of company class
Company1 = Company(query.strip())
Company1.get10k()
#print(Company1.cik)
#print(Company1.get10k())

#Okay so look into creating a vector embedding by breaking paragraphs then saving them to an OpenAI database 

# Read the contents of the file
with open('test.txt', 'r', encoding='utf-8') as file:
    testTxt = file.read()
from openai import OpenAI

client = OpenAI()
"""
#Converting txt file to vector embeddings
import re
from gensim.utils import simple_preprocess

def read_text_in_chunks(file_path, chunk_size=10000):
    with open(file_path, 'r', encoding='utf-8') as file:
        chunk = []
        for line in file:
            # Simple preprocessing for each line
            processed_line = simple_preprocess(line)
            chunk.extend(processed_line)
            if len(chunk) >= chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk

file_path = "AAPL 10-K"

from gensim.models import Word2Vec

# Initialize the model
model = Word2Vec(vector_size=100, window=5, min_count=5, workers=4)

# Build vocabulary and train the model
for chunk in read_text_in_chunks(file_path):
    model.build_vocab([chunk], update=True)
    model.train([chunk], total_examples=model.corpus_count, epochs=model.epochs)

# Save the entire model
model.save("word2vec_large.model")

# Save only the word vectors
word_vectors = model.wv
word_vectors.save("wordvectors_large.kv")



test_df = pd.read_csv['test.txt']
print(test_df)


Facebook for cosine similarity 
response = client.embeddings.create(
  model="text-embedding-ada-002",
  input= "Hello my name is Sid",
  encoding_format="float"
)

embeddings = response.data[0].embedding
print(response.usage)

# Convert embeddings to a numpy array if they are not already
embeddings_array = np.array(embeddings)
#reshaping embeddings array
embeddings_array = embeddings_array.reshape(1, -1)


# Save the numpy array to a file
np.save('embeddings.npy', embeddings_array)

print(embeddings_array)
#Using facebook's AI
import faiss

# Assuming 'embeddings' is a NumPy array of your embeddings
dimension = embeddings_array.shape[1]  # Number of dimensions for each vector
index = faiss.IndexFlatL2(dimension)  # Create a flat (brute-force) index
# Add vectors to the index
index.add(embeddings_array)

print(index)

#Q&A
print(index.query(query))
"""
