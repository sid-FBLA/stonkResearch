import requests
import constants

def query_openai(prompt, engine="text-davinci-003", max_tokens=100):
    api_key = constants.APIKEY # Replace with your OpenAI API key
    headers = {
        "Authorization": f"Bearer {constants.APIKEY}"
    }
    data = {
        "engine": engine,
        "prompt": prompt,
        "max_tokens": max_tokens
    }
    response = requests.post("https://api.openai.com/v1/engines/davinci/completions", headers=headers, json=data)
    return response.json()

# Example usage
prompt = "Translate the following English text to French: 'Hello, how are you?'"
response = query_openai(prompt)
print(response)
