import os
import paramiko
import json
import time
from threading import Thread

def run_server():
	os.system('python3.6 udpServer.py')

def run_client(ip):
	try :
		os.system('sshpass -p "labredesML340" ssh -o StrictHostKeyChecking=no isis@' + str(ip) + ' "rm RedesLab4/UDP/recepcion.txt"')
		os.system('sshpass -p "labredesML340" ssh -o StrictHostKeyChecking=no isis@' + str(ip) + ' "rm RedesLab4/UDP/*.log"')
	except:
		print("Failed to remove at " + str(ip))
	os.system('sshpass -p "labredesML340" ssh -o StrictHostKeyChecking=no isis@' + str(ip) + ' "python3 RedesLab4/UDP/udpClient.py"')

def getProperties():
    with open('configUDP.txt', 'r') as file:
        properties = json.load(file)
    return properties

def killIptraf():
	os.system("kill $(ps aux | grep 'iptraf' | awk '{print $2}')")

def logStartNetstat(n):
	os.system("netstat -s >> Logs/Netstat_UDP_C" + str(n) + "_Start.log")

def logEndNetstat(n):
	os.system("netstat -s >> Logs/Netstat_UDP_C" + str(n) + "_End.log")

def startIptraf(n):
	os.system("sudo iptraf -i eth0 -L /home/s2g4/RedesLab4/UDP/Logs/UDP_C" + str(n) + "_traffic.log -B")

def makeDirFile():
	os.system('mkdir Logs')
	os.system('mkdir clientLogs')

def logFileStatus(ip, i, n):
	os.system('sshpass -p "labredesML340" ssh -o StrictHostKeyChecking=no isis@' + str(ip) + ' "ls -l RedesLab4/UDP/" >> clientLogs/UDP_T' + str(n) + '_C' + str(i) + '.log')

def runTest(n):
	properties = getProperties()
	numberClients = int(properties['numberClients'])
	startIptraf(numberClients)
	time.sleep(1)
	serverThread = Thread(target=run_server)
	listOfIPs = properties['clientIPs']
	serverThread.start()
	time.sleep(1)
	for i in range(numberClients):
		t = Thread(target=run_client, args=[listOfIPs[i]])
		t.start()
	serverThread.join()
	killIptraf()
	for i in range(numberClients):
		logFileStatus(listOfIPs[i], i, n)

def swapProperties(n):
	with open('configUDP.txt', 'r') as file:
		tmp = json.load(file)
		tmp['numberClients'] = int(n)
	with open('configUDP.txt', 'w') as file:
		file.write(json.dumps(tmp))

p = getProperties();
nClients = p['nClients']
makeDirFile()
for i in nClients:
	logStartNetstat(i)
	print('Running client #', str(i))
	swapProperties(i)
	runTest(i)
	logEndNetstat(i)
	time.sleep(10)