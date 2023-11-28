import requests
# import xmltodict 
from bs4 import BeautifulSoup
import re
import json

# API info
from config import *

#To list config items
verification_url = verification_url
mulesoft_url = mulesoft_url

client_id = client_id
client_secret = client_secret

def generate_token():
    '''
    Generates the Bearer token needed for OpenAI API authentication. Returns the Bearer token as a string.
    '''
    try:
        url = f"{verification_url}"
        payload = f"client_id={client_id}&client_secret={client_secret}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.request("POST", url, headers=headers, data=payload)
        token = response.json()["access_token"]
        return "Bearer " + token

    except Exception as e:
        return {
            "status": "error",
            "data": e,
            "message": e.orig.args if hasattr(e, "orig") else f"{e}",
        }
    

def generate_completion(payload, mulesoft_url, bearer_token):
    '''
    Generates a completion from the MuleSoft endpoint on the Vox platform and returns the result. 
    Returns the completion as a string.
    
    Args:
        payload: (dict) payload for completion
        mulesoft_url: (str) url endpoint of the MuleSoft connection
        bearer_token: (str) authentication token generated
    '''
    url = mulesoft_url + '/completion'
    payload = json.dumps(payload) #needed to convert into string
    bearer_token = bearer_token 
    headers = {"Authorization": bearer_token, "Content-Type": "application/json"}
    
    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        result = response.json()["result"]
        token = response.json()["totalTokens"]
        return result
    else:
        print("Unable to call with status code {}".format(response.status_code))
    
    
#Generate the token, valid for 30 min    
token = generate_token()
assert isinstance(token,str), "Check if client_id and client_secret are passed incorrectly from the config.py file"

url = mulesoft_url + '/deployments'

bearer_token = token
headers = {"Authorization": bearer_token, "Content-Type": "application/json"}
response = requests.request("GET", url, headers=headers)


#Detailing models to be used during examples

text_davinci_003 = 'text-davinci-003'
gpt_35_turbo = 'gpt-35-turbo'

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

url_link = 'https://www.fiercepharma.com/pharma/gsks-jemperli-prolongs-life-endometrial-cancer-trial-will-fda-expansion-come-next'

result = requests.get(url_link, headers=headers).text
soup = BeautifulSoup(result, "html.parser")
text = soup.get_text()

for i in ["\n","\t","\r", "  "]:
    text = text.replace(i, "")



# Get the completion with input parameters
def metadata_prompt(text):

    # Build the prompt
    prompt = f"""Extract the article title, publisher, author, date of publication, if there is no relevant text reply with None:
    '''{text}'''
    """
    # prompt = f"""Extract the author, date of publication, publisher, article title, if there is no relevant text reply with None:
    # '''{text}'''
    # """
    payload = {
        "prompt": prompt,
        "engine": text_davinci_003,
        "max_tokens": "128",
        "temperature": 0.0
    }
    text_response = generate_completion(payload, mulesoft_url, bearer_token)
    return text_response

