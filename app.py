import time
import random
import eventlet
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO

eventlet.monkey_patch()

app = Flask(__name__)
app.config["SECRET_KEY"] = "demo"
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

current_metric = 50.0

def background_data_generator():
    global current_metric
    while True:
        current_metric += random.uniform(-2.0, 2.0)
        current_metric = max(0, min(100, current_metric))
        
        timestamp = time.strftime("%H:%M:%S")
        
        socketio.emit("server_push", {
            "type": "WebSocket",
            "time": timestamp,
            "value": round(current_metric, 2)
        })
        socketio.sleep(1)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/data")
def http_poll():
    return jsonify({
        "type": "HTTP",
        "time": time.strftime("%H:%M:%S"),
        "value": round(current_metric, 2)
    })

if __name__ == "__main__":
    socketio.start_background_task(background_data_generator)
    socketio.run(app, host="192.168.1.2", port=5000)