from socket import *
import random
import selectors
import types

class Guesser(object):
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.name = ""
        self.best_guess = 99999
        self.num_messages = 0
        self.num_bad_messages = 0
        self.num_wrong_range = 0
        self.num_incorrect_guess = 0

    def new_guess(self, guess, correct_value):
        new_distance = abs(guess - correct_value)
        old_distance = abs(self.best_guess - correct_value)
        if new_distance < old_distance:
            self.best_guess = guess

class TCPGuessingServer(object):

    def __init__(self, host = '', port = 3600):
        self.sel = selectors.DefaultSelector()
        self.host = host
        self.port = port
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.guessers = {}
        self.min_number = random.randint(1, 1000)
        self.max_number = random.randint(self.min_number + 100, self.min_number + 1000)
        self.correct_value = random.randint(self.min_number, self.max_number)
        self.correct_value_found = False

    def listen(self):
        self.sock.listen(50)
        print('The server is listening...')
        self.sock.setblocking(False)
        self.sel.register(self.sock, selectors.EVENT_READ, data=None)
        while True:
            events = self.sel.select(timeout=None)
            for key, mask in events:
                # From the listening socket, need to accept the connection
                if key.data is None:
                    self.accept_wrapper(key.fileobj)
                # Contains data, need to process data from a client
                else:
                    self.service_connection(key, mask)

    def accept_wrapper(self, sock):
        conn, addr = sock.accept()
        print("Accepting connection from ", addr)
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)
        self.guessers[addr] = Guesser(conn, addr)

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            try:
                recv_data = sock.recv(1024)
                if recv_data:
                    # Check to see if this guesser has a name yet
                    # If not, assume this is the name
                    if data.addr in self.guessers:
                        # Try and read the user's name
                        if self.guessers[data.addr].name == "":
                            self.guessers[data.addr].name = recv_data.decode()
                            data.outb += ("Your name is " + self.guessers[data.addr].name).encode()
                        # Try and read a guess
                        else:
                            self.guessers[data.addr].num_messages += 1
                            try:
                                guess = int(recv_data)
                                prior_best_guess = abs(self.guessers[data.addr].best_guess - self.correct_value)
                                if abs(guess - self.correct_value) < prior_best_guess:
                                    self.guessers[data.addr].best_guess = guess

                                if guess >= 0 and guess <= 2500:
                                    if guess >= self.min_number and guess <= self.max_number:
                                        if guess == self.correct_value:
                                            sock.send(("CONGRATULATIONS! You found the correct number").encode())
                                            self.end_game(self.guessers[data.addr].name)
                                            return

                                        else :
                                            self.guessers[data.addr].num_incorrect_guess += 1
                                            if guess > self.correct_value:
                                                sock.send(("Try a smaller number").encode())
                                            else:
                                                sock.send(("Try a larger number").encode())
                                    else:
                                        self.guessers[data.addr].num_wrong_range += 1
                                        sock.send(("Number not in the selected range!").encode())

                                else:
                                    self.guessers[data.addr].num_bad_messages += 1
                                    sock.send(("Guesses must be between 1 and 2500!").encode())

                            # The message was not a valid number
                            except ValueError:
                                self.guessers[data.addr].num_bad_messages += 1
                                sock.send(("You did not enter a number").encode())
                else:
                    print('Client ', data.addr, "disconnected")
                    self.sel.unregister(sock)
                    sock.close()
            except ConnectionError:
                print('Connection error for ', data.addr, ", disconnected")

    def end_game(self, winner_name):
        request_count = 0
        incorrect_guesses = 0
        bad_numbers = 0
        malformed_responses = 0
        for key in self.guessers:
            self.sel.unregister(self.guessers[key].conn)
            self.guessers[key].conn.close()
            request_count += self.guessers[key].num_messages
            incorrect_guesses += self.guessers[key].num_incorrect_guess
            bad_numbers += self.guessers[key].num_wrong_range
            malformed_responses += self.guessers[key].num_bad_messages

        print("#############################################################")
        print(winner_name + " found the lucky number " + str(self.correct_value) + "!")
        print(str(request_count) + " total requests")
        print(str(incorrect_guesses) + " incorrect guesses")
        print(str(bad_numbers) + " invalid numbers")
        print(str(malformed_responses) + " malformed responses")

        sorted_guesses = sorted(self.guessers.items(), key=lambda x: abs(x[1].best_guess - self.correct_value))
        for guess in sorted_guesses:
            print(guess[1].name + ": " + str(guess[1].best_guess))


if __name__ == "__main__":
    while True:
        user_input = input("Server port? ")
        try:
            port_num = int(user_input)
            TCPGuessingServer('', port_num).listen()
        except ValueError:
            TCPGuessingServer('', 3600).listen()

