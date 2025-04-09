from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required

app = Flask(__name__, static_folder="../frontend", static_url_path="")
app.config["JWT_SECRET_KEY"] = "supersecretakey123!"
CORS(app, resources={r"/api/*": {"origins": "*"}})
jwt = JWTManager(app)

# ---------------------- API Routes ----------------------
@app.route("/api/login", methods=["POST"])
def login():
    return jsonify({
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
        "business_id": 1
    }), 200

@app.route("/api/products", methods=["GET"])
@jwt_required()
def get_products():
    return jsonify([
        {
            "id": 1,
            "name": "Laptop Gamer",
            "barcode": "123456789",
            "stock": 15,
            "sale_price": 1500.00
        },
        {
            "id": 2,
            "name": "Teclado Mecánico",
            "barcode": "987654321",
            "stock": 35,
            "sale_price": 120.50
        }
    ]), 200

@app.route("/api/analytics/sales-data", methods=["GET"])
@jwt_required()
def sales_data():
    return jsonify([
        {"product": "Laptop Gamer", "sales": 42},
        {"product": "Teclado Mecánico", "sales": 89}
    ]), 200

# ---------------------- Serve Frontend ----------------------
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)