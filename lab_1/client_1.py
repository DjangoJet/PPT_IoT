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

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (args.i, args.p)

    try:
        message = [hat.temperature, hat.pressure, hat.humidity]
        print('Sending {!r}'.format(message))
        sent = sock.sendto(pickle.dumps(message), server_address)
    finally:
        print('Closing socket')
        sock.close()
    sleep(0.5)
