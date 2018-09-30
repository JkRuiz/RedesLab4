import socket
import json

#Función que recibe los mensajes que entran al socket.
def msgReceive(sock):
	data, addr = serverSocket.recvfrom(1024)
	return data

#Función que envia los datos.
def msgSend(msg, sock)
	serverSocket.sendto(msg, sock)

#Obtiene las propiedades del servidor del archivo configUDP.txt
def getProperties():
    with open('configUDP.txt', 'r') as file:
        properties = json.load(file)
    return properties

#Obtiene las propiesdades
properties = getProperties()
#Nombre del archivo que se va a enviar
fileName = properties['fileName']
#Numero de clientes a los que se escuchara
numeroClientes = int(['numberClients'])
#Numero de puerto que se utilizara
port= int (properties['serverPort'])
chunkSize = int(properties['chunkSize'])




#genera un socket UDP
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#la dirección y el puerto por donde el servidor va a escuchar
serverSocket.bind(('127.0.0.1', 9000))

i = 0
hay = True
while hay:
	#recibe los datos del socket y la dirección del cliente
	data, addr = serverSocket.recvfrom(1024)
	print (data.decode())
	#abre el archivo que el cliente envio
	f = open('randomText500.txt')

	outputData = f.read(1024)
	contador = 0
	while (outputData):
		serverSocket.sendto(outputData.encode(), addr)
		print(outputData)
		outputData = f.read(1024)
		i = i + 1
		print (i)

	outputData = "acabe"
	print(outputData)	
	i = i+1
	serverSocket.sendto(outputData.encode(), addr)
	print (i)
	data, addr = serverSocket.recvfrom(1024)
	print(data.decode())
	hay = False



