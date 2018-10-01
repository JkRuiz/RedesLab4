import socket
import json
import time
from threading import Thread

#Obtiene las propiedades del servidor del archivo configUDP.txt
def getProperties():
    with open('configUDP.txt', 'r') as file:
        properties = json.load(file)
    return properties
def threaded_function(id, addr):
	print(id)
	#contador de paquetes
	i = 0
	#booleano para saber hasta cuando debe seguir activo el while.
	hay = True
	#recepción y envio de mensajes.
	while hay:
		
		#abre el archivo que el cliente envio.
		f = open(fileName)
		#
		outputData = " "
		#while para el envio del archivo.
		while (outputData):
			#chunk de información que se enviara. 
			outputData = f.read(chunkSize)
			#envio de l segmento del archivo.
			serverSocket.sendto(outputData.encode(), addr)
			#imprime la información enviada.
			#print(outputData)
			#aumenta el contador de paquetes enviados.
			i = i + 1
			#imprime el contador.
			#print (i)
		#cierra el archivo.
		f.close()
		#envia mensaje para que el cliente sepa que se termino la transmicion.
		outputData = "acabe"
		#imprime el mensaje de terminar.
		#print(outputData)	
		#aumenta el contador de paquetes.
		i = i+1
		#envia el mensaje de termino.
		serverSocket.sendto(outputData.encode(), addr)
		#imprime el contador de mensajes.
		#print (i)
		# recive el numero de pauqetes recibidos.
		data, addr = serverSocket.recvfrom(1024)
		#imprime el numero de paquetes enviados.
		#print(data.decode())
		#indica la terminación del while.
		hay = False

#Obtiene las propiesdades.
properties = getProperties()
#Nombre del archivo que se va a enviar.
fileName = properties['fileName']
#Numero de clientes a los que se escuchara.
numeroClientes = int(properties['numberClients'])
#Numero de puerto que se utilizara.
port= int (properties['serverPort'])
#Tamaño de los paquetes que se van a usar.
chunkSize = int(properties['chunkSize'])
#Genera el log de la transacción.
logPrefix = properties['logPrefix'] + str(numeroClientes) + "_" + str(time.time()) + ".log"


#genera un socket UDP.
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#Obtiene el hostname sobre el que se ejecuta el programa.
host = socket.gethostname()
#la dirección y el puerto por donde el servidor va a escuchar.
serverSocket.bind(('', port))

#arreglo de threads
threads = []

j = 1
while j <= numeroClientes:

		#recibe los datos del socket y la dirección del cliente.
		data, addr = serverSocket.recvfrom(1024)
		print (data.decode())
		if (data):
			thread = Thread(target=threaded_function, args=(j, addr))
			thread.start()
			threads.append(thread)
#for que sincroniza los threads.
for i in range(len(threads)):
	threads[i].join() 





