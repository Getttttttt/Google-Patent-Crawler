from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
import time
import re

pattern = r"Cited By \((\d+)\)"
           
if __name__ == '__main__':
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    input_path="./PatentsData/PatentsApplicationNumber"
    output_path="./PatentsData/MainDatas/Citation"
    for root, dirs, files in os.walk(input_path):
        for dir in dirs:
            if not os.path.exists(output_path+'/'+dir):
                os.mkdir(output_path+'/'+dir)
            for root, dirs, files in os.walk(input_path+'/'+dir):
                for file in files:
                    with open(output_path+'/'+dir+'/'+file,'w', encoding='utf-8') as f_output:
                        id_list=[]
                        with open(input_path+'/'+dir+'/'+file,'r') as f_input:
                            for line in f_input:
                                line=line.strip()
                                id_list.append(line)
                        for id in id_list:
                            url = f'https://patents.google.com/patent/{id}/'
                            print(url)
                            driver.get(url)
                            wait = WebDriverWait(driver, 1)
                            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                            soup = BeautifulSoup(driver.page_source, 'html.parser')
                            items = soup.find_all('h3', {'id': 'citedBy'})
                            if items != []:
                                cited_string = items[0].text.strip()
                                match = re.search(pattern, cited_string)
                                if match:
                                    number = match.group(1)
                            else:
                                number = ' '
                            f_output.write("id-"+id);f_output.write("    ")
                            f_output.write("citedBy-"+number)
                            f_output.write("\n")
                            time.sleep(2)