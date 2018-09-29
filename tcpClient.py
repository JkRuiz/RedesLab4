# client.py
import json
import time
import socket
import hashlib


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
    data = b''
    while utf8len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data


properties = getProperties()
host = str(properties['serverIp'])
port = int(properties['serverPort'])
chunkSize = int(properties['chunkSize'])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
statusOk = 'STATUS_OK'
fileOk = 'FILE_OK'
fileError = 'FILE_ERROR'
endFile = 'END_OF_FILE'

s.connect((host, port))
msgSend(statusOk, s)
fileName = msgReceive(s)
hasher = hashlib.md5()

#print('Valor del filename: ', fileName)

with open('received_file', 'w') as f:
    while True:
        print('receiving data...')
        data = msgReceive(s)
        #print('DATO : ', data)
        final = data.split(' ')
        if final[0].strip() == endFile:
            hasheado = final[1]
            break
        if data == '':
            break
        hasher.update(data.encode())
        # write data to a file
        # f.write(data)
f.close()

hasheado2 = hasher.hexdigest()
if (hasheado.strip() == hasheado2.strip()):
    msgSend(fileOk, s)
else:
    msgSend(fileError, s)
s.close()

print('connection closed')
