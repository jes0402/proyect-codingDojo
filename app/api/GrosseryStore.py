import requests
from bs4 import BeautifulSoup


URL = "https://veggo.cl/tomate-kilogramo.html"

def get_price(URL):
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    price = soup.find("span", {"class": "price"}).text

    priceInt = int(price.replace("$", "").replace(".", ""))

    return priceInt