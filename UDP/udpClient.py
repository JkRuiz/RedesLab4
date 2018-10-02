import socket

#genera un socket UDP
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#direccion del servidor
serverAdr = ('localhost', 9000)
#envia mensaje al servidor
cliente.sendto('status OK'.encode(), serverAdr)

#booleano que determina se ya se termino de recivir el archivo
hay = True
#guarda el mensaje a medida que va llegando
mensajeTotal = ""
#contador de paquetes que recibe
i = 0
#Abre el archivo que va a guardar la información recibida
f = open('recepción.txt', 'a')
#while para recibir y enviar mensajes
while hay:
	#envia mensaje al servidor
	message, addrSerer = cliente.recvfrom(1024)
	#recibe el mensaje y lo guarda en la
	if 'END_OF_FILE' not in message.decode():
		#se incrementa el numero de paquetes recibidos
		i = i +1
		#se añade el mensaje que llego al que ya había
		mensajeTotal = mensajeTotal + message.decode()
		print(mensajeTotal)
	#Si el mensaje contiene "acabe" se cambia ha false la variable booleana y se incrementa el numero de paquetes
	else:
		#cambio de la variable
		hay = False
		#Incrementa el número de paquetes
		i = i + 1 
#Escribe el archivo.
f.write(mensajeTotal)
#Cierra el archivo.
f.close()
#print(mensajeTotal)
#print (i)
no = False
while (not no):
	cliente.sendto(str(i).encode(), serverAdr)
	message, addrSerer = cliente.recvfrom(1024)
	if (message == "OK"):
		no = True
