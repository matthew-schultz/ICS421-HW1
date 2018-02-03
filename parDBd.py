#parDBD.py
import socket
import sqlite3
import sys
#import sqlite3.OperationalError


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
        except sqlite3.OperationalError as e:
            print(e)
            tableCreatedMsg = 'failure'
        else:
            tableCreatedMsg = 'success'
        sqlConn.commit()
        sqlConn.close()

        response = tableCreatedMsg
        print(response)

        print ('parDBd: send response "' + str(response) +  '" for sql "' + str(ddlSQL) + '"')
        runDDLConn.send(response.encode())

        runDDLConn.close()
        mySocket.close()
    else:
        print("parDBd: ERROR need at least 3 arguments to run properly (e.g. \"python3 parDBd.py 171.0.0.2 5000\"")


if __name__ == '__main__':
    try:
        Main()
    except OSError as e:
        print('failed due to OSError; please retry in a minute\n' + str(e))


