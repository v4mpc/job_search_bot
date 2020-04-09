#!/usr/bin/python3
# for processing request

from urllib import request, parse, error
from bs4 import BeautifulSoup
import json
import re
import time
import math
import slack


TIME_TO_WAIT=20

def get_total_jobs():
    html = get_page_html()
    # lets replace all class with id so that not to interfier datatypes
    sm = html.find(class_="search-main__header__sub-title--faded")
    return int(sm.span.string)


def mySlack():
    slack_token = "xoxb-551750797382-1053373911459-i8k6VH1HHGf702DPGsAYliFj"
    client = slack.WebClient(token=slack_token)
    client.chat_postMessage(
    channel="CG7BZF52B",
    text="Hello from your app! :tada:"
    )

def get_total_pages():
    return math.ceil(get_total_jobs()/20)


def get_jobs(page):
    html = get_page_html(page)
    jobs = html.find(type="application/ld+json").string
    j = json.loads(jobs)
    return j['itemListElement']


def get_page_html(page=1):
    url = f"https://www.brightermonday.co.tz/jobs?page={page}"
    user_agent = 'Mozilla/5.0'
    req = request.Request(url, headers={'User-Agent': user_agent})
    try:
        with request.urlopen(req) as resp:
            # print(resp.read().decode('utf-8'))
            return BeautifulSoup(resp.read().decode('utf-8'), 'html.parser')
    except error.HTTPError as e:
        print(e.reason)
    except error.URLError as er:
        print(er.reason)
    else:
        print('Something is not right')




def main():
    print('Begin')
    for page in range(1, get_total_pages()+1):
        time.sleep(TIME_TO_WAIT)
        for job in get_jobs(page):
            if re.search(r'teach(er)?|literature|english|\b(ic?t)\b|software|developer|web|php|system|engineer|programmer|kiswahili|history|civics', job['name'], re.I):
                # notify_send(f'@page {page}', job["name"])
                print(job["name"])
    print('end')




if __name__ == '__main__':
    # main()
    mySlack()