import socket
import time
import hashlib
import datetime
import json
import time
from threading import Thread


def msgSend(msg, sock):
    size = utf8len(msg)
    #print('EL SIZE AL ENVIAR UN MENSAJE NO ENCODE ES : ', size)
    if len(str(size)) <= 4:
        print('SIZE MODIFIED')
        first = str('0' * (4 - len(str(size))))
        finalSize = str(first) + str(size)
    print('EL SIZE ES : ', finalSize.encode())
    print('EL MENSAJE ES : ', str(msg).encode('utf-8'))
    sock.sendall(finalSize.encode())
    sock.sendall(str(msg).encode('utf-8'))

def utf8len(s):
    return len(s.encode('utf-8'))

def msgReceive(sock):
    size = sock.recv(4).decode()
    if size == '':
        return ''
    #print(' EL SIZE DEL CHUNK ES : ', (size))
    data = recvall(sock, int(size)).decode('utf-8')
    return data

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = ''
    while utf8len(data) < n:
        packet = sock.recv(n - utf8len(data))
        if not packet:
            return None
        print("Packet  == ", str(packet))
        data += str(packet)
    return data


def threaded_function(conn, addr, id):
    start = datetime.datetime.now()
    sout("C" + str(id) + ": Connection started at " + str(start))
    data = msgReceive(conn)
    sout("C" + str(id) + ": " + data)

    rsp = "Sending " + fileName
    sout("S: " + rsp + " to C" + str(id) + " with IP " + addr[0])
    msgSend(rsp, conn)

    f = open(fileName, 'r')
    l = f.read(chunkSize)
    while (l):
        #print('EL VALOR DE L ES : ' , l)
        msgSend(l, conn)
        l = f.read(chunkSize)
    f.close()

    with open(fileName, 'r') as afile:
        buf = afile.read()
        hasher.update(buf)
    hasheado = hasher.hexdigest()
    sout("S: END_OF_FILE")
    msgSend(('END_OF_FILE ' + hasheado), conn)
    sout("S: MD5Hash " + hasheado)

    asw = msgReceive(conn)
    sout("C" + str(id) + ": " + asw)
    summary = str(datetime.datetime.now() - start) + "s"
    sout("C" + str(id) + ": Transfered in " + summary)
    conn.close()

def getProperties():
    with open('configTCP.txt', 'r') as file:
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
logPrefix = properties['logPrefix'] + str(numberClients) + "_" + str(time.time()) + ".log"

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
serverSocket.bind(('', port))  # Bind to the port
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


