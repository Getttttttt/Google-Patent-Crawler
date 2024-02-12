import requests
from bs4 import BeautifulSoup

url = 'https://patents.google.com/?q=(CPC%3dF02B1%2f00)&oq=CPC%3dF02B1%2f00'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
items = soup.find_all('span', {'class': 'style-scope search-result-item'})
print(items)
