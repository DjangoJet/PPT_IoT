import socket
import sys
import numpy as np
from time import sleep
from sense_emu import SenseHat
import pickle

import argparse

my_parser = argparse.ArgumentParser()
my_parser.add_argument('-i', action='store', type=str, required=True)
my_parser.add_argument('-p', action='store', type=int, required=True)

args = my_parser.parse_args()

hat = SenseHat()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((args.i, args.p))
    while True:
        message = [hat.temperature, hat.pressure, hat.humidity]
        print('Sending {!r}'.format(message))
        s.sendall(pickle.dumps(message))
        data = s.recv(1024)
        data = pickle.loads(data)
        print('Received', repr(data))
