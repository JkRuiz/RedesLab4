# client.py
import json
import time
import socket
import hashlib


def msgSend(msg, sock):
    size = len(msg)
    #print('EL SIZE AL ENVIAR UN MENSAJE NO ENCODE ES : ', size)
    if len(str(size)) <= 4:
        first = str('0' * (4 - len(str(size))))
        finalMsg = str(first) + str(size) + str(msg)
    #print('EL MENSAJE ES : ', finalMsg)
    sock.send(finalMsg.encode())


def msgReceive(sock):
    size = sock.recv(4).decode()
    if size == '':
        return ''
    #print(' EL SIZE DEL CHUNK ES : ', (size))
    data = sock.recv(int(size)).decode()
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
