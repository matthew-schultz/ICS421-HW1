#runDDL.py
import socket
import sqlite3
import sys

def Main():
    #get command line arguments
    clustercfg = sys.argv[1]
    ddlfile = sys.argv[2]

    #read ddlfile as a string of sql code
    with open(ddlfile, 'r') as myfile:
        data=myfile.read().replace('\n', '')
    print("sql string is " + data)
    

    #for x in range(0, 3):
        # create a database in x container

if __name__ == '__main__':
    Main()

