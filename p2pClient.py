import socket
import time
import hashlib
import json
from threading import Thread

def pearManager(conn):
	table = conn.recv(chunkSize).decode('utf-8')
	print(table)


def getProperties():
	with open('configP2P.ini', 'r') as file:
		properties = json.load(file)
	return properties

properties = getProperties()
print(properties[''])
chunkSize = int(properties['chunkSize'])
sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
