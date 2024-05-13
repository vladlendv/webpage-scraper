import requests
from bs4 import BeautifulSoup

url = "https://scrapingclub.com/exercise/list_basic/?page=1"
response = requests.get(url)
html_data = BeautifulSoup(response.text, 'lxml')
product_cards = html_data.find_all("div", class_="w-full rounded border")

test = []

for item in product_cards:
  item_name = item.find("h4").text.strip('\n')
  item_price = item.find("h5").text
  test.append(f"{item_name} {item_price}")
  
for i in test:
  print(i)