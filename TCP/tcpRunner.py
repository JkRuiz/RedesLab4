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

def run_client(id):
	os.system('sshpass -p "labredesML340" ssh -o StrictHostKeyChecking=no isis@' + properties['clientIPs'][id-1] + ' "rm R_*"')
	os.system('ClientBashFiles/StartC' + str(id) + '.sh')

def getProperties():
    with open('configTCP.txt', 'r') as file:
        properties = json.load(file)
    return properties

def killIptraf():
	os.system("kill $(ps aux | grep 'iptraf' | awk '{print $2}')")

def startIptraf(n):
	os.system("sudo iptraf -i eth0 -L /home/s2g4/RedesLab4/TCP/TCP_C" + str(n) + "_traffic.log -B")

properties = getProperties()
numberClients = int(properties['numberClients'])
startIptraf(numberClients)
time.sleep(5)
serverThread = Thread(target=run_server)
serverThread.start()

for i in range(numberClients):
	t = Thread(target=run_client, args=[i+1])
	t.start()

serverThread.join()
killIptraf()