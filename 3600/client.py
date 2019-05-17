from socket import *
serverName = 'newton.cs.clemson.edu'
serverPort = 3600
serverSocket = socket(AF_INET, SOCK_DGRAM)
#clientSocket.connect((serverName, serverPort))
message = input("Enter text: ")
#clientSocket.send(message.encode())
while True:
	clientAddress=serverSocket.recvfrom(2048)
	message = input("Enter a number: ")
	serverSocket.sendto(message.encode(), clientAddress)

	

