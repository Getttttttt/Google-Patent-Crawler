# ~ Import packages ~ #
from google_patent_scraper import scraper_class
import json
# ~ Initialize scraper class ~ #
scraper=scraper_class(return_abstract=True)  #<- TURN ON ABSTRACT TEXT  

# ~~ Scrape patents individually ~~ #
patent_1 = 'WO2010085244A1'
err_1, soup_1, url_1 = scraper.request_single_patent(patent_1)

# ~ Parse results of scrape ~ #
patent_1_parsed = scraper.get_scraped_data(soup_1,patent_1,url_1)

# ~ Print abstract text ~ #
print(patent_1_parsed['abstract_text'])

for inventor in json.loads(patent_1_parsed['backward_cites_yes_family']):
    print(inventor)
    