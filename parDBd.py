#parDBD.py
import socket
import sqlite3
import sys

def Main():
    host = ""
    port = 5000

    mySocket = socket.socket()
    mySocket.bind((host,port))

    mySocket.listen(1)
    runDDLConn, addr = mySocket.accept()
    print ("parDBd: Connection from " + str(addr))
    ddlSQL = runDDLConn.recv(1024).decode()
    if not ddlSQL:
        return
    print ("parDBd: recv " + str(ddlSQL))

    # response = "Hello from parDBD"

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

if __name__ == '__main__':
    Main()
