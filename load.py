import os
import json

def loadData():
	with open('/config.json', 'r') as f:
		clients = json.load(f)
	return clients

def copy_to_client(addr):
	os.system('sshpass -p "' + properties['clientPassword'] + '"" ssh -o StrictHostKeyChecking=no ' + properties['clientUsername'] + '@' + addr + ' "rm RedesLab4"')
	os.system('sshpass -p "' + properties['clientPassword'] + '"" ssh -o StrictHostKeyChecking=no ' + properties['clientUsername'] + '@' + addr + ' "rm R_*"')
	os.system('sshpass -p "' + properties['clientPassword'] + '"" ssh -o StrictHostKeyChecking=no ' + properties['clientUsername'] + '@' + addr + ' "git clone https://github.com/JkRuiz/RedesLab4"')

clients = loadData()
clientIPs = clients['clientIPs']
for ip in clientIPs:
	copy_to_client(ip)
