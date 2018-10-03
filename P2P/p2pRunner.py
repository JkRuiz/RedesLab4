import os

def run_client(ip, fileName):
	try :
		os.system('sshpass -p "labredesML340" ssh -o StrictHostKeyChecking=no isis@' + str(ip) + ' "rm RedesLab4/UDP/recepcion.txt"')
	except:
		print("Failed to remove at " + str(ip))
	os.system('sshpass -p "labredesML340" ssh -o StrictHostKeyChecking=no isis@' + str(ip) + ' "deluge-console add RedesLab4/P2P/' + fileName + '.torrent"')

def check_client()