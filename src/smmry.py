import requests
import json
import os
import re

FOOTER = "I'm a new bot and I am still learning, [read more about me here,](https://wiki.ourcanadian.ca/en/admin/buycanadianwikibot) or report issues to /r/BuyCanadian modmail."

def hello():
    print("Hello World")

def loadJSON(fileName):
    with open(fileName, 'r') as json_file:
        data = json.load(json_file)
    if(data):
        return data[0]
    return None

def fetchSmmry(SM_URL):
    SM_API_KEY = os.environ['SM_API_KEY']
    url = "https://api.smmry.com/&SM_API_KEY="+SM_API_KEY+"&SM_URL="+SM_URL
    response = requests.post(url=url).json()

    if('sm_api_error' in response.keys()):
        return False, response['sm_api_error']
    else:
        return response, None

def handleSuccessfulSummary(summary, url):
    header = "This is the best tl;dr I could do for "+summary['sm_api_title']+", [original]("+url+") reduced by "+summary['sm_api_content_reduced']+". (I'm a bot)"
    content = ">"+summary['sm_api_content']

    return header+"  \n"+content+"  \n"+FOOTER

def handleShortAboutPage(url, text):
    header = "Too short for a tl;dr, so here is the full text from [original]("+url+"). (I'm a bot)"
    lines = [line.strip() for line in text if not re.match('^\s*$', line) and len(line.split()) > 3]
    content = ' '.join(lines)

    return header+"  \n"+content+"  \n"+FOOTER

def handleError(errorcode, url, text):
    errorMsg = [
        "Sorry, I depend on the SMMRY API and it seems there has been an internal server error on their side. Maybe /u/GlaucomysSabrinus can look into this.", # Internal server problem which isn't your fault
        "Sorry, I'm having troubles with that url. Maybe /u/GlaucomysSabrinus can help.", # Incorrect submission variables
        "Sorry, I'm only allowed to do this 100 times a day, seems like I'm too popular today! Maybe /u/GlaucomysSabrinus should upgrade our API token." # Intentional restriction (low credits/disabled API key/banned API key)
    ]

    if(errorcode == 3):
        # Summarization error
        return handleShortAboutPage(url, text)

    elif(errorcode < 3): print(erroMsg[errorcode]+"  \n"+FOOTER) 
    else: return "I ran into an unknown error. /u/GlaucomysSabrinus please help..."

def create():
    TMP_JSON_FILE = './buycan-tldr-TMP.json'

    if(os.stat(TMP_JSON_FILE).st_size == 0):
        return "Sorry, I'm having trouble finding an About page at this url. Maybe /u/GlaucomysSabrinus can help.  \n"+FOOTER

    data = loadJSON(TMP_JSON_FILE)

    url = data['url']
    text = data['text']
    
    summary, errorcode = fetchSmmry(url)
    if(summary): return handleSuccessfulSummary(summary, url)
    else: return handleError(errorcode, url, text)

def main():
    print("Hello World")

if __name__ == "__main__":
    main()
