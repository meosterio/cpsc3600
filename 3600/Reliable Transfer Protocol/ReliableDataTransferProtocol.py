from Simulator import Simulator
from Simulator import Packet
from Simulator import EventEntity
from enum import Enum


class ReliableDataTransferProtocol():
    def __init__(self, bidirectional = False):
        self.bidirectional = bidirectional
        self.simulator = None


    # This routine will be called once, before any of your other A-side routines are called.
    # It can be used to do any required initialization.
    def A_Init(self):
        self.p = Packet()
        #create seqnum
        self.i = 0

        #IMPLEMENT GBN BY USING AN ARRAY OF THE packets
        pass


    # This routine will be called whenever the upper layer at the sending side (A) has a message to send.
    # It is the job of your protocol to insure that the data in such a message is delivered in-order,
    # and correctly, to the receiving side upper layer.
    def A_CommunicateWithApplicationLayer(self, message):
        self.simulator.trace("A received {} from application layer".format(message),1)
        self.p = Packet()
        self.p.payload = message
        self.p.seqnum = self.i
        #self.p.acknum = self.i
        sum = checksum(self.p)
        self.p.checksum = sum
        simulator.to_layer3(EventEntity.A, self.p)
        simulator.start_timer(0, 20)

        self.i = 0 if self.i == 1 else 1

        #Just send it
        #create new packet every time message to be sent


    # This routine will be called whenever a packet sent from the B-side (i.e., as a result of a tolayer3()
    # being done by a B-side procedure) arrives at the A-side. packet is the (possibly corrupted) packet
    # sent from the B-side.
    def A_CommunicateWithNetworkLayer(self, packet):
        self.simulator.trace("A received a packet (SEQ: {}, ACK: {}, Checksum: {}, Payload: {}) from network layer layer".format(
            packet.seqnum, packet.acknum, packet.checksum, packet.payload), 1)
        if (packet.acknum == (self.p.seqnum)  and packet.seqnum == (self.p.seqnum)
            and packet.checksum == 0 and packet.payload == ""):
            print("A received a valid ACK " + str(packet.acknum))
            simulator.stop_timer(0)
        elif (packet.acknum != self.p.seqnum):
            print ("ERROR: A received a packet with the wrong ACK number!")
        else:
            print("ERROR: A received a corrupt packet!")



    # This routine will be called when A's timer expires (thus generating a timer interrupt). You'll probably
    # want to use this routine to control the retransmission of packets. See starttimer() and stoptimer()
    # below for how the timer is started and stopped.
    def A_TimerInterrupt(self):
        self.simulator.trace("A experienced a timer interrupt", 1)
        print("Resending packet from A -> B")
        simulator.to_layer3(EventEntity.A, self.p)
        simulator.start_timer(0, 20)


    # This routine will be called once, before any of your other B-side routines are called.
    # It can be used to do any required initialization.
    def B_Init(self):
        pass


    # This routine will be called whenever a packet sent from the A-side (i.e., as a result of a tolayer3() being done
    # by a A-side procedure) arrives at the B-side. packet is the (possibly corrupted) packet sent from the A-side.
    def B_CommunicateWithNetworkLayer(self, packet):
        self.simulator.trace("B received a packet (SEQ: {}, ACK: {}, Checksum: {}, Payload: {}) from network layer layer".format(
            packet.seqnum, packet.acknum, packet.checksum, packet.payload), 1)

        p = Packet()

        sum = checksum(packet)
        if (packet.checksum == sum):
            simulator.to_layer5(EventEntity.B, packet.payload)
            p.acknum = 0 if packet.seqnum == 0 else 1
            p.seqnum = packet.seqnum
            #p.checksum = sum
            simulator.to_layer3(EventEntity.B, p)
        else:
            print("ERROR: B received a corrupt packet!")
            p.acknum = 0 if packet.seqnum == 1 else 1
            p.seqnum = ""
            simulator.to_layer3(EventEntity.B, p)


def checksum(packet):
    checksum = 0

    for i in range (0, len(packet.payload)):
        checksum = (checksum + ord(packet.payload[i]))
    checksum = int(packet.seqnum) + packet.acknum + checksum

    return checksum


if __name__ == "__main__":
    rdt = ReliableDataTransferProtocol()
    simulator = Simulator(rdt)

    simulator.Setup()
    simulator.Simulate()


    #rdt.A_Init()
    #rdt.B_Init()
