from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*")

bill = []

@app.route("/")
def home():
    return "🛒 EyeBill Running (REAL TIME)"

@app.route("/add", methods=["POST"])
def add_item():
    data = request.json
    bill.append(data)

    print("ITEM:", data)

    # 🔥 REAL TIME PUSH
    socketio.emit("update", bill)

    return jsonify({"status": "ok"})

@app.route("/bill", methods=["GET"])
def get_bill():
    return jsonify(bill)

@app.route("/clear", methods=["GET"])
def clear():
    global bill
    bill = []
    socketio.emit("update", bill)
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
