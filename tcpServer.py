import socket
import time
import hashlib
from threading import Thread


def threaded_function(conn):
    data = conn.recv(buffersize).decode('utf-8')
    print('Server received', repr(data))
    conn.send(str(time.time()).encode('utf-8'))
    with open(filename, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    hasheado = hasher.hexdigest() + '\r\n'
    conn.send(hasheado.encode('utf-8'))
    f = open(filename, 'rb')
    l = f.read(buffersize)
    while (l):
        conn.send(l)
        print('Sent ', repr(l))
        l = f.read(buffersize)
    f.close()
    print('Done sending')
    conn.close()


filename = 'mytext.txt'
numberClients = 1
port = 60000
buffersize = 1024
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
serverSocket.bind((host, port))  # Bind to the port
serverSocket.listen(1)  # Now wait for client connection.
print ('Server listening....')
threads = []
j = 0
conns = []
hasher = hashlib.md5()

while j < numberClients:
    conn, addr = serverSocket.accept()
    conns.append(conn)
    j += 1

for i in range(numberClients):
    thread = Thread(target=threaded_function, args=(conns[i],))
    thread.start()
    threads.append(thread)

for i in range(len(threads)):
    threads[i].join()
