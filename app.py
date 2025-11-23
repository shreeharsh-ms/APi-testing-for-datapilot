from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'
socketio = SocketIO(app, cors_allowed_origins="*")  # allow dashboard to connect

# Simple in-memory list (optional, for demonstration only)
live_orders = []

# Render buy product page
@app.route("/")
def buy_page():
    return render_template("buy.html")

# API endpoint for website to send new order
@app.route("/api/new-order", methods=["POST"])
def new_order():
    try:
        order = request.json
        if not order.get("product") or not order.get("quantity"):
            return jsonify({"error": "Missing product or quantity"}), 400
        
        # Add to live orders
        live_orders.append(order)
        
        # Broadcast to all connected dashboards
        socketio.emit("new_order", order)
        print(f"📌 New Order: {order}")
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run WebSocket server
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8080, debug=True)
