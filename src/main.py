import os
import smmry
import praw
import re
from datetime import datetime, timedelta

'''
On VPS ~/.config/praw.ini used for Reddit config
On local, you should store it ./praw.ini
'''

TMP_TXT_FILE = './buycan-tldr-TMP.txt'
TMP_JSON_FILE = './buycan-tldr-TMP.json'

def getUrlFromSubmission(submission):
    textBody = submission.title+"\n"+submission.selftext+"\n"+submission.url
    # return getUrlFromTextBody(textBody)
    pass

def getUrlFromTextBody(body):
    url_regex = '(http[s]?://[\w\.]+)'
    findings = re.findall(url_regex, body)
    if(findings): 
        return findings[0]
    
    return None

def getUrlFromParent(reddit, comment):
    pid = comment.parent_id
    isSubmission = pid[:2] == 't3'

    if(isSubmission):
        submission = comment.parent()
        return getUrlFromSubmission(submission)
    else:
        comment = comment.parent()
        return getUrlFromTextBody(comment.body)

def allowedDomains(url):
    return re.sub('http[s]?://', '', url)

def startUrl(url):
    return url+"/robots.txt"

def handleCall(reddit, comment):
    url = getUrlFromTextBody(comment.body)
    if(not url): url = getUrlFromParent(reddit, comment)
    if(not url): return 

    f = open(TMP_TXT_FILE, 'w')
    f.write(url)
    f.close()

    if(os.path.isfile(TMP_JSON_FILE)):
        os.system("rm "+TMP_JSON_FILE)
    os.system("scrapy crawl --nolog about -o "+TMP_JSON_FILE)

    summary = smmry.create()

    comment.reply(summary)
    
def main(minu=10):
    reddit = praw.Reddit('tldr')

    # get current time and correct for how far back we want to look
    _now = datetime.now()
    _x_time_ago = _now - timedelta(minutes=minu)

    # convert UTC time to a float for comparison
    read_upto_time = _x_time_ago.timestamp()

    subreddit = reddit.subreddit('BuyCanadian')
    for comment in subreddit.comments(limit=50):
        created_time = comment.created_utc
        if(comment.author == "BuyCanadianWikiBot"):
            pass
        elif created_time < read_upto_time:
            break
        elif(re.search('!about', comment.body)):
            handleCall(reddit, comment)

if __name__ == "__main__":
    main()