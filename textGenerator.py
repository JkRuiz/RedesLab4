import random

reqSize = 250000000
fileName = 'randomText.txt'
with open(fileName,'w') as f:
    for i in range(0, reqSize):
        f.write(str(chr(int(random.randint(33,127)))))