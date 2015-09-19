#!/usr/bin/env python
"""urltextcheck is a script which looks for a user specified text pattern
in the html of a particular URL"""
import argparse
import os
import re
import smtplib
from email.mime.text import MIMEText

import requests
from bs4 import BeautifulSoup

#if __name__ == "__main__":
parser = argparse.ArgumentParser(description='textcheck')
parser.add_argument(
    '-u', '--url', help='URL whose text will be searched, e.g. http://www.example.com',
    required=True)
parser.add_argument('-t', '--text', help='Exact text to search for', required=True)
parser.add_argument(
    '-e', '--email', help='Email address to send notification if text is found',
    required=True)
parser.add_argument(
    '-s', '--subject', help='Email subject which is sent when the text is found',
    required=True)
parser.add_argument(
    '-i', '--inverse', help='Inverse operation: send email if text is NOT found',
    required=False, action='store_true')
args = parser.parse_args()

url = args.url
text = args.text
to_email = args.email
email_subject = args.subject
send_if_not_found = args.inverse

# Chose to get these values from environment variables
# instead of a file or (gasp!) hardcoded in this script/
from_email = os.environ['FROM_EMAIL']
smtp_server = os.environ['SMTP_SERVER']
smtp_port = os.environ['SMTP_PORT']
smtp_password = os.environ['SMTP_PASSWORD']

email = MIMEText("URL: {0}\nText: {1}".format(url, text))

email['Subject'] = email_subject
email['From'] = from_email
email['To'] = to_email

pattern = re.compile(text)

page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')

found_items = soup(text=pattern)

found_text = False

if len(found_items) is not 0:
    found_text = True

if found_text != send_if_not_found:
    smtp_client = smtplib.SMTP(smtp_server, smtp_port)
    smtp_client.starttls()
    smtp_client.login(from_email, smtp_password)
    smtp_client.send_message(email)
