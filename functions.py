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

def html_to_text(html):
    from bs4 import BeautifulSoup
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Find all text within the HTML document
    return soup.get_text()

def get_string_until(string, target_char):
    #index of target character
    index = string.find(target_char)
    # Slice the string up to that character
    if index != -1:  # Check if the character was found
        result = string[:index]
    else:
        result = string  # Or handle the case where the character is not found
    return result