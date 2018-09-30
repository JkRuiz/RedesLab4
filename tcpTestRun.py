import os
import paramiko
import json
import time

def getProperties():
    with open('configTCP.txt', 'r') as file:
        properties = json.load(file)
    return properties

def setupServer(ssh):
    #sudo iptraf -s eth0
    stdin, stdout, stderr = ssh.exec_command('sudo iptraf -s eth0')
    stdin.write(properties['suPassword'] + '\n')
    stdin.flush()
    time.sleep(1)
    print(stdout.read())
    stdin.flush()
    stdin.write('/home/s2g4/test_traffic.log\n')
    stdin.flush()

def shellSetup(ssh):
    chan = ssh.invoke_shell()

properties = getProperties()
serverSSH = paramiko.SSHClient()
serverSSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
serverSSH.connect(properties['serverIp'], username=properties['serverUsername'], password=properties['serverPassword'])
print('Login - OK')
setupServer(serverSSH)
serverSSH.close()
print('DONE')