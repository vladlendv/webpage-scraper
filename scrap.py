import requests
from bs4 import BeautifulSoup
from time import sleep

main_url = "https://scrapingclub.com"
fake_headers = {"User-Agent": "Mazila/6.6.6 (Windux; U; Windux NUT 6.1; en-NE; rv:1.1.1.1) Geckon/2007 Filefox/5.5.5 (.DA CSS 7.6.12345)"}
delay = 0.1

#detailed links for each product
card_urls = []

#final array of results
results = []

#get data from webpage and parse with bs4
def get_data(src):
  sleep(delay)
  response = requests.get(src, headers=fake_headers)
  data = BeautifulSoup(response.text, 'lxml')
  return data

#get the number of pagination pages
def get_pagination_length():
  url = main_url + '/exercise/list_basic/?page=1'
  data = get_data(url)
  number_of_pages = data.find_all("span", class_="page")
  return len(number_of_pages)

page_count = get_pagination_length()

print("Parsing has started...")
#go through all available pagination pages
for count in range(1, page_count):
  print(f'checked page {count}')
  url = f"{main_url}/exercise/list_basic/?page={count}"
  data = get_data(url)
  product_card = data.find_all("div", class_="w-full rounded border")

  #get all internal product links
  for product_card in product_card:
    internal_content = product_card.find("a").get("href")
    card_urls.append(internal_content)
  
#collect data from all cards into results
for card_url in card_urls:
  print(f'get data from card {card_url}.')
  url = main_url + card_url
  data = get_data(url)
  product_card = data.find("div", class_="my-8 w-full rounded border")
  name = product_card.find("h3", class_="card-title").text
  price = product_card.find("h4", class_="card-price").text
  description = product_card.find("p", class_="card-description").text
  img = product_card.find("img", class_="card-img-top").get("src")
  results.append(f"\n- {name} | price: {price}\n{description}\nimg link: {main_url + img}")

for i in results:
  print(i)

print(f"\nParsing completed successfully, { len(results) } results received. elapsed time { '%.0f' % ((delay * (page_count * len(card_urls) ) ) * 1000) } ms")

