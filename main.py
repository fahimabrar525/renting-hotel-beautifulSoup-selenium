import time

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import os
from dotenv import load_dotenv

QUESTIONS_URL = os.environ.get("QUESTIONS_URL")

load_dotenv()

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(url="https://www.booking.com/searchresults.html?ss=Cox%27s+Bazar%2C+Bangladesh&efdco=1&label=gog235jc-1DCAEoggI46AdIM1gDaBSIAQGYATG4ARfIAQzYAQPoAQH4AQKIAgGoAgO4AuaywbIGwAIB0gIkZDY4NGQyNWEtZmM4YS00Y2FjLWIyNTgtZThlYjhkNWE1NGY52AIE4AIB&aid=397594&lang=en-us&sb=1&src_elem=sb&src=index&dest_id=211349&dest_type=city&checkin=2024-05-31&checkout=2024-06-01&group_adults=2&no_rooms=1&group_children=0", headers=header)
web_html = response.text

soup = BeautifulSoup(web_html, "html.parser")

all_link_elements = soup.find_all(name="a", class_="a78ca197d0")

all_links = []
for link in all_link_elements:
    href = link["href"]

    if "http" not in href:
        all_links.append(f"https://www.booking.com{href}")
    else:
        all_links.append(href)

print(all_links)

all_prices = []
all_prices_elements = soup.find_all(name="span", class_="f6431b446c")

for link in all_prices_elements:
    my_links = link.getText().split()
    all_prices.append(my_links[1])

print(all_prices)

all_address_elements = soup.find_all(name="span", class_="b058f54b9a")
all_address = []

for address in all_address_elements:
    my_address = address.getText()
    all_address.append(my_address)

print(all_address)


driver = webdriver.Chrome()

for n in range(len(all_links)):
    driver.get(url=QUESTIONS_URL)

    time.sleep(3)

    address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

    address.send_keys(all_address[n])
    price.send_keys(all_prices[n])
    link.send_keys(all_links[n])
    submit.click()