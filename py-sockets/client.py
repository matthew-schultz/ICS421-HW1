#CLIENT
import socket
import sqlite3
#from sqlite3 import Error

def Main():
        host = '172.17.0.3'
        port = 5000

        mySocket = socket.socket()
        mySocket.connect((host,port))

        message = '''CREATE TABLE if not exists plants(commonName text, plantStatus text, dateAdded date)'''

        print ('Client: send ' + str(message))
        mySocket.send(message.encode())
        data = mySocket.recv(1024).decode()

        print ('Client: recv ' + str(data))

        mySocket.close()

if __name__ == '__main__':
	Main()

