from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta

app = Flask(__name__)

# ==== Estructuras de datos ====
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyCircularList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.head.next = new_node
            self.head.prev = new_node
        else:
            tail = self.head.prev
            tail.next = new_node
            new_node.prev = tail
            new_node.next = self.head
            self.head.prev = new_node

    def get_current(self):
        return self.head.data if self.head else None

    def rotate(self, steps=1):
        if not self.head:
            return
        for _ in range(steps):
            self.head = self.head.next


# ==== Datos base ====
time_zones = {
    "UTC": 0,
    "Colombia": -5,
    "United States": -4,
    "Spain": 2,
    "Japan": 9,
    "India": 5.5
}

# Lista doble circular para formatos
time_format_list = DoublyCircularList()
time_format_list.append("24")
time_format_list.append("12")


# ==== Rutas ====
@app.route("/")
def home():
    return render_template("index.html", zones=list(time_zones.keys()))

@app.route("/api/time")
def get_time():
    tz = request.args.get("timezone", "UTC")
    fmt = request.args.get("format", time_format_list.get_current())

    offset = time_zones.get(tz, 0)
    now = datetime.utcnow() + timedelta(hours=offset)

    if fmt == "12":
        time_str = now.strftime("%I:%M:%S %p")
    else:
        time_str = now.strftime("%H:%M:%S")

    return jsonify({
        "time": time_str,
        "timezone": tz,
        "format": fmt,
        "hours": now.hour,
        "minutes": now.minute,
        "seconds": now.second
    })

@app.route("/api/toggle-format", methods=["POST"])
def toggle_format():
    time_format_list.rotate()
    return jsonify({"new_format": time_format_list.get_current()})


if __name__ == "__main__":
    app.run(debug=True)
