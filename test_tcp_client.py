import socket
import sys
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.1.143', 20000))
sock.send(bytes("Hello I'm Client.\r\n", 'UTF-8'))
print(sock.recv(1024))
sock.send(bytes("I Have no dick.\r\n", 'UTF-8'))
print(sock.recv(1024))
#sock.close()
while True:
    time.sleep(5)
    print('5 seconds wait')
