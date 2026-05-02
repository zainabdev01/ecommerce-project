from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# ================= DATABASE CONFIG =================
uri = os.environ.get("DATABASE_URL")

if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

# fallback (local testing)
if not uri:
    uri = "sqlite:///ecommerce.db"

app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ================= MODELS =================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    status = db.Column(db.String(50))

# ================= ROUTES =================

@app.route("/")
def home():
    return "🚀 Ecommerce Backend Running Successfully!"

# -------- PRODUCTS --------
@app.route("/api/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "stock": p.stock
        } for p in products
    ])

# -------- ADD PRODUCT (optional test) --------
@app.route("/api/products", methods=["POST"])
def add_product():
    data = request.json
    p = Product(
        name=data["name"],
        price=data["price"],
        stock=data["stock"]
    )
    db.session.add(p)
    db.session.commit()
    return jsonify({"message": "Product added"})

# -------- CART --------
@app.route("/api/cart/add", methods=["POST"])
def add_to_cart():
    data = request.json
    item = CartItem(
        cart_id=data["cart_id"],
        product_id=data["product_id"],
        quantity=data["quantity"]
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({"message": "Added to cart"})

@app.route("/api/cart/<int:cart_id>")
def get_cart(cart_id):
    items = CartItem.query.filter_by(cart_id=cart_id).all()
    return jsonify([
        {
            "product_id": i.product_id,
            "quantity": i.quantity
        } for i in items
    ])

# -------- ORDERS --------
@app.route("/api/order", methods=["POST"])
def create_order():
    data = request.json
    order = Order(
        user_id=data["user_id"],
        status="Processing"
    )
    db.session.add(order)
    db.session.commit()
    return jsonify({"message": "Order created"})

# ================= INIT DB =================
@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("Database created!")

# ================= RUN =================
if __name__ == "__main__":
    app.run()
