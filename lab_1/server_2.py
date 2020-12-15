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

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = (args.i,args.p)
print('Starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

hat = SenseHat()

while True:
    print('\nWaiting to receive message')
    data, address = sock.recvfrom(4096)
    if data:
        message = [hat.temperature, hat.pressure, hat.humidity]
        send = sock.sendto(pickle.dumps(message), address)