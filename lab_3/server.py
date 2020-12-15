from flask import Flask
import json
from sense_emu import SenseHat

hat = SenseHat()

app = Flask(__name__)


@app.route('/')
def hello():
    return json.dumps({
        "temperature": hat.temperature,
        "pressure": hat.pressure,
        "humidity": hat.humidity
    })