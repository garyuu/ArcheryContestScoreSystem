'''
Author: Garyuu
Date:   2017/2/4
Name:   socket_manager
Descr.: The port that communicate with other devices.
'''
import socket
import sys
import threading
import json

class SocketManager:
    def __init__(self, port, max_client, on_message):
        self.on_message = on_message
        # Create socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('192.168.1.128', port))
        self.server_socket.setdefaulttimeout(10)
        self.main_thread = threading.Thread(target = self.main_thread_function)

    def __destroy__(self):
        self.server_socket.close()

    def start(self):
        self.server_socket.listen(self.max_client)
        self.main_thread.start()

    def main_thread_function(self):
        while True:
            try:
                (client_socket, address) = self.server_socket.accept()
                print("Client connected from {}.".format(address))
                threading.Thread(target = self.socket_thread_function, args = (client_socket,)).start()
            except:
                break

    def socket_thread_function(self, socket):
        size = 1024
        socket.setdefaulttimeout(10)
        while True:
            try:
                data = socket.recv(size)
                print(data)
                if data:
                    message = json.loads(data.decode("UTF-8"))
                    socket.send(json.dumps(self.on_message(message)))
                else:
                    raise error('Client disconnected')
            except:
                print('Client closed')
                socket.close()
                return False
