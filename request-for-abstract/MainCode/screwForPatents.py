from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
import os

internatinalClassification = []
with open('./PatentsData/InternationalClassification/EnergyRecoveryAndUtilization.txt', 'r') as f:
    for application in f:
        application=application.strip()
        internatinalClassification.append(application)
print(internatinalClassification)

options = webdriver.FirefoxOptions()
options.add_argument('--headless')  # Run in headless mode (no GUI)
driver = webdriver.Firefox(options=options)

for classficationNumber in internatinalClassification:
    os.mkdir("./PatentsData/PatentsApplicationNumber/"+f"Class{classficationNumber}".replace("/","-"))
    for year in range(2008,2024):
        with open("./PatentsData/PatentsApplicationNumber/"+f"Class{classficationNumber}".replace("/","-")+f"/Date{str(year)}-{str(year+1)}.txt",'w') as f:
            for month in range(11):
                url = f'https://patents.google.com/?q=({classficationNumber})&after=priority:{str(year)+str(month+1).zfill(2)}02&before=priority:{str(year)+str(month+2).zfill(2)}01&num=100'
                driver.get(url)
                while not driver.find_elements(By.CSS_SELECTOR, 'search-result-item')  and not driver.find_elements(By.ID, 'noResultsMessage'):
                    time.sleep(1)
                if driver.find_elements(By.ID, 'noResultsMessage'):
                    continue
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                items = soup.find_all('span', {'class': 'style-scope search-results'})
                totalAccount = items[4].text
                totalPages = int(totalAccount.replace(",","")) // 100 
                if totalPages>10:
                    totalPages=10
                for page in range(totalPages+1):
                    urlPage = url + f"&page={str(page)}"
                    driver.get(urlPage)
                    while not driver.find_elements(By.CSS_SELECTOR, 'search-result-item'):
                        time.sleep(1)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    items = soup.find_all('span', {'class': 'style-scope search-result-item','data-proto':'OPEN_PATENT_PDF'})
                    for patent in items:
                        f.write(patent.text)
                        f.write("\n")
            url = f'https://patents.google.com/?q=({classficationNumber})&after=priority:{str(year)+str(month+2).zfill(2)}02&before=priority:{str(year+1)+str(1).zfill(2)}01&num=100'
            driver.get(url)
            while not driver.find_elements(By.CSS_SELECTOR, 'search-result-item')  and not driver.find_elements(By.ID, 'noResultsMessage'):
                time.sleep(1)
            if driver.find_elements(By.ID, 'noResultsMessage'):
                continue
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            items = soup.find_all('span', {'class': 'style-scope search-results'})
            totalAccount = items[4].text
            totalPages = int(totalAccount.replace(",","")) // 100 
            if totalPages>10:
                totalPages=10
            for page in range(totalPages):
                urlPage = url + f"&page={str(page)}"
                driver.get(urlPage)
                while not driver.find_elements(By.CSS_SELECTOR, 'search-result-item')  and not driver.find_elements(By.ID, 'noResultsMessage'):
                    time.sleep(1)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                items = soup.find_all('span', {'class': 'style-scope search-result-item','data-proto':'OPEN_PATENT_PDF'})
                for patent in items:
                    f.write(patent.text)
                    f.write("\n")