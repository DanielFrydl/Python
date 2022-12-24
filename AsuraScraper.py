import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import os
import functools
import concurrent.futures
print('Insert URL for scraping: ')
url = input()
#url = 'https://asura.gg/manga/heavenly-demon-instructor/'
session = requests.Session()
reqs = session.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')
folderName = 'images'

def download_image():
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Create a list of tasks to be executed concurrently
        tasks = [executor.submit(download_image_task, i) for i in imageArray]
        # Iterate over the tasks and display a progress bar
        for task in concurrent.futures.as_completed(tasks):
            pass

@functools.lru_cache(maxsize=None)
def download_image_task(i):  
    for i in (pbar := tqdm(imageArray,bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}')):
        session_ID = requests.Session()
        pbar.set_description('Progress of: ' + rawstring)
        source = session_ID.get(i)
        try:
            with open(directory + '/' + i.split('/')[-1], 'wb') as img:
                img.write(source.content)
        except FileNotFoundError:
            os.mkdir(directory)
            with open(directory + '/' + i.split('/')[-1], 'wb') as img:
                img.write(source.content)
try:
    if os.path.isdir(folderName):
        print('Folder Exists')
    else:
        os.mkdir(folderName)
except:
    print('Failure')

urls = []
for link in soup.find_all('a'):
    href = str(link.get('href'))
    if 'chapter' in href:
        urls.append(href)

badChars = ["asura","scans","https","gg"]

for URL in urls:
    session2 = requests.Session()
    getURL = session2.get(URL)
    newsoup = BeautifulSoup(getURL.text, 'html.parser')
    images = newsoup.find_all('img')
    rawstring = ''.join(letter for letter in URL if letter.isalnum())

    for character in badChars:
        rawstring = rawstring.replace(character,"")
    directory = 'images/' + rawstring.upper()
    imageArray = []

    for newimage in images:
        imageArray.append(newimage.get('src'))
    
    if not os.path.exists(directory):
        download_image()
    else: pass
