#Scraping .json files
import requests
#Pandas dataframe
import pandas as pd
#importing our helper functions
import functions
from company import Company

#create request header
headers = {'User-Agent': "sid20102004@gmail.com"}

#SEC data:

#returns filing metadata for company
def filing_metadata(cik):
    #getting the filing metadata for company 
    return requests.get(
    f'https://data.sec.gov/submissions/CIK{cik}.json',
    headers=headers
)

#Gets the CIK without the zeroes
def getDirectCIK(self): 
    # get all companies data (this is for CIK--ticker pairing)
    companyTickers = requests.get(
        "https://www.sec.gov/files/company_tickers.json",
        headers=headers
    )
    # dictionary to dataframe --> orient --> rows = index | This is a pandas dataframe NOT an array
    companyTickers = pd.DataFrame.from_dict(companyTickers.json(), orient='index')
    #write a function that loops thorugh the companyTicker dataframe until we get the relevant Ticker then return CIK
    #initalizing index variable --> Index where ticker is located
    index = -1
    for row in companyTickers.itertuples():
        #removing all whitespace and converting to uppercase 
        if row.ticker.strip().upper() == self.ticker.strip().upper():
            #Who knew the index is not stored as an integer--how stupid
            index = int(row.Index)
            print(index)
            break
    directCik = companyTickers.iloc[index].cik_str
    #CIK is saved as a number not a string
    return str(directCik)

#Adds necessary zeroes to directCIK
def getCIK(self): 
    #Note: We can use the .directCIK attribute here instead 
    return self.getDirectCIK().zfill(10)

#Writes all the text in the 10k to a txt file
def get10k(self):
    filingMetadata = filing_metadata(self.cik)
    # dictionary to dataframe
    allForms = pd.DataFrame.from_dict(filingMetadata.json()['filings']['recent'])

    #Accessing the 10k
    annualFilingIndex = allForms['form'].tolist().index('10-K')
    #We need the string until the hashtag this is the string used in the access link
    annualFilingAccession = functions.remove_hypens((allForms['accessionNumber'].tolist()[annualFilingIndex]))
    #This is the last part of the string we will need
    annualFilingPrimaryDocument = (allForms['primaryDocument'].tolist()[annualFilingIndex])
    url = f'https://www.sec.gov/ix?doc=/Archives/edgar/data/{self.directCIK}/{annualFilingAccession}/{annualFilingPrimaryDocument}'
    #getting all the HTML and its children from the selected element
    contentHTML = functions.get_html_from_javascript(url, '#dynamic-xbrl-form')
    #extracting all the text content form that section of the 10k
    company10ktext = functions.html_to_text(contentHTML)

    #All the text gets written in a file called companyInfo.txt
    fileName = self.ticker + " 10-K"
    # Open the file. If it doesn't exist, it will be created.
    with open(fileName, 'w', encoding="utf-8") as file:
        # Write some content to the file
        file.write(company10ktext)




#Adding methods to Company Class
Company.getDirectCIK = getDirectCIK
Company.getCIK = getCIK
Company.get10k = get10k
