from socket import *
import threading

class ThreadedTCPEchoServer(object):
    def __init__(self, host = '', port = 3600):
        self.host = host
        self.port = port
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(50)
        print('The server is listening...')
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,
                             args = (client, address)).start()
            print("Accepting connection from ", address)

    def listenToClient(selfself, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    response = data
                    client.send(response)
                    print('Echoing "', data, '" to ', address)
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                print('Client ', address, "disconnected")
                return False

if __name__ == "__main__":
    while True:
        port_num = input("Server port? ")
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass

    ThreadedTCPEchoServer('', port_num).listen()