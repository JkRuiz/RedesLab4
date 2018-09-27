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
hasheado = s.recv(buffersize).decode('utf-8')
hasher = hashlib.md5()

with open('received_file', 'wb') as f:
    print ('file opened')
    while True:
        print('receiving data...')
        data = s.recv(buffersize)
        hasher.update(data)
        if not data:
            break
        print('data=%s', (data))
        print('----------')
        # write data to a file
        f.write(data)
hasheado2 = hasher.hexdigest() + '\r\n'
if (hasheado == hasheado2):
    print('Se recibio el archivo exitosamente')
else:
    print('No se recibio el archivo correctamente')

tiempoTotal = time.time() - float(tiempoLlegada)
print(' Tiempo total en segundos: ', tiempoTotal)
f.close()
print('Successfully get the file')
s.close()
print('connection closed')
