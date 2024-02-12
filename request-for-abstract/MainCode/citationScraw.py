from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
import os
import re

pattern = r"Cited By \((\d+)\)"

id='US20170190327A1'

options = webdriver.FirefoxOptions()
options.add_argument('--headless')  # Run in headless mode (no GUI)
driver = webdriver.Firefox(options=options)

url = f'https://patents.google.com/patent/{id}/'
driver.get(url)
while not driver.find_elements(By.ID, 'citedBy'):
    time.sleep(1)
soup = BeautifulSoup(driver.page_source, 'html.parser')
items = soup.find_all('h3', {'id': 'citedBy'})
cited_string = items[0].text.strip()
match = re.search(pattern, cited_string)
if match:
    number = match.group(1)
    print(number)
