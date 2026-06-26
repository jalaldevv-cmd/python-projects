import requests
import csv
from bs4 import BeautifulSoup

URL = "https://www.scrapethissite.com/pages/simple/"

def get_html(url):
    response = requests.get(url)
    return response.text

def extract_countries(html):
    soup = BeautifulSoup(html, "html.parser")

    countries = soup.find_all("div", class_="country")

    results = []
    
    for country in countries:
        name = country.find("h3", class_="country-name").text.strip()
        capital = country.find("span", class_="country-capital").text.strip()
        population = country.find("span", class_="country-population").text.strip()

        results.append([name, capital, population])

    return results

def save_to_csv(data):
    with open("countries.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Country", "Capital", "Population"])

        for row in data:
            writer.writerow(row)

def main():
    print("Starting country scraping...")
    html = get_html(URL)
    countries = extract_countries(html)
    save_to_csv(countries)

    print(f"Saved {len(countries)} countries to CSV!")

if __name__ == "__main__":
    main()
