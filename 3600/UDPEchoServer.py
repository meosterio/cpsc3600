from socket import *
import threading

class UDPEchoServer(object):
    def __init__(self, host = '', port = 3600): #constructor
        self.host = host
        self.port = port

    def listen(self):
        with socket(AF_INET, SOCK_DGRAM) as s:
            s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            print('The server is listening...')
            while True:
                message, clientAddr = s.recvfrom(2048)
                print('Echoing "', message, '" to ', clientAddr)
                s.sendto(message, clientAddr)

if __name__ == "__main__":
    while True:
        port_num = input("Server port? ")
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass

    UDPEchoServer('', port_num).listen() #object is used as self
