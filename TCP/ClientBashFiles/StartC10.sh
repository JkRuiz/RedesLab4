#!/bin/bash

sshpass -p "labredesML340" ssh -o StrictHostKeyChecking=no isis@172.24.101.126 "python3 RedesLab4/TCP/tcpClient.py"
