from google_patent_scraper import scraper_class
import json
import os
import time

scraper=scraper_class(return_abstract=True)
           
if __name__ == '__main__':
    input_path="./PatentsData/PatentsApplicationNumber"
    output_path="./PatentsData/MainDatas"
    total=0
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
                            err, soup, url=scraper.request_single_patent(id)
                            patent_parsed = scraper.get_scraped_data( soup, id,url)
                            f_output.write("id-"+id);f_output.write("    ")
                            f_output.write("abstract-"+patent_parsed['abstract_text'].strip().replace("\n",""))
                            f_output.write("\n")
                            time.sleep(3)