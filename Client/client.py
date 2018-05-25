import socket
import os
import time
import sys

import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
graph1 = fig.add_subplot(151)
graph2 = fig.add_subplot(152)
graph3 = fig.add_subplot(153)
graph4 = fig.add_subplot(154)
graph5 = fig.add_subplot(155)
attributes = ["Total Tasks","Running Tasks","User Processes","System Processes","Free Memory"]
i = 0
j = 0

def animate(i):
	recv = open('Received Files/recv0.txt','r+')
	recv.seek(0,0)
	l = []
	for line in recv.read().split('\n')[:5]:
		l.append(float(line.split()[-1]))
	graph1.clear()
	graph2.clear()
	graph3.clear()
	graph4.clear()
	graph5.clear()
	if(l[0]>250):
		graph1.bar([0],[l[0]],width=0.5,color='r')
	else:
		graph1.bar([0],[l[0]],width=0.5,color='g')
	if(l[1]>14):
		graph2.bar([0],[l[1]],width=0.5,color='r')
	else:
		graph2.bar([0],[l[1]],width=0.5,color='g')
	if(l[2]>1.5):
		graph3.bar([0],[l[2]],width=0.5,color='r')
	else:
		graph3.bar([0],[l[2]],width=0.5,color='g')
	if(l[3]>0.8):
		graph4.bar([0],[l[3]],width=0.5,color='r')
	else:
		graph4.bar([0],[l[3]],width=0.5,color='g')
	if(l[4]<150000):
		graph5.bar([0],[l[4]],width=0.5,color='r')
	else:
		graph5.bar([0],[l[4]],width=0.5,color='g')
	graph1.set_xticks([0.25])
	graph2.set_xticks([0.25])
	graph3.set_xticks([0.25])
	graph4.set_xticks([0.25])
	graph5.set_xticks([0.25])
	graph1.set_xticklabels([attributes[0]])
	graph2.set_xticklabels([attributes[1]])
	graph3.set_xticklabels([attributes[2]])
	graph4.set_xticklabels([attributes[3]])
	graph5.set_xticklabels([attributes[4]])
	graph1.set_ylim([0, 300])
	graph2.set_ylim([0, 20])
	graph3.set_ylim([0, 2])
	graph4.set_ylim([0, 1.5])
	graph5.set_ylim([0, 400000])


# id1 = os.fork()
# if(id1!=0):    # Parent Process
s = socket.socket()
s.connect(("localhost",int(sys.argv[1])))
k = 0
print "Connecting as user"

s.send(str(k))

#if(k==str(0)):
id1 = os.fork()
if(id1!=0):
	while(True):
		# Run command to check system specs and store in output.txt
		os.system('top -n 1 -b | head -n 10 > Sent\ Files/output'+ str(i)+ '.txt')

		f = open('Sent Files/'+'output'+str(i)+'.txt','r')
		recv = open('Received Files/'+'recv0.txt','r+')
		i += 1
		j += 1

		data = f.read() # can specify how much data of output is needed to be sent
		s.send(data)
		d = s.recv(1024)
		print(d)
		recv.write(d)
		recv.seek(0,0)
			# ani = animation.FuncAnimation(fig, animate, interval=1000)
			# plt.show()
		time.sleep(3) # sleep for 3 seconds
			# plt.close()
else:  # Child Process
 	ani = animation.FuncAnimation(fig, animate, interval=1000)
 	plt.show()
#else:
#	j = raw_input()
#	s.send(j)
#	k = s.recv(1024)
#	print k


s.close()
