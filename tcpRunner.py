import os
import paramiko
import json
from threading import Thread

def run_server():
	import tcpServer

def run_client(ip):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ip, username=properties['clientUsername'], password=properties['clientPassword'])
	ssh.exec_command('python3 tcpClient.py')
	ssh.close()

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