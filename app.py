from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# ----------------------------
# DATABASE CONNECTION
# ----------------------------
def get_db():
    conn = sqlite3.connect("ecommerce.db")
    conn.row_factory = sqlite3.Row
    return conn


# ----------------------------
# INIT DATABASE
# ----------------------------
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        address TEXT,
        phone TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        price REAL,
        stock_quantity INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Cart (
        cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Cart_Items (
        cart_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cart_id INTEGER,
        product_id INTEGER,
        quantity INTEGER
    )
    """)

    conn.commit()
    conn.close()


init_db()


# ----------------------------
# HOME ROUTE
# ----------------------------
@app.route('/')
def home():
    return "🚀 Ecommerce Backend Running on Render with SQLite!"


# ----------------------------
# USERS
# ----------------------------
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Users")
    rows = cursor.fetchall()

    users = []
    for r in rows:
        users.append({
            "id": r["user_id"],
            "name": r["name"],
            "email": r["email"],
            "phone": r["phone"]
        })

    conn.close()
    return jsonify(users)


@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Users (name, email, password, address, phone)
        VALUES (?, ?, ?, ?, ?)
    """, (data['name'], data['email'], data['password'], data['address'], data['phone']))

    conn.commit()
    conn.close()

    return jsonify({"message": "User added"})


# ----------------------------
# PRODUCTS
# ----------------------------
@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Products")
    rows = cursor.fetchall()

    products = []
    for r in rows:
        products.append({
            "id": r["product_id"],
            "name": r["name"],
            "description": r["description"],
            "price": r["price"],
            "stock": r["stock_quantity"]
        })

    conn.close()
    return jsonify(products)


@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Products (name, description, price, stock_quantity)
        VALUES (?, ?, ?, ?)
    """, (data['name'], data['description'], data['price'], data['stock']))

    conn.commit()
    conn.close()

    return jsonify({"message": "Product added"})


# ----------------------------
# CART
# ----------------------------
@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Cart_Items (cart_id, product_id, quantity)
        VALUES (?, ?, ?)
    """, (data['cart_id'], data['product_id'], data['quantity']))

    conn.commit()
    conn.close()

    return jsonify({"message": "Added to cart"})


@app.route('/cart/<int:cart_id>', methods=['GET'])
def view_cart(cart_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.name, p.price, ci.quantity
        FROM Cart_Items ci
        JOIN Products p ON ci.product_id = p.product_id
        WHERE ci.cart_id = ?
    """, (cart_id,))

    rows = cursor.fetchall()

    cart = []
    for r in rows:
        cart.append({
            "product": r["name"],
            "price": r["price"],
            "quantity": r["quantity"]
        })

    conn.close()
    return jsonify(cart)


# ----------------------------
# RUN (IMPORTANT FOR RENDER)
# ----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
