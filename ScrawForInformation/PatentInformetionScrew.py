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
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "search-ui")))
    
    SCROLL_PAUSE_TIME = 1  
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load the page.
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    patent_information_dict = {}
    
    #citation number
    citation_account = soup.find('h3',{'id':'patentCitations'})
    if citation_account == None :
        citation_exist = 0
        patent_information_dict['citation_exist'] = "NoCitation"
    else:
        citation_exist = 1
        patent_information_dict['citation_exist'] = citation_account.text.strip()
    
    #citation is Patent cited what
    if citation_exist == 0:
        patent_information_dict['citation_infor'] = 'NoCitation'
    else:
        table = citation_account.find_next('div', {'class': 'table style-scope patent-result'})
        citation_items = table.find_all('div', {'class': 'tr style-scope patent-result'})
        citation = []
        if citation_items != []:
            for item in citation_items:
                single_items = []
                all_span = item.find_all('span')
                for small_item in all_span:
                    single_items.append(small_item.text.strip().strip('\n').replace('\n', ''))
                citation.append(single_items)
        else: pass         
        patent_information_dict['citation_infor'] = citation
        
    
    #non patent citation number
    non_patent_citation_account = soup.find('h3',{'id':'nplCitations'})
    if non_patent_citation_account == None :
        non_patent_citation_exist = 0
        patent_information_dict['non_patent_citation_exist'] = "NoNonPatentCitation"
    else:
        non_patent_citation_exist = 1
        patent_information_dict['non_patent_citation_exist'] = non_patent_citation_account.text
    
    #non patent citation is Patent cited what
    if non_patent_citation_exist == 0:
        patent_information_dict['non_patent_citation_infor'] = 'NoNonPatentCitation'
    else:
        table = non_patent_citation_account.find_next('div', {'class': 'table style-scope patent-result'})
        citation_items = table.find_all('div', {'class': 'tr style-scope patent-result'})
        citation = []
        if citation_items != []:
            for item in citation_items:
                single_items = []
                all_span = item.find_all('span')
                for small_item in all_span:
                    single_items.append(small_item.text.strip().strip('\n').replace('\n', ''))
                citation.append(single_items)
        else: pass 
    
    #citedBy number
    citedBy_account = soup.find('h3',{'id':'citedBy'})
    if citedBy_account == None :
        citedBy_exist = 0
        patent_information_dict['citedBy_exist'] = "NocitedBy"
    else:
        citedBy_exist = 1
        patent_information_dict['citedBy_exist'] = citedBy_account.text
    
    #citedBy is what Patent cited
    if citedBy_exist == 0:
        patent_information_dict['citedBy_infor'] = 'NocitedBy'
    else:
        table = citedBy_account.find_next('div', {'class': 'table style-scope patent-result'})
        citation_items = table.find_all('div', {'class': 'tr style-scope patent-result'})
        citation = []
        if citation_items != []:
            for item in citation_items:
                single_items = []
                all_span = item.find_all('span')
                for small_item in all_span:
                    single_items.append(small_item.text.strip().strip('\n').replace('\n', ''))
                citation.append(single_items)
        else: pass  
        patent_information_dict['citedBy_infor'] = citation
        
    #abstract is here
    abstract = soup.find('div', {'class':'abstract style-scope patent-text'})
    if abstract != None:
        patent_information_dict['abstract'] = abstract.text.strip().replace('\n', '')
    else:
        patent_information_dict['abstract'] = ''
    
    #title 
    title = soup.find('h1',{'id':'title'})
    if title != None:
        patent_information_dict['title'] = title.text.strip().replace('\n', '')
    else:
        patent_information_dict['title'] = ''

    #find similar document
    similar_document = soup.find('h3',{'id':'similarDocuments'})
    if similar_document == None:
        patent_information_dict['similar_document'] = "NoExist"
    else:
        table = similar_document.find_next('div', {'class': 'table style-scope patent-result'})
        similar_items = table.find_all('div',{'class':'tr style-scope patent-result'})
        similar_list = []
        for similar in similar_items:
            similar_span = similar.find_all('span')
            single_similar_list = []
            for similar_span_single in similar_span:
                single_similar_list.append(similar_span_single.text.strip().strip('\n').replace('\n', ''))
            similar_list.append(single_similar_list)
        patent_information_dict['similar_document'] = similar_list
    
    #find patent application
    patent_application = soup.find('h3',{'id':'parentApplications'})
    if patent_application == None:
        patent_information_dict['patent_application'] = "NoExist"
    else:
        patent_application_items = patent_application.find_next('div',{'class':'table style-scope patent-result'})
        patent_application_list = []
        patent_application_items = patent_application_items.find_all('div',{'class':'tr style-scope patent-result'})
        for patent_application_single in patent_application_items:
            single_patent_application = []
            patent_application_span = patent_application_single.find_all('span')
            for span in patent_application_span:
                single_patent_application.append(span.text.strip().strip('\n').replace('\n', ''))
            patent_application_list.append(single_patent_application)
        patent_information_dict['patent_application'] = patent_application_list
        
    #find priority application
    patent_priority_application = soup.find('h3',{'id':'applicationPriorityApps'})
    if patent_priority_application == None:
        patent_information_dict['patent_priority_application'] = "NoExist"
    else:
        patent_priority_application_items = patent_priority_application.find_next('div',{'class':'table style-scope patent-result'})
        patent_priority_application_list = []
        patent_priority_application_items = patent_priority_application_items.find_all('div',{'class':'tr style-scope patent-result'})
        for patent_priority_application in patent_priority_application_items:
            single_patent_priority_application = []
            patent_priority_application_span = patent_priority_application.find_all('span')
            for span in patent_priority_application_span:
                single_patent_priority_application.append(span.text.strip().strip('\n').replace('\n', ''))
            patent_priority_application_list.append(single_patent_priority_application)
        patent_information_dict['patent_priority_application'] = patent_priority_application_list
    
    #find Applications Claiming Priority
    patent_priority_application = soup.find('h3',{'id':'appsClaimingPriority'})
    if patent_priority_application == None:
        patent_information_dict['patent_application_claiming_priority'] = "NoExist"
    else:
        patent_priority_application_items = patent_priority_application.find_next('div',{'class':'table style-scope patent-result'})
        patent_priority_application_list = []
        patent_priority_application_items = patent_priority_application_items.find_all('div',{'class':'tr style-scope patent-result'})
        for patent_priority_application in patent_priority_application_items:
            single_patent_priority_application = []
            patent_priority_application_span = patent_priority_application.find_all('span')
            for span in patent_priority_application_span:
                single_patent_priority_application.append(span.text.strip().strip('\n').replace('\n', ''))
            patent_priority_application_list.append(single_patent_priority_application)
        patent_information_dict['patent_application_claiming_priority'] = patent_priority_application_list
        
    
    #find legalEvents
    patent_priority_application = soup.find('h3',{'id':'legalEvents'})
    if patent_priority_application == None:
        patent_information_dict['legal_event'] = "NoExist"
    else:
        patent_priority_application_items = patent_priority_application.find_next('div',{'class':'table style-scope patent-result'})
        patent_priority_application_list = []
        patent_priority_application_items = patent_priority_application_items.find_all('div',{'class':'tr style-scope patent-result'})
        for patent_priority_application in patent_priority_application_items:
            single_patent_priority_application = []
            patent_priority_application_span = patent_priority_application.find_all('span')
            for span in patent_priority_application_span:
                single_patent_priority_application.append(span.text.strip().strip('\n').replace('\n', ''))
            patent_priority_application_list.append(single_patent_priority_application)
        patent_information_dict['legal_event'] = patent_priority_application_list
    
    
    #find inventor numbers
    inventor_infor = soup.find('dl',{'class':'important-people style-scope patent-result'})
    if inventor_infor != None:
        inventor_infor = inventor_infor.find_all('dd')
        patent_information_dict['inventor_number']  = len(inventor_infor)
    else:
        patent_information_dict['inventor_number']  = 0
    
    #find how many classification it in
    classfication = soup.find('section',{'id':'classifications','class':'style-scope patent-result'})
    if classfication != None:
        classification_tree = classfication.find_all('classification-tree',{'class':'style-scope classification-viewer'})
        patent_information_dict['classfication_nums'] = len(classification_tree)
        classfication_viewer = classfication.find('classification-viewer',{'class':'style-scope patent-result'})
        classfication_items = classfication.find_all('concept-mention',{'class':'style-scope classification-tree'})
        classfication_list = []
        for item in classfication_items:
            item = item.find('state-modifier',{'class':'code style-scope classification-tree'})
            classfication_list.append(item['data-cpc'])
        patent_information_dict['classfication_items'] = classfication_list
    else:
        patent_information_dict['classfication_nums'] = 0
        patent_information_dict['classfication_items'] = None
        
        
        
    application_timeline = soup.find('application-timeline',{'class':'style-scope patent-result'})
    
    #find application events
    application_events_title = application_timeline.find('div',{'class':'header style-scope application-timeline'})
    if application_events_title != None:
        application_events_find = application_events_title.find_all_next('div',{'class':'event layout horizontal style-scope application-timeline'})
        application_events = []
        for item in application_events_find:
            single_event = []
            time_search = item.find('div',{'date':''})
            if time_search != None:
                single_event.append(time_search.text.strip().replace('\n', ''))
            else:
                single_event.append('NoTime')
            single_event.append(item.find('span',{'class':'title-text style-scope application-timeline'}).text.strip().replace('\n', ''))
            application_events.append(single_event)
        patent_information_dict['application_events'] = application_events
    else:
        patent_information_dict['application_events'] = 'NoExist'
        
    #find Worldwide applications
    worldwide_application_find = application_timeline.find('div',{'class':'event style-scope application-timeline'})
    if  worldwide_application_find != None:
        worldwide_active_application_final = []
        worldwide_not_active_application_final = []
        worldwide_active_spans = worldwide_application_find.find_all('span',{'id':'cc','class':'active style-scope application-timeline'})
        worldwide_not_active_spans = worldwide_application_find.find_all('span',{'id':'cc','class':'not_active style-scope application-timeline'})
        for item in worldwide_active_spans:
            worldwide_active_application_final.append(item.text.strip().replace('\n','').replace(',',''))
        for item in worldwide_not_active_spans:
            worldwide_not_active_application_final.append(item.text.strip().replace('\n','').replace(',',''))
        patent_information_dict['active_area'] = worldwide_active_application_final
        patent_information_dict['not_active_area'] = worldwide_not_active_application_final
    else:
        patent_information_dict['active_area'] = 'NoExist'
        patent_information_dict['not_active_area'] = 'NoExist'
        
    return patent_information_dict
    
dict_p = scraw_patent('US9359556B2')
with open('test.txt','w',encoding='utf-8') as f:
    for key,value in dict_p.items():
        f.write(key)
        f.write('    ')
        if isinstance(value,list):
            f.write(str(len(value)))
            for i in value:
                f.write('    ')
                f.write(','.join(i))
                f.write('\n')
            f.write('\n')
        else:
            f.write('    ')
            f.write(str(value))
            f.write('\n')