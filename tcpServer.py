import socket
import time
import hashlib
from threading import Thread


def threaded_function(conn, addr):
    print ('Got connection from', addr)
    data = conn.recv(buffersize).decode('utf-8')
    print('Server received', repr(data))
    conn.send(str(time.time()).encode('utf-8'))
    filename = 'mytext.txt'
    f = open(filename, 'rb')
    l = f.read(buffersize)
    while (l):
        conn.send(l)
        print('Sent ', repr(l))
        l = f.read(buffersize)
    f.close()
    print('Done sending')
    conn.close()


numberClients = 2
port = 60000
buffersize = 1024
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
serverSocket.bind((host, port))  # Bind to the port
serverSocket.listen(1)  # Now wait for client connection.
print ('Server listening....')
threads = []

for i in range(numberClients):
    conn, addr = serverSocket.accept()  # Establish connection with client.
    thread = Thread(target=threaded_function, args=(conn, addr))
    thread.start()
    threads.append(thread)

for i in range(len(threads)):
    threads[i].join()
