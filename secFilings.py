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
#importing BeautifulSoup (for further html parsing)
from bs4 import BeautifulSoup


# create request header
headers = {'User-Agent': "sid20102004@gmail.com"}

# get all companies data (this is for CIK--ticker pairing)
companyTickers = requests.get(
    "https://www.sec.gov/files/company_tickers.json",
    headers=headers
    )

# format response to dictionary and get first key/value
firstEntry = companyTickers.json()['0']

# parse CIK // without leading zeros
directCik = companyTickers.json()['0']['cik_str']

# dictionary to dataframe --> orient --> rows = index | This is a pandas dataframe NOT an array
companyData = pd.DataFrame.from_dict(companyTickers.json(), orient='index')

# add leading zeros to CIK
companyData['cik_str'] = companyData['cik_str'].astype(str).str.zfill(10)

"""Review: At this point we have a pandas dataframe with all hte companies Tickers, Names, and CIKs. 
Now we are going to access the actual SEC filing data"""


#Building CIK--currently we are using APPL--later we will have a function parameter that takes the ticker
cik = companyData[0:1].cik_str[0]

# get company specific filing metadata
filingMetadata = requests.get(
    f'https://data.sec.gov/submissions/CIK{cik}.json',
    headers=headers
)

# dictionary to dataframe
allForms = pd.DataFrame.from_dict(filingMetadata.json()['filings']['recent'])
print(allForms.columns)

#Accessing the 10k
print(allForms['form'])
annualFilingIndex = allForms['form'].tolist().index('10-K')
#We need the string until the hashtag this is the string used in the access link
annualFilingAccession = functions.remove_hypens((allForms['accessionNumber'].tolist()[annualFilingIndex]))
#This is the last part of the string we will need
annualFilingPrimaryDocument = (allForms['primaryDocument'].tolist()[annualFilingIndex])
print(annualFilingIndex)
print(annualFilingAccession)
print(annualFilingPrimaryDocument)

#extracts the the html content embedded within the 10k
def extract_html(url, cssSelector): 
    #Getting selenium then downloading web driver add to requirements.txt
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager
    #We need these modules to wait for javascript content 
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException  # Import TimeoutException


    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    url = f'https://www.sec.gov/ix?doc=/Archives/edgar/data/{directCik}/{annualFilingAccession}/{annualFilingPrimaryDocument}'
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 30)  # Wait for up to 10 seconds
        # Wait for the JavaScript to load the content--> this xbrl form is our "ticket"
        driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to appear
        content = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, cssSelector)))
        print(content)
        # Retrieve and print the text content
        return content.get_attribute("innerHTML")

        # If you want the HTML content
        # print(element.get_attribute("innerHTML"))

    except TimeoutException:
        return "Element not found within the time frame"

    # Don't forget to close the driver
    driver.quit()

contentHTML = extract_html(f'https://www.sec.gov/ix?doc=/Archives/edgar/data/{directCik}/{annualFilingAccession}/{annualFilingPrimaryDocument}', 
             "#dynamic-xbrl-form")



company10k = functions.html_to_text(contentHTML)
#All the text gets written in a file called companyInfo.txt
fileName = "Company Ticker" + " 10k"
# Open the file. If it doesn't exist, it will be created.
with open(fileName, 'w', encoding="utf-8") as file:
    # Write some content to the file (optional)
    file.write(company10k)