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
           
def scraw_patent(id):
    url = f'https://patents.google.com/patent/{id}/'
    print(url)
    driver.get(url)
    wait = WebDriverWait(driver, 1)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    #citation is Patent cited what
    table = soup.find('div', {'class': 'table style-scope patent-result'})
    items = table.find_all('a', {'class': 'style-scope state-modifier','id':'link'})
    citation = []
    if items != []:
        for item in items:
            citation.append(item.text.strip())
    else: pass        
    
    #abstract is here
    abstract = soup.find('div', {'class': 'abstract style-scope patent-text'}).text
    print(abstract)
    
    #title 
    title = soup.find('h1',{'id':'title'}).text.strip()
    print(title)
    
    #citedBy
    tableByCited = soup.find('div', {'class': 'tbody style-scope patent-result'})
    items = tableByCited.find_all('a', {'class': 'style-scope state-modifier','id':'link'})
    citedByPatents = []
    if items != []:
        for item in items:
            citedByPatents.append(item.text.strip())
    else: pass
    print(citedByPatents)
    
    return citation
    
print(scraw_patent('US9359556B2'))