import paho.mqtt.client as mqtt
from sense_emu import SenseHat
import time
import json

hat = SenseHat()

mqttBroker ="test.mosquitto.org" 

client = mqtt.Client("Sense_sensors")
client.connect(mqttBroker) 

while True:
    client.publish("SENSOR_DATA", json.dumps({
        "temperature": hat.temperature,
        "pressure": hat.pressure,
        "humidity": hat.humidity
    }))
    time.sleep(1)