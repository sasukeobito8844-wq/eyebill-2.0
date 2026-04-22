from flask import Flask, request, jsonify

app = Flask(__name__)

bill = []

# ---------------- HOME (NO 404) ----------------
@app.route("/")
def home():
    return "🛒 EyeBill Server Running"

# ---------------- ADD ITEM ----------------
@app.route("/add", methods=["POST"])
def add_item():
    data = request.json
    bill.append(data)
    print("ITEM ADDED:", data)
    return jsonify({"status": "ok"})

# ---------------- GET BILL ----------------
@app.route("/bill", methods=["GET"])
def get_bill():
    return jsonify(bill)

# ---------------- CLEAR BILL ----------------
@app.route("/clear", methods=["GET"])
def clear_bill():
    global bill
    bill = []
    return jsonify({"status": "cleared"})

# ---------------- REMOVE ITEM ----------------
@app.route("/remove/<int:index>", methods=["GET"])
def remove_item(index):
    global bill
    if 0 <= index < len(bill):
        bill.pop(index)
    return jsonify(bill)

# ---------------- RECEIPT ----------------
@app.route("/receipt", methods=["GET"])
def receipt():
    total = sum(item["price"] for item in bill)

    text = "----- EyeBill Receipt -----\n\n"

    for item in bill:
        text += f"{item['product']} - €{item['price']}\n"

    text += "\n--------------------------\n"
    text += f"TOTAL: €{round(total,2)}\n"
    text += "Thank you!\n"

    return text

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
