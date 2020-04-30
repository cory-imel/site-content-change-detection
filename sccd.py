import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import smtplib
import configparser
from email.message import EmailMessage


config = configparser.ConfigParser()
config.read('config.txt')

URL = config.get('SETTINGS', 'URL')
TOADDR = config.get('SETTINGS', 'TOADDR')
FROMADDR = config.get('SETTINGS', 'FROMADDR')
MSG = config.get('SETTINGS', 'MSG')
USERNAME = config.get('SETTINGS', 'USERNAME')
PASSWORD = config.get('SETTINGS', 'PASSWORD')
SMTP = config.get('SETTINGS', 'SMTP')
STRING = config.get('SETTINGS', 'STRING').split('|')

while True:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:75.0.0) Gecko/20100101 Firefox/75.0'}
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    li_tags = soup.find_all('li')
    found = 0
    for li_tag in li_tags:
        if str(li_tag) == STRING[0] or str(li_tag) == STRING[1] or str(li_tag) == STRING[2] or str(li_tag) == STRING[3]:
            print(li_tag)
            found += 1

    if found == 4:
        print("sleeping 60 seconds - ", datetime.now())
        time.sleep(60)
        continue

    else:

        server = smtplib.SMTP(SMTP, 587)
        server.starttls()
        server.login(USERNAME, PASSWORD)

        msg = EmailMessage()
        msg.set_content(MSG)

        msg['Subject'] = 'Check njh site - ' + str(datetime.now())
        msg['From'] = str(FROMADDR)
        msg['To'] = str(TOADDR)

        print('From: ' + str(FROMADDR))
        print('To: ' + str(TOADDR))
        print('Message: ' + str(MSG))

        server.send_message(msg)
        server.quit()
        break
