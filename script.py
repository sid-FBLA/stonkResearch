#installing OpenAi
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

from langchain.chains.openai_functions.openapi import get_openapi_chain

#import Finnhub into langchain
#chain = get_openapi_chain("API_DOCUMENTATION_URL")
#response = chain("YOUR_QUERY")


os.environ["OPENAI_API_KEY"] = constants.APIKEY

#sys.argv[1] takes the user input in the command line and stores it in the query variable
print("Submit Ticker:")
query = functions.user_input()
print(query)




#Creating an instance of company class
Company1 = Company(query.strip())
print(f'Ticker: {Company1.ticker}')

print(Company1.cik)
print(Company1.get10k())
