import socket
import time
import hashlib
import datetime
import json
from threading import Thread


def threaded_function(conn, addr, id):
    sout("C" + str(id) + ": Connection started at: " + str(datetime.datetime.now()), id)
    data = conn.recv(chunkSize).decode('utf-8')
    sout("C" + str(id) + ": " + data, id)

    rsp = "Sending " + fileName
    sout("S: " + rsp)
    conn.send()

    conn.send(str(time.time()).encode('utf-8'))
    with open(fileName, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    hasheado = hasher.hexdigest() + '\r\n'
    conn.send(hasheado.encode('utf-8'))
    f = open(fileName, 'rb')
    l = f.read(chunkSize)
    while (l):
        conn.send(l)
        print('Sent ', repr(l))
        l = f.read(chunkSize)
    f.close()

    print('Done sending')
    conn.close()

def getProperties():
    with open('configTCP.ini', 'r') as file:
        properties = json.load(file)
    return properties

def sout(l):
	log.write(l + '\n')
	print(l)

properties = getProperties()
fileName = properties['fileName']
numberClients = int(properties['numberClients'])
port = int(properties['serverPort'])
chunkSize = int(properties['chunkSize'])
logPrefix = properties['logPrefix'] + str(numberClients) + ".txt"

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
serverSocket.bind((host, port))  # Bind to the port
serverSocket.listen(numberClients)  # Now wait for client connection.

with  open((logPrefix), 'w') as log:
	sout('Server listening....')

	threads = []
	hasher = hashlib.md5()
	for j in range(numberClients):
	    conn, addr = serverSocket.accept()
	    sout('Server adopted connection #' + str(j))
	    thread = Thread(target=threaded_function, args=(conn, addr, j))
	    thread.start()
	    threads.append(thread)

	for i in range(len(threads)):
	    threads[i].join()
