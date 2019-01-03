import socket
import numpy as np
import scipy as sp
import scipy.ndimage

import Image

import matplotlib.pyplot as plt

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
filename='l.jpg'
f = open(filename,'rb')
l = f.read(BUFFER_SIZE)
while (l):
       s.send(l)
       #print('Sent ',repr(l))
       l = f.read(BUFFER_SIZE)
       if not l:
           f.close()
           s.close()
           break
s.close()
