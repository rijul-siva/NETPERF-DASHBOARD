from flask import Flask, jsonify
import time
import random

app = Flask(__name__)
current_metric = 50.0

@app.route("/api/data")
def http_poll():
    global current_metric
    current_metric += random.uniform(-2.0, 2.0)
    current_metric = max(0, min(100, current_metric))
    return jsonify({
        "type": "HTTP",
        "time": time.strftime("%H:%M:%S"),
        "value": round(current_metric, 2)
    })

if __name__ == "__main__":
    app.run(port=5000)