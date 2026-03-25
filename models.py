import os
from dotenv import load_dotenv
import mysql.connector
from datetime import datetime

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# 🔹 Insert new product
def add_product(name, url, target_price, email, current_price):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO products (product_name, product_url, target_price, email, current_price, last_checked)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (
        name,
        url,
        target_price,
        email,
        current_price,
        datetime.now()
    ))

    conn.commit()
    conn.close()


# 🔹 Get all products
def get_all_products():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products ORDER BY id DESC")
    products = cursor.fetchall()

    conn.close()
    return products


# 🔹 Get single product (NEW)
def get_product_by_id(product_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()

    conn.close()
    return product


# 🔹 Update price (used by tracker)
def update_price(product_id, price):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE products
    SET current_price = %s, last_checked = %s
    WHERE id = %s
    """

    cursor.execute(query, (price, datetime.now(), product_id))
    conn.commit()
    conn.close()


# 🔹 Update target price (NEW)
def update_product(product_id, new_price, new_email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE products SET target_price = %s, email = %s WHERE id = %s",
        (new_price, new_email, product_id)
    )

    conn.commit()
    conn.close()


# 🔹 Delete product (NEW)
def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))

    conn.commit()
    conn.close()


# 🔹 Insert price history
def insert_price_history(product_id, price):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO price_history (product_id, price, checked_at)
    VALUES (%s, %s, %s)
    """

    cursor.execute(query, (product_id, price, datetime.now()))
    conn.commit()
    conn.close()


# 🔹 Mark alert sent
def mark_alert_sent(product_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE products SET alert_sent = TRUE WHERE id = %s",
        (product_id,)
    )

    conn.commit()
    conn.close()