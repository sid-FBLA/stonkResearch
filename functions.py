import sys

def user_input():
    #empty array to store each argument 
    args = []
    #initalizing our input variable
    input = ""
    for arg in sys.argv:
        #appends each text element to the args array
        args.append(arg)
    #convert to text
    for word in args[1:]:
        input += word + " "
    #now we get the entire string
    return input 

def remove_hypens(text):
    print(text)
    # Remove hyphens (replace with an empty string)
    result = text.replace('-', '')

    return result

#returns a string until a certain character
def get_string_until(string, target_char):
    #index of target character
    index = string.find(target_char)
    # Slice the string up to that character
    if index != -1:  # Check if the character was found
        result = string[:index]
    else:
        result = string  # Or handle the case where the character is not found
    return result

#Getting html from javascript loaded elements
def get_html_from_javascript(url, cssSelector):
    #Getting selenium then downloading web driver add to requirements.txt
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager
    #We need these modules to wait for javascript content 
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException  # Import TimeoutException

    #installing the latest webdriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 30)  # Wait for up to 10 seconds
        # Wait for the JavaScript to load the content--> this xbrl form is our "ticket"
        driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to appear
        content = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, cssSelector)))
        print(content)
        # Retrieve all HTML content within css Selector
        return content.get_attribute("innerHTML")

    except TimeoutException:
        return "Element not found within the time frame"

    # Don't forget to close the driver
    driver.quit()

#After retrieving html content this will extract all the text
def html_to_text(html):
    from bs4 import BeautifulSoup
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    formatted_text = soup.get_text(separator='\n')

    # Find all text within the HTML document
    return formatted_text
