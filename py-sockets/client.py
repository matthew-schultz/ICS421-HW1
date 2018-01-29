mport socket

def Main():
        host = '172.17.0.2'
        port = 5000

        mySocket = socket.socket()
        mySocket.connect((host,port))

        message = "Hello from client program!"

        print ('Client: send ' + str(message))
        mySocket.send(message.encode())
        data = mySocket.recv(1024).decode()

        print ('Client: recv ' + str(data))

        mySocket.close()

if __name__ == '__main__':
    Main()

