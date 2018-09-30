import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAdr = ('localhost', 9000)

cliente.sendto('status OK'.encode(), serverAdr)

hay = True
mensajeTotal = ""
i = 0
while hay:

	message, addrSerer = cliente.recvfrom(1024)

	if "acabe" not in message.decode():

		i = i +1
		mensajeTotal = mensajeTotal + message.decode()

	else:

		hay = False
		i = i + 1 

print(mensajeTotal)
print (i)
cliente.sendto(str(i).encode(), serverAdr)