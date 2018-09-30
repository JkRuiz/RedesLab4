import os
import paramiko
import json
import time
from threading import Thread

def run_server():
	import tcpServer

def run_cmd(chan, cmd):
    stdin = chan.makefile('wb')
    stdin.write(cmd + '\n')
    stdin.flush()

def run_client(ip):
	os.system('sshpass -p "labredesML340" ssh -o StrictHostKeyChecking=no isis@' + ip + ' "rm R_*"')
	os.system('sshpass -p "labredesML340" ssh -o StrictHostKeyChecking=no isis@' + ip + ' "python3 RedesLab4/TCP/tcpClient.py"')

def getProperties():
    with open('configTCP.json', 'r') as file:
        properties = json.load(file)
    return properties

def killIptraf():
	os.system("kill $(ps aux | grep 'iptraf' | awk '{print $2}')")

def startIptraf(n):
	os.system("sudo iptraf -i eth0 -L /home/s2g4/RedesLab4/TCP/Logs/TCP_C" + str(n) + "_traffic.log -B")

def runTest():
	properties = getProperties()
	numberClients = int(properties['numberClients'])
	startIptraf(numberClients)
	time.sleep(1)
	serverThread = Thread(target=run_server)
	serverThread.start()
	for i in range(numberClients):
		t = Thread(target=run_client, args=[i+1])
		t.start()
	serverThread.join()
	killIptraf()

def swapProperties(n):
	with open('configTCP.json', 'r') as file:
		properties = json.load(file)
		properties['numberClients'] = int(n)
	with open('configTCP.json', 'w') as file:
		file.write(json.dumps(properties))
	return properties

properties = getProperties();
nClients = properties['nClients']
for i in nClients:
	swapProperties(i)
	runTest()



