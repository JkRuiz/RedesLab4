#!/bin/bash
##Enter Username and Password Details:
userName="isis"
password="labredesML340"

expect -c "
    spawn ssh ${userName}@172.24.101.117
    expect "password: "
    send "$password\r"
    epxect -re "Last Login: "
    send "cd RedesLab4/TCP\r"
    send "python3 tcpClient.py\r"
"
