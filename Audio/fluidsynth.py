import sys
import time
from socket import *
serverHost = "localhost"
serverPort = 9800
s = socket(AF_INET, SOCK_STREAM)
s.connect((serverHost, serverPort))
s.send(("noteon 1 100 120 \n").encode())
time.sleep(1)
s.send(("noteoff 1 46 \n noteoff 1 49 \n noteoff 1 53 \n").encode())
s.send(("quit\n").encode())
data = s.recv(1024)
print(data)