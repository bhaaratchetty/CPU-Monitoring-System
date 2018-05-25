import socket
import sys
import thread
import psycopg2

ipnchar = ""
userp = ""
systemp = ""
totalm = ""
usedm = ""
freem = ""

def client_details():
	conn = None
	global ipnchar
	global userp
	global systemp
	global totalm
	global usedm
	global freem
	try:
	    conn = psycopg2.connect(host="localhost",database="monitoring",user="daniel",password="pwd")
	    cur = conn.cursor()
	    print('Database Connection Open')
	    cur.execute("""insert into cpu(ipnchar,userp,systemp) values(%s,%s,%s)""",(ipnchar,userp,systemp))
	    conn.commit()
	    print("Hello")
	    cur.execute("""insert into memory(ipnchar,totalm,usedm,freem) values(%s,%s,%s,%s)""",(ipnchar,totalm,usedm,freem))
	    cur.close()
	    conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
	    print(error)
	finally:
	    if conn is not None:
	        conn.close()
	        print('Database connection closed.')	


def query_details(tes):
	conn1 = None
	print(ipnchar)
	try:
		conn1 = psycopg2.connect(host="localhost",database="monitoring",user="daniel",password="pwd")
		cur = conn1.cursor()
		print('Database Connection Open')
		if(tes == "cpu"):
			cur.execute("select * from cpu;")
			conn.send(str(cur.fetchall()))
			conn1.commit()
			cur.close()
			#print("Hello")
		else:
			cur.execute("select * from memory;")
			conn.send(str(cur.fetchall()));
			conn1.commit()
			cur.close()
			
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn1 is not None:
			conn1.close()
			print('Database connection closed.')

def parseData(dataFile, toSendFile):
	global userp
	global systemp
	global totalm
	global usedm
	global freem
	l = []
	for line in dataFile:
		l.append(line.split())
	del l[0]
	l[0] = ["Tasks",l[0][1],l[0][3],l[0][5],l[0][7],l[0][9]]
	l[1] = ["CPU", l[1][1],l[1][3],l[1][5],l[1][7],l[1][9]]
	l[2] = ["Memory",l[2][3],l[2][5],l[2][7]]
	userp = l[1][1]
	systemp = l[1][2]
	totalm = l[2][1]
	usedm = l[2][2]
	freem = l[2][3]
	del l[3]
	del l[3]
	del l[3]
	l[3] = ["Process 1",l[3][0],l[3][1],l[3][8],l[3][9]]
	l[4] = ["Process 2",l[4][0],l[4][1],l[4][8],l[4][9]]
	del l[5]
	print(l)
	analyze(l, toSendFile)

s = socket.socket()
s.bind(("localhost",int(sys.argv[1])))
s.listen(10)
i = 0
j = 0

def analyze(l, toSendFile):
	for elem in l:
		if(elem[0] == "Tasks"):
			if(int(elem[1])>250):
				toSendFile.write("Too many Total Tasks: " + elem[1] + "\n")
			else:
				toSendFile.write("Total Number of Tasks is normal " + elem[1]+"\n")
			if(int(elem[2])>14):
				toSendFile.write("Too many running tasks: "+elem[2]+"\n")
			else:
				toSendFile.write("Number of running tasks is normal: "+ elem[2]+"\n")
		if(elem[0]=="CPU"):
			if(float(elem[1])>1.5):
				toSendFile.write("Too many user processes: "+elem[1] + "\n")
			else:
				toSendFile.write("Number of user processes is normal: " +elem[1]+"\n")
			
			if(float(elem[2])>0.8):
				toSendFile.write("Too many system processes: "+elem[2]+"\n")
			else:
				toSendFile.write("Number of system processes is normal: "+elem[2]+"\n")
		if(elem[0]=="Memory"):
			if(int(elem[1])-int(elem[3])<150000):
				toSendFile.write("Too much Memory usage. Memory left: "+str(int(elem[1])-int(elem[3])) + "\n")
			else:
				toSendFile.write("Normal Memory usage. Memory left: " + str(int(elem[1])-int(elem[3])) + "\n")
		 
	toSendFile.write("Current Processes\n")
	toSendFile.write("Process \t\t CPU % \t \t Memory usage\n")
	toSendFile.write("%s \t \t %s \t \t %s\n" %(l[3][2],l[3][3],l[3][4]))
	toSendFile.write("%s \t \t %s \t \t %s\n" %(l[4][2],l[4][3],l[4][4]))
	toSendFile.seek(0,0)

def get_usage(conn, addr):
	m = conn.recv(1024)
	if(m==str(0)):
		while(True):
			global ipnchar
			global i
			global j
			# sc,address = s.accept()
			# print(addr)
			ipnchar = str(addr[0])+":"+ str(addr[1])

			print("port number is : ",int(addr[1]))
			f = open('Received Files/'+'file_' + str(i) + '.txt','w+')
			toSendFile = open('Sent Files/'+'send_'+str(j)+'.txt','w+')
			i += 1
			j += 1
			l = conn.recv(1024)  # Will contain the entire data
			f.write(l)
			f.seek(0,0)
			parseData(f, toSendFile)
			client_details()
			data = toSendFile.read()
			print(data)
			conn.send(data)
			f.close()
			# sc.close()
	else:
		
			
		l = conn.recv(1024)
		query_details(l)
		

while True:
#Accepting incoming connections
    conn, addr = s.accept()
#Creating new thread. Calling clientthread function for this function and passing conn as argument.
    thread.start_new_thread(get_usage,(conn, addr)) #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.

s.close()	

