import socket as socket
import signal
import sys
import json
import pickle

class PythonSniffer:

    #Class Inastantiator (constructor)    
    def __init__(self, packet_log = None, number_of_packets=0, capture_filter='NoLo'):
        self.packet_list = []
        self.good_packet_list = []
        self.capture_filter = capture_filter

        if packet_log != None:
            self.load_capture_file(packet_log)
        else:
            self.number_of_packets = number_of_packets
            self.WasInterrupted = False

            #Signal Handler to handle Ctrl+C user input.
            signal.signal(signal.SIGINT, self.signal_handler)

            print('Starting Packet Capture. Press Ctrl+C to Stop')
            self.start_capture()

    def load_capture_file(self, filename):
        with open(filename, 'rb') as f:
            self.packet_list = pickle.load(f)

    def start_capture(self):

        #This is specified in Linux to recieve packets of all protocols. 
        #check the manual page "man packet", for details
        ETH_P_ALL = 0x0003
        s = socket.socket( socket.AF_PACKET , socket.SOCK_RAW , socket.ntohs(ETH_P_ALL)) #Linux
        
        #Capture Packets forever if number_of_packets set to 0 until the user press Ctrl+C
        if self.number_of_packets == 0:
            count = 1
            while True and not self.WasInterrupted:
                packet = s.recvfrom(65565) #Blocks until a packet is captured!

                if self.capture_filter == 'NoLo' and packet[1][0] == 'lo': #Skip Loopback interface packets (the ones to 127.0.0.1)
                    continue #skip storing this packet's information

                print ('\t%d Packets captured so far' % count, end='\t\r')
                self.packet_list.append(packet)
                count = count + 1
        #Capture a limited number of packets
        elif self.number_of_packets >= 0:
            count = 0
            while count<self.number_of_packets and not self.WasInterrupted: 
                packet = s.recvfrom(65565) #Blocks until a packet is captured!
                if self.capture_filter == 'NoLo' and packet[1][0] == 'lo': #Skip Loopback interface packets (the ones to 127.0.0.1)
                    continue #skip storing this packet's information
                self.packet_list.append(packet)
                count = count + 1
                print ('\t%d Packets captured so far' % self.number_of_packets, end='\t\r')
        print("Packet Capture Completed")


    def write_with_pickle(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.good_packet_list, f)

    def signal_handler(self,sig, frame):
        print('\nPacket Capture stopped by User')
        self.WasInterrupted = True



    #ToString method
    def __str__(self):
        str_info = ''
        str_info = str(len(self.packet_list)) + ' Packets captured'
        
        return str_info
    




    