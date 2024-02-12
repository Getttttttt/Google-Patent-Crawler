from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
import time
import re

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)

pattern = r"Cited By \((\d+)\)"
           
def scraw_citation_patent(id):
    url = f'https://patents.google.com/patent/{id}/'
    print(url)
    driver.get(url)
    wait = WebDriverWait(driver, 1)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('div', {'class': 'table style-scope patent-result'})
    items = table.find_all('a', {'class': 'style-scope state-modifier','id':'link'})
    citation = []
    if items != []:
        for item in items:
            citation.append(item.text.strip())
    else: pass
    return citation
    
print(scraw_citation_patent('US9359556B2'))