#!/usr/bin/env python

import random
import socket, select
from time import gmtime, strftime
from random import randint
import sys
import time

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

    size = len(bytes)
    print(size)

    sock.sendall(str(size).encode())

    answer = (sock.recv(4096)).decode()
    print(answer)

    if answer is "1":
        print("Received 1")
        sock.sendall(bytes)
        new_file = open("new_image.png", 'wb')

        new_image = sock.recv(4*size)
        new_file.write(new_image)

    #im = cv2.imread("new_image.png",0)
    #cv2.imshow("grey", im)
    myfile.close()
    new_file.close()


finally:
    sock.close()
