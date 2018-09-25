# client.py
import time
import socket
import hashlib

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
host = socket.gethostname()   # Get local machine name
port = 60000                  # Reserve a port for your service.
buffersize = 1024

s.connect((host, port))
message = 'Hellooo servercito'
s.send(message.encode('utf-8'))
tiempoLlegada = s.recv(buffersize)

with open('received_file', 'wb') as f:
    print ('file opened')
    while True:
        print('receiving data...')
        data = s.recv(buffersize)
        print('data=%s', (data))
        print('----------')
        if not data:
            break
        # write data to a file
        f.write(data)
tiempoTotal = time.time() - float(tiempoLlegada)
print('TIEMPO TOTAL DE : ', tiempoTotal, ' SEGUNDOS ')
f.close()
print('Successfully get the file')
s.close()
print('connection closed')
