from bs4 import *
import requests
import re
from zipfile import ZipFile
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime

WEBDRIVER = r"C:\Desktop\python\Web Development\chromedriver.exe"
LOGO = r'''  _____                             _____                                
 |_   _|                           / ____|                               
   | |  _ __ ___   __ _  __ _  ___| (___   ___ _ __ __ _ _ __   ___ _ __ 
   | | | '_ ` _ \ / _` |/ _` |/ _ \\___ \ / __| '__/ _` | '_ \ / _ \ '__|
  _| |_| | | | | | (_| | (_| |  __/____) | (__| | | (_| | |_) |  __/ |   
 |_____|_| |_| |_|\__,_|\__, |\___|_____/ \___|_|  \__,_| .__/ \___|_|   
                         __/ |                          | |              
                        |___/                           |_|              '''

print(LOGO)
try:
    os.mkdir('Images')
except FileExistsError:
    os.removedirs('Images')
    os.mkdir('Images')

site = input("Enter URL:\n")
while site[:4] != "http":
    print("Please enter full url with http/https")
    site = input("Enter full URL:\n")

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
start_time = datetime.datetime.now()
browser.get(site)
time.sleep(2)
content = browser.find_element(By.XPATH, "//*").get_attribute('outerHTML')
soup = BeautifulSoup(content, 'html.parser')
image_tags = soup.find_all('img')

urls = [img['src'] for img in image_tags]
filenames = []
for url in urls:
    filename = re.search(r'/([\w+" "+"("+")"_-]+[.](jpg|gif|png|svg|webp))$', url)
    if not filename:
        print("This url was skipped because of incorrect format: {}".format(url))
        continue
    with open(f"./Images/{filename.group(1)}", 'wb') as f:
        if 'http' not in url:
            url = '{}{}'.format(site, url)
        response = requests.get(url)
        f.write(response.content)
with ZipFile('images.zip', 'w') as zipObj:
    for filename in os.listdir(f"./Images/"):
        zipObj.write(f'./Images/{filename}')
for file in os.listdir(f"./Images/"):
    os.remove(f"./Images/{file}")

os.removedirs('Images')
end_time = datetime.datetime.now()

print('--------------------------------------')
print(f'Completed in {end_time - start_time}!\nimages.zip saved in folder.')
