#runDDL.py
import configparser
import socket
import sqlite3
import sys
from threading import Thread


def CreateNodeDatabase(ddlSQL, dbhost, dbport, nodeNum):
    #host = '172.17.0.' + str(x)
    #port = 5000
    print('runDDL.py: connecting to host ' + dbhost)

    mySocket = socket.socket()
    try:
        mySocket.connect((dbhost, dbport))
        print('runDDL.py: send ' + str(ddlSQL))
        mySocket.send(ddlSQL.encode())
        data = str(mySocket.recv(1024).decode())
        print('runDDL.py: recv ' + data)
        if(data == 'success'):
            catSQL = 'INSERT INTO dtables VALUES ("","","' + dbhost + '","","",0,' + str(nodeNum) + ',"","","")'
            print('catSQL is: ' + catSQL)
            # print('')
    except OSError:
        print('runDDL.py: failed to connect to host ' + dbhost)
    mySocket.close()


def CreateCatalog():
    sqlConn = sqlite3.connect('catalog.db')
    c = sqlConn.cursor()
    # catSQL = 'DROP TABLE dtables;\n'
    catSQL = '''CREATE TABLE IF not exists dtables(tname char(32), 
            nodedriver char(64), 
            nodeurl char(128), 
            nodeuser char(16), 
            nodepasswd char(16), 
            partmtd int, 
            nodeid int, 
            partcol char(32), 
            partparam1 char(32),
            partparam2 char(32),
            CONSTRAINT unique_nodeid UNIQUE(nodeid))'''
    # Create table
    tableCreatedMsg = ''
    try:
        c.execute(catSQL)
    except Error:
        tableCreatedMsg = 'failed'
    else:
        tableCreatedMsg = 'success'    
    return tableCreatedMsg


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

        catMsg = CreateCatalog()
        print('Catalog creation: ' + catMsg)

        #CreateDatabase(3,  ddlSQL)
        for currentNodeNum in range(1, int(configDict['numnodes']) + 1):
            dbhost = configDict['node' + str(currentNodeNum) + '.hostname']
            dbport = int(configDict['port'])
            t = Thread(target=CreateNodeDatabase, args=(ddlSQL, dbhost, dbport, currentNodeNum, ))
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

