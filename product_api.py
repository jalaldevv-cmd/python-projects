import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

DATABASE = "products.db"


class Product(BaseModel):
    name: str
    price: float


def create_table():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price REAL
    )
    """)

    connection.commit()
    connection.close()


@app.get("/products")
def get_products():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
    SELECT *
    FROM products
    """)

    products = cursor.fetchall()

    connection.close()

    return products


@app.get("/products/{product_id}")
def get_product(product_id: int):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
    SELECT *
    FROM products
    WHERE id = ?
    """,
        (product_id,),
    )

    product = cursor.fetchone()

    connection.close()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products")
def create_product(product: Product):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO products (name, price)
        VALUES (?, ?)
        """,
        (product.name, product.price),
    )

    connection.commit()
    connection.close()

    return {
        "message": "Product created",
        "name": product.name,
        "price": product.price,
    }


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
    DELETE FROM products 
    WHERE id = ?
    """,
        (product_id,),
    )

    deleted_rows = cursor.rowcount

    connection.commit()
    connection.close()

    if deleted_rows == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": f"Product #{product_id} successfully deleted"}


@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE products
        SET name = ?, price = ?
        WHERE id = ?
        """,
        (updated_product.name, updated_product.price, product_id),
    )

    update_checker = cursor.rowcount
    connection.commit()
    connection.close()

    if update_checker == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": f"Product #{product_id} successfully updated"}


create_table()
