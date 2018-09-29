import random

reqSize = 500000000
fileName = 'randomText500.txt'
with open(fileName,'w') as f:
    for i in range(0, reqSize):
        f.write(str(chr(int(random.randint(33,127)))))