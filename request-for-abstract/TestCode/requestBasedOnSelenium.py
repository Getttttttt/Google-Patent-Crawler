from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time

# Set up the Selenium driver
options = webdriver.FirefoxOptions()
options.add_argument('--headless')  # Run in headless mode (no GUI)
driver = webdriver.Firefox(options=options)

# Navigate to the page
url = 'https://patents.google.com/?q=(F02B1%2f00)&after=priority:20080101&num=100&page='
for i in range(29):
    url_page=url+str(i)
    driver.get(url_page)

    # Wait for the page to load
    while not driver.find_elements(By.CSS_SELECTOR, 'search-result-item'):
        time.sleep(1)

    # Get the page source and parse it with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    items = soup.find_all('span', {'class': 'style-scope search-result-item','data-proto':'OPEN_PATENT_PDF'})

    # Print the results
    print(items)

    time.sleep(20)
    
driver.quit()
