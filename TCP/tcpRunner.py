import os
import paramiko
import json
from threading import Thread

def run_server():
	import tcpServer

def run_cmd(chan, cmd):
    stdin = chan.makefile('wb')
    stdin.write(cmd + '\n')
    stdin.flush()

def run_client(id):
	os.system('ClientBashFiles/StartC' + str(id) + '.sh')

def getProperties():
    with open('configTCP.txt', 'r') as file:
        properties = json.load(file)
    return properties

def email():
	print('Done with test!!')

properties = getProperties()
os.system('./setupTCP.sh')
serverThread = Thread(target=run_server)
serverThread.start()

numberClients = int(properties['numberClients'])
for i in range(numberClients):
	t = Thread(target=run_client, args=[i])
	t.start()

serverThread.join()
email()