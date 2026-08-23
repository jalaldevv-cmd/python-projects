from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import pandas as pd


URL = "https://www.scrapingcourse.com/javascript-rendering"


def scrape_products(page):
    products = []

    try:
        page.goto(URL, timeout=10000)

    except PlaywrightTimeoutError:
        print("Page took too long to load.")
        return []

    product_cards = page.locator(".product-item")

    for i in range(product_cards.count()):
        product = product_cards.nth(i)

        name = product.locator(".product-name").inner_text()
        price = product.locator(".product-price").inner_text()
        product_url = product.locator("a").get_attribute("href")

        products.append({
            "name": name,
            "price": price,
            "url": product_url
        })

    return products


def save_products(products):
    if not products:
        print("No products to save.")
        return
    
    data = pd.DataFrame(products)

    data["price"] = (
        data["price"]
        .str.replace("$", "", regex=False)
        .astype(float)
    )

    data = data.drop_duplicates()

    data.to_csv("dynamic_products.csv", index=False)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        products = scrape_products(page)

        save_products(products)

        browser.close()

    print(f"Saved {len(products)} products.")


if __name__ == "__main__":
    main()
