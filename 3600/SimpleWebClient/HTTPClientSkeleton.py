# Student name: Alex Moore
# CID: 10819083

import argparse
from socket import *
import os               # To read the last modified time
import datetime
import sys              # In order to terminate the program

# Read in the arguments for the HTTP Client
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('server_host',
                   help='The server you are trying to contact')
parser.add_argument('server_port', type=int,
                   help='The port for the server')
parser.add_argument('filename',
                   help='The name of the file you wish to download')

# Args contains three values
#args.server_host = the server host you entered when running the program
#args.server_port = the port you want to connect to on the server
#args.filename = the name of the requested file
args = parser.parse_args()

print("server_host: " + args.server_host)
print("server_host: " + str(args.server_port))
print("server_host: " + args.filename)

clientSocket = socket(AF_INET, SOCK_STREAM)#Complete this code
clientSocket.connect((args.server_host, args.server_port))  #Complete this code)
clientSocket.send(("GET /" + args.filename + " HTTP/1.1").encode()) #Complete this code)

# Get the status line
result = clientSocket.recv(2048)#Complete this code\
decode = result.decode()
print(decode)

# You need to handle two types of responses: 200 OK responses, and 404 Not Found responses
# Check to see which response was returned by the server and handle it appropriately
#Complete this code
rec = ""
if (decode.find("200 OK") > 0):
    while True:
        data = clientSocket.recv(1024)
        #print(data.decode())
        if not data:
            break
        rec = rec + data.decode()
    print(rec)

clientSocket.close()
