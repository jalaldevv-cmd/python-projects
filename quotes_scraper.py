import requests
import csv
from bs4 import BeautifulSoup

URL = 'https://quotes.toscrape.com/'


def get_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def extract_quotes(html):
    soup = BeautifulSoup(html, "html.parser")
    quote_tags = soup.find_all("div", class_="quote")
    results = []

    for tag in quote_tags:
        quote = tag.find("span", class_="text").text.strip()
        author = tag.find("small", class_="author").text.strip()
        results.append([quote, author]) 

    return results

def save_to_csv(quotes):
    
    with open("quotes.csv", "w", newline="", encoding="utf-8" ) as file:
        writer = csv.writer(file)
        writer.writerow(["Quote", "Author"])

        for row in quotes:
            writer.writerow(row)

def main():
    print('Starting quote scraper...')

    try:
        html = get_html(URL)
    
    except requests.RequestException as e:
        print("Request Failed: ", e)
        return
    
    quotes = extract_quotes(html)
    save_to_csv(quotes)

    print(f'Saved {len(quotes)} quotes successfully!')

if __name__ == "__main__":
    main()

    