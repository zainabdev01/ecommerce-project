from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# ================= DATABASE =================
uri = os.environ.get("DATABASE_URL")

if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

if not uri:
    uri = "sqlite:///ecommerce.db"

app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ================= MODELS =================

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50))

# ================= INIT DB AUTOMATIC =================
with app.app_context():
    db.create_all()

# ================= ROUTES =================

@app.route("/")
def home():
    return "🚀 Ecommerce Backend Running Successfully"

# ---------- PRODUCTS ----------
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

# ---------- CART ----------
@app.route("/api/cart/add", methods=["POST"])
def add_cart():
    data = request.json
    item = CartItem(
        product_id=data["product_id"],
        quantity=data["quantity"]
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({"message": "Added to cart"})

# ---------- ORDERS ----------
@app.route("/api/order", methods=["POST"])
def create_order():
    order = Order(status="Processing")
    db.session.add(order)
    db.session.commit()
    return jsonify({"message": "Order created"})

# ================= RUN =================
if __name__ == "__main__":
    app.run()