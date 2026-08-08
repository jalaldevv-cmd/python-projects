import requests
import sqlite3
from datetime import datetime

PRODUCT_URLS = ["https://dummyjson.com/products/1", "https://dummyjson.com/products/2", "https://dummyjson.com/products/3" ]

def create_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prices (
        id INTEGER PRIMARY KEY,
        date TEXT,
        product TEXT,
        price REAL
    )
    """)

def get_product(url):
    response = requests.get(url)
    response.raise_for_status()

    product = response.json()

    date = datetime.now().strftime("%Y-%m-%d")
    name = product["title"]
    price = product["price"]

    return (date, name, price)

def save_product(cursor, product_data):
    cursor.execute("""
    INSERT INTO prices (date, product, price)
    VALUES (?, ?, ?)
    """, product_data)

def get_previous_price(cursor, product_name):
    cursor.execute("""
    SELECT price
    FROM prices 
    WHERE product = ?
    ORDER BY id DESC
    LIMIT 1
    """, (product_name,))

    result = cursor.fetchone()

    if result:
        return result[0]

    return None

def display_price_change(current_price, previous_price):
    if previous_price is None:
        print("No previous price to compare.")

    elif current_price > previous_price:
        change = current_price - previous_price
        print(f"Price increased by {change:.2f}")

    elif current_price < previous_price:
        change = previous_price - current_price
        print(f"Price decreased by {change:.2f}")

    else:
        print("Price stayed the same.")
    

def display_prices(cursor):
    cursor.execute("""
    SELECT *
    FROM prices    
    """)

    products = cursor.fetchall()

    print("\nPrice History")
    print("-" * 30)

    for product in products:
        print(product)

def main():
    connection = sqlite3.connect("price_tracker.db")
    cursor = connection.cursor()

    create_table(cursor)

    for url in PRODUCT_URLS:
        product_data = get_product(url)

        _, product_name, current_price = product_data
        previous_price = get_previous_price(cursor, product_name)

        save_product(cursor, product_data)

        display_price_change(current_price, previous_price)

    connection.commit()

    display_prices(cursor)

    connection.close()


if __name__ == "__main__":
    main()

