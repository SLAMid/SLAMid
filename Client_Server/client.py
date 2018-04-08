#!/usr/bin/env python

import random
import socket, select
from time import gmtime, strftime
from random import randint
import sys
import cv2
import matplotlib as plt
import matplotlib.image as mpimg

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

    # send image size to server
    # sock.sendall("SIZE %s" % size)
    #sock.send(size.encode())
    sock.sendall(bytes)
    print("Sent image")

    with open("tmp_client.png", 'wb') as f:
        while True:
            data = sock.recv(1024)
            if data:
                print("Receiving data...")
                f.write(data)
            else:
                break
    f.close()
    print("Received image")

    #print 'answer = %s' % answer

    # send image to server
    # if answer == 'GOT SIZE':
    #     sock.sendall(bytes)
    #     new_image = sock.recv(4*size)

    #     new_file = open("new_image.png", 'wb')
    #     new_file.write(new_image)

    #     #im = cv2.imread("new_image.png",0)
    #     #cv2.imshow("grey", im)

    # myfile.close()

finally:
    sock.close()