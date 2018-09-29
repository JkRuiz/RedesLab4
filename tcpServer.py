import socket
import time
import hashlib
import datetime
import json
import time
from threading import Thread


def mesgSend(msg, sock):
    size = len(msg)
    #print('EL SIZE AL ENVIAR UN MENSAJE NO ENCODE ES : ', size)
    if len(str(size)) <= 4:
        first = str('0' * (4 - len(str(size))))
        finalMsg = str(first) + str(size) + str(msg)
    #print('EL MENSAJE ES : ', finalMsg)
    sock.send(finalMsg.encode())


def recive(sock):
    size = sock.recv(4).decode()
    if size == '':
        return ''
    #print(' EL SIZE DEL CHUNK ES : ', (size))
    data = sock.recv(int(size) + 3).decode()
    return data


def threaded_function(conn, addr, id):
    start = datetime.datetime.now()
    sout("C" + str(id) + ": Connection started at " + str(start))
    data = recive(conn)
    sout("C" + str(id) + ": " + data)

    rsp = "Sending " + fileName
    sout("S: " + rsp + " to C" + str(id) + " with IP " + addr[0])
    mesgSend(rsp, conn)

    f = open(fileName, 'rb')
    l = f.read(chunkSize)
    while (l):
        print('EL VALOR DE L ES : ' , l)
        mesgSend(l, conn)
        l = f.read(chunkSize)
    f.close()

    with open(fileName, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    hasheado = hasher.hexdigest()
    sout("S: END_OF_FILE")
    mesgSend(('END_OF_FILE ' + hasheado), conn)
    sout("S: MD5Hash " + hasheado)

    asw = recive(conn)
    sout("C" + str(id) + ": " + asw)
    summary = str(datetime.datetime.now() - start) + "s"
    sout("C" + str(id) + ": Transfered in " + summary)
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
logPrefix = properties['logPrefix'] + str(numberClients) + "_" + str(time.time()) + ".txt"

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
serverSocket.bind((host, port))  # Bind to the port
serverSocket.listen(numberClients)  # Now wait for client connection.

with  open((logPrefix), 'w') as log:
	sout('Server listening....')
	tStart = datetime.datetime.now()

	threads = []
	hasher = hashlib.md5()
	for j in range(numberClients):
	    conn, addr = serverSocket.accept()
	    sout('Server adopted connection #' + str(j+1))
	    thread = Thread(target=threaded_function, args=(conn, addr, j+1))
	    thread.start()
	    threads.append(thread)

	for i in range(len(threads)):
	    threads[i].join()

	summary = str(datetime.datetime.now() - tStart) + "s"
	sout("S: Transfered in " + summary)


