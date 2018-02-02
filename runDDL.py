#runDDL.py
import configparser
import socket
import sqlite3
import sys
from threading import Thread


def SendDDLToNode(ddlSQL, dbhost, dbport, nodeNum):
    #host = '172.17.0.' + str(x)
    #port = 5000
    print('runDDL.py: connecting to host ' + dbhost)

    mySocket = socket.socket()
    try:
        mySocket.connect((dbhost, dbport))
        print(__file__ + ': send ' + str(ddlSQL))
        mySocket.send(ddlSQL.encode())
        data = str(mySocket.recv(1024).decode())
        print(__file__ + ': recv ' + data)

        if(data == 'success'):
            tname = getTname(ddlSQL)
            print('tname is ' + tname)

            catSQL = 'DELETE FROM dtables WHERE nodeid='+ str(nodeNum) + ';'            

            if SQLIsCreate(ddlSQL):
                print ('ddlSQL is a create statement')
                catSQL = 'TRUNCATE TABLE tablename;'
                catSQL = 'INSERT INTO dtables VALUES ("'+ tname +'","","' + dbhost + '","","",0,' + str(nodeNum) + ',NULL,NULL,NULL)'
            runSQL(catSQL)
            print('runDDL.py: ' + catSQL)
            # print('')
    except OSError:
        print('runDDL.py: failed to connect to host ' + dbhost)
    mySocket.close()


def runSQL(sql):
    print(__file__ + ': executing sql statement ' + sql) 
    try:
        sqlConn = sqlite3.connect('catalog.db')
        c = sqlConn.cursor()
        c.execute(sql)
        print(str(c.fetchall()))
        sqlConn.commit()
        sqlConn.close()
    except Error as e:
        print(e)


def SQLIsCreate(sql):
    isInsert = False
    # remove leading whitespace from sql string and split
    sqlArray = sql.lstrip().split(" ")
    # print(str(sqlArray))
    # print(sqlArray[0].upper())
    if sqlArray[0].upper() == 'CREATE':
        isInsert = True
    return isInsert


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
        tableCreatedMsg = 'failure'
    else:
        tableCreatedMsg = 'success'
    sqlConn.commit()
    sqlConn.close()
    return tableCreatedMsg


def getTname(data):
    tname = ''
    
    dataArray = data.split(' ')
    count = 0
    for d in dataArray:
        # print('d is ' + d)
        if d.upper() == 'TABLE':
            print('d matches TABLE')
            #print('dataArray[count+1] is ' + dataArray[count+1])
            if dataArray[count + 1] == 'if':
                 print('slot after d matches if')
                 print('dataArray[count+4] is ' + dataArray[count+4])
                 tname = dataArray[count+4]
            else: tname = dataArray[count + 1]
        count = count + 1   
    tname = tname.split('(')[0]
    return tname


def Main():
    #get command line arguments
    if(len(sys.argv) >= 3):
        clustercfg = sys.argv[1]
        ddlfile = sys.argv[2]
        
        configDict = ParseConfig(clustercfg)
        # print('ParseConfig returned ' + str(configDict))

        #read ddlfile as a string to be executed as sql
        with open(ddlfile, 'r') as myfile:
            ddlSQL=myfile.read().replace('\n', '')
        # print("sql string is " + ddlSQL)

        catMsg = CreateCatalog()
        print(__file__ + ': CreateCatalog() returned: ' + catMsg)

        #CreateDatabase(3,  ddlSQL)
        for currentNodeNum in range(1, int(configDict['numnodes']) + 1):
            dbhost = configDict['node' + str(currentNodeNum) + '.hostname']
            dbport = int(configDict['node' + str(currentNodeNum) + '.port'])
            # print('will connect to node' + str(currentNodeNum) + ' at IP:' + dbhost + ' and port:' + str(dbport))
            t = Thread(target=SendDDLToNode, args=(ddlSQL, dbhost, dbport, currentNodeNum, ))
            t.start()
    else:
          print(__file__ + ': ERROR need at least 3 arguments to run properly (e.g. \"python3 runDDL.py cluster.cfg plants.sql\"')



def ParseConfig(clustercfg):
    '''config = configparser.ConfigParser()
    config.read(clustercfg)
    print("Config has been read")

    configDict = {'numnodes': config.get('clustercfg', 'numnodes'),
            'catalog.hostname': config.get('clustercfg', 'catalog.hostname'),
            'node1.hostname': config.get('clustercfg', 'node1.hostname'),
            'node2.hostname': config.get('clustercfg', 'node2.hostname'),
            'port': config.get('clustercfg', 'port')}'''
    file = open(clustercfg)
    content = file.read()
    configArray = content.split("\n")
    # configList = []
    configDict = {}
    for config in configArray:
        if config:
            c = config.split("=")
            # print (c[0] + ' is ' + c[1])
            configKey = c[0]
            configValue = c[1]
            if(('node' in configKey or 'catalog' in configKey) and 'hostname' in configKey):
                #print('configKey has node hostname')
                nodename = configKey.split(".")[0]
                hostname = configValue.split(":")
                configIP = hostname[0]
                configPort = hostname[1].split("/")[0]
                configDb = hostname[1].split("/")[1]
                '''print('nodename is ' + nodename)
                print('configValue is ' + configValue)
                print('configIP is ' + configIP)
                print('configPort is ' + configPort)
                print('configDb is ' + configDb)'''        
                configDict[nodename + '.port'] = configPort
                configDict[nodename + '.db'] = configDb
                configValue = configIP
            configDict[configKey]=configValue
        '''#configList.append(c)[1]
                print (c[0] + '=' + c[1])
                configDict[c[0]] = c[1]'''

    # print ('cfg dictionary is ' + str(configDict))
    file.close()
    return configDict


if __name__ == '__main__':
    Main()

