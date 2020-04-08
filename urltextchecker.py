#!/usr/bin/env python
"""urltextcheck is a script which looks for a user specified text pattern
in the html of a particular URL"""
import argparse
import os
import re

import requests
from bs4 import BeautifulSoup
from pushover import Client

parser = argparse.ArgumentParser(description='textcheck')
parser.add_argument(
    '-u', '--url', help='URL whose text will be searched, e.g. http://www.example.com',
    required=True)
parser.add_argument('-t', '--text', help='Exact text to search for', required=True)
parser.add_argument(
    '-T', '--title', help='Message title which is sent when the text is found',
    required=True)
parser.add_argument(
    '-i', '--inverse', help='Inverse operation: send email if text is NOT found',
    required=False, action='store_true')
args = parser.parse_args()

url = args.url
text = args.text
message_title = args.title
send_if_not_found = args.inverse

message_body = f"URL: {url}\nText: {text}"

pattern = re.compile(text)

page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')

found_items = soup(text=pattern)

found_text = False

if len(found_items) is not 0:
    found_text = True

print(f"Found text: {found_text}")

if found_text != send_if_not_found:
    print("Sending notification")
    client = Client(os.getenv("PUSHOVER_KEY"), api_token=os.getenv("PUSHOVER_TOKEN"))
    client.send_message(message_body, title=message_title)
