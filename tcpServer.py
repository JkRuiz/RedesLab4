import socket
import time
import hashlib
import datetime
import json
from threading import Thread


def threaded_function(conn, addr, host):
    with open(addr + "_" + host + logPrefix, 'w') as log:
        log.write("Connection started at: " + datetime.datetime.now().time())
        data = conn.recv(buffersize).decode('utf-8')
        print('Server received', repr(data))
        log.write("C:" +  data.decode())
        
        conn.send(str(time.time()).encode('utf-8'))
        with open(fileName, 'rb') as afile:
            buf = afile.read()
            hasher.update(buf)
        hasheado = hasher.hexdigest() + '\r\n'
        conn.send(hasheado.encode('utf-8'))
        f = open(fileName, 'rb')
        l = f.read(buffersize)
        while (l):
            conn.send(l)
            print('Sent ', repr(l))
            l = f.read(buffersize)
        f.close()

        print('Done sending')
        conn.close()

def getProperties():
    with open('configTCP.ini', 'r') as file:
        properties = json.load(file)
    return properties

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
print ('Server listening....')

threads = []
j = 0
hasher = hashlib.md5()
print('out')
for j in range(numberClients):
    print('in')
    conn, addr = serverSocket.accept()
    print('Server adopted connection #' + j)
    thread = Thread(target=threaded_function, args=(conn, addr, socket.gethostname()))
    thread.start()
    threads.append(thread)

for i in range(len(threads)):
    threads[i].join()
