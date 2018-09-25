import socket

port = 60000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
serverSocket.bind((host, port))  # Bind to the port
serverSocket.listen(1)  # Now wait for client connection.
print ('Server listening....')

while True:
    conn, addr = serverSocket.accept()  # Establish connection with client.
    print ('Got connection from', addr)
    data = conn.recv(1024).decode('utf-8')
    print('Server received', repr(data))
    filename = 'mytext.txt'
    f = open(filename, 'rb')
    l = f.read(1024)
    while (l):
        conn.send(l)
        print('Sent ', repr(l))
        l = f.read(1024)
    f.close()
    print('Done sending')
    conn.close()
