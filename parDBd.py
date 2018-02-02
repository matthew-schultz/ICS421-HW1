#parDBD.py
import socket
import sqlite3
import sys


def Main():
    if(len(sys.argv) >= 3):
        host = sys.argv[1]
        #host = ''
        port = int(sys.argv[2])

        mySocket = socket.socket()
        mySocket.bind((host,port))

        mySocket.listen(1)
        runDDLConn, addr = mySocket.accept()
        print ("parDBd: Connection from " + str(addr))
        ddlSQL = runDDLConn.recv(1024).decode()
        if not ddlSQL:
            return
        print ("parDBd: recv " + str(ddlSQL))

        sqlConn = sqlite3.connect('plants.db')
        c = sqlConn.cursor()

    # Create table
        tableCreatedMsg = ''
        try:
            c.execute(ddlSQL)
        except Error:
            tableCreatedMsg = 'failed'
        else:
            tableCreatedMsg = 'success'
    
        response = tableCreatedMsg
        print(response)

        print ("parDBd: send " + str(response))
        runDDLConn.send(response.encode())

        runDDLConn.close()
    else:
        print("parDBd: ERROR need at least 3 arguments to run properly (e.g. \"python3 parDBd.py 171.0.0.2 5000\"")


if __name__ == '__main__':
    try:
        Main()
    except OSError:
        print('failed due to OSError; please retry in a minute')

