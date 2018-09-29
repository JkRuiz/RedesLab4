# client.py
import json
import time
import socket
import hashlib


def msgSend(msg, sock):
    size = len(msg)
    if len(str(size)) <= 4:
        #gprint('SIZE MODIFIED')
        first = str('0' * (4 - len(str(size))))
        finalSize = str(first) + str(size)
    #print('EL SIZE ES : ', finalSize.encode())
    #print('EL MENSAJE ES : ', str(msg).encode())
    sock.sendall(finalSize.encode())
    sock.sendall(str(msg).encode())

def msgReceive(sock):
    size = recvall(sock, 4).decode()
    if size == '':
        return ''
    data = recvall(sock, int(size)).decode()
    return data

def recvall(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        #print("Packet  == ", packet)
        data += packet
    return data

def getProperties():
    with open('configTCP.txt', 'r') as file:
        properties = json.load(file)
    return properties


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

with open("R_" + fileName, 'w') as f:
    i = 0
    while True:
        i+=1
        if i%100 == 0: print('receiving data...')
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
        f.write(data)
f.close()

hasheado2 = hasher.hexdigest()
if (hasheado.strip() == hasheado2.strip()):
    msgSend(fileOk, s)
else:
    msgSend(fileError, s)
s.close()

print('connection closed')
