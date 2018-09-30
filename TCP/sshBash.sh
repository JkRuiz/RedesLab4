#!/bin/bash
##Enter Username and Password Details:
userName="isis"
password="labredesML340"

spawn ssh ${userName}@172.24.101.117
expect "password: "
send "$password\r"
expect -re "Last Login: "
send "cd RedesLab4/TCP\r"
send "python3 tcpClient.py\r"
