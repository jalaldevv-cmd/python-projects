from database import get_connection
from models import Product
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/debug/routes")
def debug_routes():
    return [route.path for route in app.routes]

@app.get("/products")
def get_products():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM products
        """)

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return products


@app.get("/products/{product_id}")
def get_product(product_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM products
        WHERE id = %s
        """,
        (product_id,),
    )

    product = cursor.fetchone()

    cursor.close()
    connection.close()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products")
def create_product(product: Product):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO products (name, price)
        VALUES (%s, %s)
        """,
        (product.name, product.price),
    )

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Product successfully created",
        "name": product.name,
        "price": product.price,
    }


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM products
        WHERE id = %s
        """,
        (product_id,),
    )

    delete_checker = cursor.rowcount

    connection.commit()

    cursor.close()
    connection.close()

    if delete_checker == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": f"Product #{product_id} successfully deleted"}


@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE products
        SET name = %s, price = %s
        WHERE id = %s
        """,
        (updated_product.name, updated_product.price, product_id),
    )

    update_checker = cursor.rowcount

    connection.commit()

    cursor.close()
    connection.close()

    if update_checker == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": f"Product #{product_id} successfully updated"}
