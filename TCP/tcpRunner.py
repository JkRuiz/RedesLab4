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
	os.system('sshpass -p "labredesML340" ssh -o StrictHostKeyChecking=no isis@' + str(ip) + ' "rm R_*"')
	os.system('sshpass -p "labredesML340" ssh -o StrictHostKeyChecking=no isis@' + str(ip) + ' "python3 RedesLab4/TCP/tcpClient.py"')

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
	listOfIPs = properties['clientIPs']
	serverThread.start()
	for i in range(numberClients):
		t = Thread(target=run_client, args=[listOfIPs[i]])
		t.start()
	serverThread.join()
	killIptraf()

def swapProperties(n):
	with open('configTCP.json', 'r') as file:
		tmp = json.load(file)
		tmp['numberClients'] = int(n)
	with open('configTCP.json', 'w') as file:
		file.write(json.dumps(tmp))

p = getProperties();
nClients = p['nClients']
for i in nClients:
	print('Running client #', str(i))
	swapProperties(i)
	runTest()
	time.sleep(10)



