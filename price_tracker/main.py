import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv

URL = "https://books.toscrape.com/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_html(url):
    response = requests.get(url, headers=headers)
    return response.text

def extract_price(html):
    soup = BeautifulSoup(html, "html.parser")

    price_tag = soup.find("p", class_="price_color")

    if not price_tag:
        return None
    else:
        return price_tag.text.strip()
    
def save_price(price):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("price.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, price])

def main():
    html = get_html(URL)
    price = extract_price(html)

    if price:
        save_price(price)
        print("Price saved successfully! Price found: ", price)

    else:
        print("Price not found...")

if __name__ == "__main__":
    main()
