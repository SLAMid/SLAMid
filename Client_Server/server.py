#!/usr/bin/env python

import random
import socket, select
from time import gmtime, strftime
import cv2

imgcounter = 1
basename = "image%s.png"

HOST = '127.0.0.1'
PORT = 6666
size = 0

connected_clients_sockets = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(10)

connected_clients_sockets.append(server_socket)

while True:

    read_sockets, write_sockets, error_sockets = select.select(connected_clients_sockets, [], [])

    for sock in read_sockets:

        if sock == server_socket:

            sockfd, client_address = server_socket.accept()
            connected_clients_sockets.append(sockfd)
            print("Connected with client {}".format(client_address))

        else:
            try:
                with open("tmp_server.png", 'wb') as f:
                    while True:
                        data = sock.recv(1024)
                        if data:
                            print("Receiving data...")
                            f.write(data)
                        else:
                            break
                f.close()
                print("Received image")

                #IMAGE MANIPULATION BEGINS HERE
                # print("Manipulating image")
                # imm = cv2.imread("temp_server.png")
                # imm = cv2.cvtColor(imm, cv2.COLOR_BGR2GRAY)
                # cv2.imwrite("temp_gray.png",imm)
                #AND ENDS HERE
                # print("Finished manipulating image")
                # myfile_gray = open("temp_gray.png", 'rb')
                # print("Sending image")
                # bytes = myfile_gray.read()
                # sock.sendall(bytes)
                # print("Finished sending image")
                # print("Closing socket")

                print("Sending file back")
                file_r = open("tmp_server.png", "rb")
                bytes = file_r.read()
                sock.sendall(bytes)
                sock.shutdown()

            except:
                print("No data received, closing socket")
                sock.close()
                connected_clients_sockets.remove(sock)
                print("Disconnected with client {}".format(client_address))
                continue
server_socket.close()
