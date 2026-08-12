import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

URL = "https://books.toscrape.com/"


def get_html(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None


def extract_books(soup):
    books = []

    book_items = soup.find_all("article", class_="product_pod")

    for book in book_items:
        try:
            title = book.h3.a["title"]
            price_text = book.find("p", class_="price_color").text.strip()

            price = float(price_text.replace("£", ""))

            availability = book.find("p", class_="instock availability").text.strip()

            rating = book.p["class"][1]

            books.append(
                {
                    "title": title,
                    "price": price,
                    "currency": "GBP",
                    "availability": availability,
                    "rating": rating,
                }
            )

        except (AttributeError, KeyError, ValueError) as e:
            print(f"Could not extract the book: {e}")

    return books


def get_next_page(soup):
    next_button = soup.find("li", class_="next")

    if next_button:
        return next_button.a["href"]

    return None


def save_books(books):
    try:
        with open("books.csv", "w", newline="", encoding="utf-8") as file:

            fieldnames = ["title", "price", "currency", "availability", "rating"]

            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(books)

    except OSError as e:
        print(f"Could not save CSV file: {e}")


def main():
    current_url = URL
    all_books = []

    while current_url:
        html = get_html(current_url)

        if html is None:
            break

        soup = BeautifulSoup(html, "html.parser")

        books = extract_books(soup)
        all_books.extend(books)

        next_page = get_next_page(soup)

        if next_page:
            current_url = urljoin(current_url, next_page)
        else:
            current_url = None

    save_books(all_books)

    print(f"Saved {len(all_books)} books.")


if __name__ == "__main__":
    main()
