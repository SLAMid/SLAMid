#!/usr/bin/env python

import random
import socket, select
from time import gmtime, strftime
from random import randint
import sys

image = sys.argv[1]

HOST = '127.0.0.1'
PORT = 6666

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
sock.connect(server_address)

try:

    # open image
    myfile = open(image, 'rb')
    bytes = myfile.read()

    sock.sendall(bytes)
    new_image = sock.recv(10000)
    new_file = open("new_image.png", 'wb')
    new_file.write(new_image)

    #im = cv2.imread("new_image.png",0)
    #cv2.imshow("grey", im)

    myfile.close()
    new_file.close()


finally:
    sock.close()