from flask import Flask, request, jsonify
import pyodbc
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# SQL Server Connection
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=localhost;'
    'DATABASE=Ecommerce_order_managmentsystem;'
    'Trusted_Connection=yes;'
)

cursor = conn.cursor()

# Home Route
@app.route('/')
def home():
    return "Ecommerce Backend is Running!"

# Get Users API
@app.route('/users', methods=['GET'])
def get_users():
    cursor.execute("SELECT * FROM Users")
    rows = cursor.fetchall()

    users = []
    for r in rows:
        users.append({
            "id": r.user_id,
            "name": r.name,
            "email": r.email,
            "phone": r.phone
        })

    return jsonify(users)

# Add User API
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json

    cursor.execute("""
        INSERT INTO Users (name, email, password, address, phone)
        VALUES (?, ?, ?, ?, ?)
    """, data['name'], data['email'], data['password'], data['address'], data['phone'])

    conn.commit()
    return jsonify({"message": "User added successfully"})
@app.route('/products', methods=['GET'])
def get_products():
    cursor.execute("SELECT * FROM Products")
    rows = cursor.fetchall()

    products = []
    for r in rows:
        products.append({
            "id": r.product_id,
            "name": r.name,
            "price": float(r.price),
            "stock": r.stock_quantity
        })

    return jsonify(products)

if __name__ == '__main__':
    app.run(debug=True)