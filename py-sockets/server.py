#SERVER.PY
import socket
import sqlite3

def Main():
    host = ""
    port = 5000

    mySocket = socket.socket()
    mySocket.bind((host,port))

    mySocket.listen(1)
    conn, addr = mySocket.accept()
    print ("Server: Connection from " + str(addr))
    data = conn.recv(1024).decode()
    if not data:
        return
    print ("Server: recv " + str(data))

    response = "Hello from Server"

    sqlconn = sqlite3.connect('plants.db')
    c = sqlconn.cursor()

    # Create table

    c.execute(data)
    
    tableExistsMsg = 'table plants does not exist'
    tb_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='plants'"
    if sqlconn.execute(tb_exists).fetchone():
        tableExistsMsg = 'table plants exists'
    
    response = tableExistsMsg
    print(response)

    print ("Server: send " + str(response))
    conn.send(response.encode())

    conn.close()

if __name__ == '__main__':
    Main()
