import requests
from bs4 import BeautifulSoup
from time import sleep

def get_pagination_length():
  url = "https://scrapingclub.com/exercise/list_basic/?page=1"
  response = requests.get(url)
  html_data = BeautifulSoup(response.text, 'lxml')
  number_of_pages = html_data.find_all("span", class_="page")
  return len(number_of_pages)

page_count = get_pagination_length()
results = []
delay = 1

print("Parsing has started...")

for count in range(1, page_count):
  sleep(delay)
  url = f"https://scrapingclub.com/exercise/list_basic/?page={count}"
  response = requests.get(url)
  html_data = BeautifulSoup(response.text, 'lxml')
  product_cards = html_data.find_all("div", class_="w-full rounded border")

  for item in product_cards:
    item_name = item.find("h4").text.strip('\n')
    item_price = item.find("h5").text
    results.append(f"{item_name} {item_price}")
  
  
for i in results:
  print(i)

print(f"Parsing completed successfully, { len(results) } results received. elapsed time { '%.0f' % ((delay * page_count) * 1000) } ms")

