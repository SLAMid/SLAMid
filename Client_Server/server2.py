#!/usr/bin/env python

import random
import socket, select
from time import gmtime, strftime

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

        else:
            try:

                data = sock.recv(4096)
                print("Received %s" % data)

                if data:
                        myfile = open("temp.png", 'wb')
                        myfile.write(data)

                        data = sock.recv(5000)
                        if not data:
                            myfile.close()
                            break
                        myfile.write(data)
                        myfile.close()

                        #IMAGE MANIPULATION BEGINS HERE
                        #imm = cv2.imread("temp.png")
                        #imm = cv2.cvtColor(imm, cv2.COLOR_BGR2GRAY)
                        #cv2.imwrite("temp_gray.png",imm)
                        #AND ENDS HERE

                        myfile_gray = open("temp.png", 'rb')
                        bytes = myfile_gray.read()

                        sock.sendall(bytes)
                        sock.shutdown()
            except:
                sock.close()
                connected_clients_sockets.remove(sock)
                continue
server_socket.close()