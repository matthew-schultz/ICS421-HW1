#runDDL.py
import configparser
import socket
import sqlite3
import sys
from threading import Thread

def CreateDatabase(ddlSQL, dbhost, dbport):
    #host = '172.17.0.' + str(x)
    #port = 5000
    print('runDDL.py: connecting to host ' + dbhost)

    mySocket = socket.socket()
    try:
        mySocket.connect((dbhost, dbport))
        print('runDDL.py: send ' + str(ddlSQL))
        mySocket.send(ddlSQL.encode())
        data = mySocket.recv(1024).decode()
        print('runDDL.py: recv ' + str(data))
    except OSError:
        print('runDDL.py: failed to connect to host ' + dbhost)
    mySocket.close()

# def CreateCatalog():


def Main():
    #get command line arguments
    if(len(sys.argv) >= 3):
        clustercfg = sys.argv[1]
        ddlfile = sys.argv[2]
        
        configDict = ParseConfig(clustercfg)
        print('ParseConfig returned ' + str(configDict))

        #read ddlfile as a string to be executed as sql
        with open(ddlfile, 'r') as myfile:
            ddlSQL=myfile.read().replace('\n', '')
        # print("sql string is " + ddlSQL)
    
        #CreateDatabase(3,  ddlSQL)
        for i in range(1, 3):
            dbhost = configDict['node' + str(i) + '.hostname']
            dbport = int(configDict['port'])
            t = Thread(target=CreateDatabase, args=(ddlSQL, dbhost, dbport, ))
            t.start()
            # create a database in x container
            # CreateDatabase(ddlSQL, dbhost, dbport)
    else:
          print("runDDL.py: ERROR need at least 3 arguments to run properly (e.g. \"python3 runDDL.py cluster.cfg plants.sql\"")



def ParseConfig(clustercfg):
    config = configparser.ConfigParser()
    config.read(clustercfg)
    print("Config has been read")
    '''print(config.get('clustercfg', 'numnodes'))
    print(config.get('clustercfg', 'catalog.hostname'))
    print(config.get('clustercfg', 'node1.hostname'))
    print(config.get('clustercfg', 'node2.hostname'))'''

    configDict = {'numnodes': config.get('clustercfg', 'numnodes'),
            'catalog.hostname': config.get('clustercfg', 'catalog.hostname'),
            'node1.hostname': config.get('clustercfg', 'node1.hostname'),
            'node2.hostname': config.get('clustercfg', 'node2.hostname'),
            'port': config.get('clustercfg', 'port')}

    return configDict


if __name__ == '__main__':
    Main()

