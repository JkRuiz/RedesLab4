import os
import paramiko
from threading import Thread

def run_server():
	import tcpServer

def run_client(ip):
	serverSSH = paramiko.SSHClient()
	serverSSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	serverSSH.connect(ip, username=properties['clientUsername'], password=properties['clientPassword'])
	serverSSH.exec_command('./setupTCP.sh')


def getProperties():
    with open('configTCP.txt', 'r') as file:
        properties = json.load(file)
    return properties

properties = getProperties()
os.system('./setupTCP.sh')
serverThread = Thread(target=run_server)
serverThread.start()

numberClients = int(properties['numberClients'])
ips = properties['clientIPs']
for i in range(numberClients):
	run_client(ips[i])

serverThread.join()
print('Done with test!!')