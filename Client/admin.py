import socket
import os
import time
import sys

s = socket.socket()
s.connect(("localhost",int(sys.argv[1])))

k = 1

s.send(str(k))

print "Connecting as admin"

print "Enter the resource you want to check status"
j = raw_input()
s.send(j)
k = s.recv(1024)
print k
	
	
s.close()
