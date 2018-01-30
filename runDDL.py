#runDDL.py
import socket
import sqlite3
import sys

def CreateDatabase(x, ddlSQL):
    host = '172.17.0.' + str(x)
    port = 5000
    print('runDDL.py: connecting to host ' + host)

    mySocket = socket.socket()
    try:
        mySocket.connect((host,port))
        print('runDDL.py: send ' + str(ddlSQL))
        mySocket.send(ddlSQL.encode())
        data = mySocket.recv(1024).decode()
        print('runDDL.py: recv ' + str(data))
    except OSError:
        print('runDDL.py: failed to connect to host ' + host)
    mySocket.close()
    

def Main():
    #get command line arguments
    if(len(sys.argv) >= 3):
        clustercfg = sys.argv[1]
        ddlfile = sys.argv[2]

        #read ddlfile as a string to be executed as sql
        with open(ddlfile, 'r') as myfile:
            ddlSQL=myfile.read().replace('\n', '')
        # print("sql string is " + ddlSQL)
    
        #CreateDatabase(3,  ddlSQL)
        for x in range(3, 5):
            # create a database in x container
            CreateDatabase(x, ddlSQL)
    else:
          print("runDDL.py: ERROR need at least 3 arguments to run properly (e.g. \"python3 runDDL.py cluster.cfg plants.sql\"")        

if __name__ == '__main__':
    Main()

