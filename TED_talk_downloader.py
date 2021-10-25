import requests  # Geetting content from the page

from bs4 import BeautifulSoup #Library to Scrapy

import re # Regular expression pattern matching
import sys # for argument parsing

# Exception Handling

if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    raise sys.exit('Error: Please enter the Ted Talk URL')
#url = 'https://www.ted.com/talks/monday_com_relief_to_recovery'
r = requests.get(url)
print('Download about to start')

soup = BeautifulSoup(r.content, features='lxml')
for val in soup.findAll('script'):
    if (re.search('talkPage.init', str(val))) is not None:
        result = str(val)

result_mp4 = re.search("(?P<url>https?://[^\s]+)(mp4)", result).group('url')
mp4_url = result_mp4.split('"')[0]

print(f"Downloading video from...  {mp4_url}")

file_name = mp4_url.split("/")[len(mp4_url.split("/"))-1].split('?')[0]

print(f"Strong video in ... {file_name}")

r = requests.get(mp4_url)

with open(file_name,'wb') as f:
    f.write(r.content)

print("Download process has finished")