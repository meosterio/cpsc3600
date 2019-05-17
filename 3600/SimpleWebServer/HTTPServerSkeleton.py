# Student name: Alex Moore
# CID: 10819083

#import socket module
from socket import *
import os               # To read the last modified time
import datetime         # To format the last modified time
import sys              # In order to terminate the program

serverPort = 8075
serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a sever socket
#Complete this code
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print ('The web server is up on port:' ,serverPort)

while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024)

        # Find the filename of the requested file
        filename = message.split()[1]
        #print (filename)

        # Open and read the file
        f = open(filename[1:])
        outputdata = f.read()

        # Find the date the file was last modified
        statbuf = os.stat(filename[1:])
        last_modified = datetime.datetime.fromtimestamp(
            int(statbuf.st_mtime)).strftime('%m-%d-%Y %H:%M:%S')#Complete this code

        #Send one HTTP header line into socket
        # Complete this code
        connectionSocket.send('HTTP/1.1 200 OK Content-Type: text/html\r\n'.encode())
        connectionSocket.send(("Last-Modified: " + last_modified + '\r\n\r\n').encode())
        #connectionSocket.close()

        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        # Close client socket
        #Complete this code
        connectionSocket.close()
    except FileNotFoundError:
        #Send response message for file not found
        #Complete this code
        connectionSocket.send(
            b'\nHTTP/1.1 404 Not Found Content-Type: text/html\r\n\r\n')

        #Close client socket
        #Complete this code
        connectionSocket.close()
        connectionSocket.close()
serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data
