import socket
import sys
import numpy as np
from time import sleep
from sense_emu import SenseHat
import pickle
import selectors
import types

import argparse

my_parser = argparse.ArgumentParser()
my_parser.add_argument('-i', action='store', type=str, required=True)
my_parser.add_argument('-p', action='store', type=int, required=True)

args = my_parser.parse_args()

def clamp(value, min_value, max_value):
    """
    Returns *value* clamped to the range *min_value* to *max_value* inclusive.
    """
    return min(max_value, max(min_value, value))

def scale(value, from_min, from_max, to_min=0, to_max=8):
    """
    Returns *value*, which is expected to be in the range *from_min* to
    *from_max* inclusive, scaled to the range *to_min* to *to_max* inclusive.
    If *value* is not within the expected range, the result is not guaranteed
    to be in the scaled range.
    """
    from_range = from_max - from_min
    to_range = to_max - to_min
    return (((value - from_min) / from_range) * to_range) + to_min

def render_bar(screen, origin, width, height, color):
    """
    Fills a rectangle within *screen* based at *origin* (an ``(x, y)`` tuple),
    *width* pixels wide and *height* pixels high. The rectangle will be filled
    in *color*.
    """
    # Calculate the coordinates of the boundaries
    x1, y1 = origin
    x2 = x1 + width
    y2 = y1 + height
    # Invert the Y-coords so we're drawing bottom up
    max_y, max_x = screen.shape[:2]
    y1, y2 = max_y - y2, max_y - y1
    # Draw the bar
    screen[y1:y2, x1:x2, :] = color
    
def display_readings(hat, recv):
    """
    Display the temperature, pressure, and humidity readings of the HAT as red,
    green, and blue bars on the screen respectively.
    """
    # Calculate the environment values in screen coordinates
    temperature_range = (0, 40)
    pressure_range = (950, 1050)
    humidity_range = (0, 100)
    temperature = scale(clamp(recv[0], *temperature_range), *temperature_range)
    pressure = scale(clamp(recv[1], *pressure_range), *pressure_range)
    humidity = scale(clamp(recv[2], *humidity_range), *humidity_range)
    # Render the bars
    screen = np.zeros((8, 8, 3), dtype=np.uint8)
    render_bar(screen, (0, 0), 2, round(temperature), color=(255, 0, 0))
    render_bar(screen, (3, 0), 2, round(pressure), color=(0, 255, 0))
    render_bar(screen, (6, 0), 2, round(humidity), color=(0, 0, 255))
    hat.set_pixels([pixel for row in screen for pixel in row])

hat = SenseHat()

sel = selectors.DefaultSelector()
messages = [b"Message 1 from client.", b"Message 2 from client."]


def start_connections(host, port, num_conns):
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
        print("starting connection", connid, "to", server_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(
            connid=connid,
            msg_total=sum(len(m) for m in messages),
            recv_total=0,
            messages=list(messages),
            outb=b"",
        )
        sel.register(sock, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            print("received", pickle.loads(recv_data), "from connection", data.connid)
            display_readings(hat, pickle.loads(recv_data))
            data.recv_total += len(recv_data)
        if not recv_data:
            print("closing connection", data.connid)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb:
            data.outb = b'ok'
        if data.outb:
            print("sending", data.outb, "to connection", data.connid)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

host = args.i
port = args.p
num_conns = 1
start_connections(host, int(port), int(num_conns))

try:
    while True:
        events = sel.select(timeout=1)
        if events:
            for key, mask in events:
                service_connection(key, mask)
        # Check for a socket being monitored to continue.
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()