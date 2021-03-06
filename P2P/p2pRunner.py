import os
import subprocess   
import json
import smtplib
import datetime
import time
from threading import Thread
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

#Extract properties 
def getProperties():
    with open('configP2P.json', 'r') as file:
        properties = json.load(file)
    return properties

def run_torrent(torrentName):
    os.system('deluged')
    time.sleep(5)
    os.system('deluge-console add ' + torrentName)

def unlink_torrent(fileName):
    os.system('deluge-console rm ' + fileName)
    os.system('rm /home/maro96leon/Downloads/*')

def check_status():
    status = subprocess.check_output("deluge-console info", shell=True).decode()
    if "Seeding" not in status:
        return False
    return True

def gitUpdate():
    os.system('git pull')

def logStartNetstat(i, n):
    os.system("netstat -s | grep segments >> Logs/Netstat_T" + str(n) + "_C" + str(i) + "_Start.log")

def logEndNetstat(i, n):
    os.system("netstat -s | grep segments >> Logs/Netstat_T" + str(n) + "_C" + str(i) + "_End.log")

def handleIfTop(t, i, n):
    os.system("sudo iftop -t -s " + str(t) + " >> Logs/P2P_T" + str(n) + "_C" + str(i) + "_traffic.log")

def makeDirFile():
    os.system('rm -rf Logs')
    os.system('mkdir Logs')

def sout(l):
    log.write(l + '\n')
    log.flush()
    print(l)

def getId():
    with open('id','r') as f:
        nId = json.load(f)['id']
    return nId

def send_mail_gmail(username,password,sender,toaddrs_list,msg_text,subject,attachment_path_list):
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.starttls()
    s.login(username, password)
    #s.set_debuglevel(1)
    msg = MIMEMultipart()
    recipients = toaddrs_list
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    if attachment_path_list is not None:
        for each_file_path in attachment_path_list:
            try:
                file_name=each_file_path.split("/")[-1]
                part = MIMEBase('application', "octet-stream")
                part.set_payload(open(each_file_path, "rb").read())

                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment' ,filename=file_name)
                msg.attach(part)
            except:
                print("could not attach file")
    msg.attach(MIMEText(msg_text,'html'))
    s.sendmail(sender, recipients, msg.as_string())

gitUpdate()
makeDirFile()
properties = getProperties()
i = getId()
print("Running client #" + i)
t = properties['runtime']
n = properties['numberClients']
unlink_torrent(properties['fileName'])
thread = Thread(target=handleIfTop, args=[t, i, n])
with open('Logs/P2P_T' + str(n) + "_C" + str(i) + ".log", 'w') as log:
    thread.start()
    logStartNetstat(i, n)
    run_torrent(properties['torrentName'])
    tStart = datetime.datetime.now()
    done = False
    while not done:
        done = check_status()
    summary = str(datetime.datetime.now() - tStart) + "s"
    logEndNetstat(i, n)
    sout("C: Transfered in " + summary)
thread.join()
unlink_torrent(properties['fileName'])
logs = ['Logs/P2P_T' + str(n) + "_C" + str(i) + ".log",
"Logs/P2P_T" + str(n) + "_C" + str(i) + "_traffic.log",
"Logs/Netstat_T" + str(n) + "_C" + str(i) + "_End.log",
"Logs/Netstat_T" + str(n) + "_C" + str(i) + "_Start.log"]
send_mail_gmail(properties['email'], properties['passwd'],properties['email'],properties['dest'],
"Working OK", "Logs for T" + str(n) + " C" + str(i) + " " + properties['fileName'], logs)
