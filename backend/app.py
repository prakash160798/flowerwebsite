import os
from decimal import Decimal
from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

def get_db():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "db"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "floweradmin"),
        password=os.getenv("DB_PASSWORD", "change-me"),
        database=os.getenv("DB_NAME", "flower_shop"),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )

@app.get("/api/health")
def health():
    try:
        conn=get_db()
        conn.close()
        return jsonify(status="ok", database="reachable")
    except Exception as exc:
        return jsonify(status="error", database="unreachable", error=str(exc)),503

@app.get("/api/products")
def get_products():
    conn=get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id,name,description,price,stock FROM products ORDER BY id")
            products=cur.fetchall()
            for product in products:
                product["price"]=float(product["price"])
            return jsonify(products)
    finally:
        conn.close()

@app.post("/api/orders")
def create_order():
    data=request.get_json(silent=True) or {}
    customer=data.get("customer",{})
    items=data.get("items",[])

    if not items:
        return jsonify(error="Cart is empty"),400

    conn=get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO customers(name,email,phone,address) VALUES(%s,%s,%s,%s)",
                (customer.get("name"),customer.get("email"),
                 customer.get("phone"),customer.get("address"))
            )
            customer_id=cur.lastrowid
            total=Decimal("0")

            for item in items:
                quantity=int(item.get("quantity",1))
                cur.execute(
                    "SELECT price,stock FROM products WHERE id=%s FOR UPDATE",
                    (item["product_id"],)
                )
                product=cur.fetchone()
                if not product or product["stock"] < quantity:
                    conn.rollback()
                    return jsonify(error="Product is unavailable"),400
                total += Decimal(str(product["price"])) * quantity

            cur.execute(
                "INSERT INTO orders(customer_id,total_amount,order_status) VALUES(%s,%s,'PLACED')",
                (customer_id,total)
            )
            order_id=cur.lastrowid

            for item in items:
                quantity=int(item.get("quantity",1))
                cur.execute("SELECT price FROM products WHERE id=%s",(item["product_id"],))
                price=cur.fetchone()["price"]
                cur.execute(
                    "INSERT INTO order_items(order_id,product_id,quantity,price) VALUES(%s,%s,%s,%s)",
                    (order_id,item["product_id"],quantity,price)
                )
                cur.execute(
                    "UPDATE products SET stock=stock-%s WHERE id=%s",
                    (quantity,item["product_id"])
                )

            conn.commit()
            return jsonify(order_id=order_id,total=float(total),status="PLACED"),201

    except Exception as exc:
        conn.rollback()
        return jsonify(error=str(exc)),500
    finally:
        conn.close()

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000)
