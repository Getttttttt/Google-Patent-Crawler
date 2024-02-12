import requests
from bs4 import BeautifulSoup

def get_patent_numbers(cpc):
    url = f"https://patents.google.com/?q=CPC%3D{cpc}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    patent_numbers = []
    for link in soup.find_all('a'):
        if link.get('href') and '/patent/' in link.get('href'):
            patent_number = link.get('href').split('/')[-1]
            patent_numbers.append(patent_number)
    return patent_numbers

cpc = "F02B1/00"
patent_numbers = get_patent_numbers(cpc)
print(patent_numbers)
