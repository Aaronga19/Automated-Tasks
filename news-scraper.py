import requests

from bs4 import BeautifulSoup

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import datetime

with open("secret.json") as f:
    secret = json.loads(f.read())

def get_secret(secret_name, secrets=secret):
    try:
        return secrets[secret_name]
    except:
        msg = "la variable %s no existe" % secret_name
        raise (msg)

now = datetime.datetime.now()

# email content placeholder
content = ''


def extract_new(url):
    print('Extracting Hacker new Stories')
    cnt = ''
    cnt += (f'<b> HN Top Stories:</b>\n <br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td', attrs={'class':'title','valign':''})):
        cnt += ((f'{str(i+1)} :: {tag.text} \n <br>') if tag.text != 'More' else '')
    return cnt

cnt = extract_new('http://news.ycombinator.com/')
print('Content Extracted!')
content += cnt
content += ('<br>--------<br>')
content += ('<br><br> End of message') 

# Send the email

print('Composing Email...')

# Update your email details

SERVER = 'smtp.gmail.com'
PORT = 587
FROM = get_secret('FROM')
TO = get_secret('TO')
PSWD = get_secret('PSWD')

msg = MIMEMultipart()

msg['Subject'] = f'Top News Stories HN [Automated Email] {str(now.day)} - {str(now.month)} - {str(now.year)}'
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))


print ('Initiating Server...')

server = smtplib.SMTP(SERVER, PORT)

server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(FROM,PSWD)
server.sendmail(FROM, TO, msg.as_string())

print('---------------------------------- Email Sent... ----------------------------------')

server.quit()