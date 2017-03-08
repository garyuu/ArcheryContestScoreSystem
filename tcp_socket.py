'''
Author: Garyuu
Date:   2017/2/4
Name:   tcp_socket
Descr.: The port that communicate with other devices.
'''
import socket
import sys
import threading
import json

class SocketManager:
    def __init__(self, port, max_client):
        self.message_buffer = []
        self.socket_stack = {}
        self.buffer_lock = threading.Lock()
        self.max_client = max_client
        # Create socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('192.168.1.128', port))

    def send(self, message):
        self.socket_stack[int(message['machine'])].send(json.dumps(message).encode("UTF-8"))

    def start(self):
        self.server_socket.listen(self.max_client)
        threading.Thread(target = self.main_tread).start()

    def main_tread(self):
        while True:
            (client_socket, address) = self.server_socket.accept()
            print("Client connected from {}.".format(address))
            threading.Thread(target = self.socket_thread_function, args = (client_socket,)).start()

    def push_message(self, message):
        self.buffer_lock.acquire()
        self.message_buffer.append(message)
        self.buffer_lock.release()

    def pop_message(self):
        self.buffer_lock.acquire()
        if len(self.message_buffer):
            result = self.message_buffer[0]
            del self.message_buffer[0]
        else:
            result = False
        self.buffer_lock.release()
        return result

    def socket_thread_function(self, socket):
        size = 1024
        while True:
            try:
                data = socket.recv(size)
                print(data)
                if data:
                    message = json.loads(data.decode("UTF-8"))
                    print(message)
                    self.socket_stack[message['machine']] = socket
                    self.push_message(message)
                else:
                    raise error('Client disconnected')
            except:
                print('Client closed')
                socket.close()
                return False

def __message_graber(sockmng):
    while True:
        msg = sockmng.pop_message()
        if msg:
            print(msg[1])
            sockmng.send(msg[0], "Server Response".encode("UTF-8"))

if __name__ == '__main__':
    sockmng = SocketManager(20000, 40)
    threading.Thread(target = __message_graber, args = (sockmng,)).start()
    sockmng.start()
    while True:
        pass    

