import random
from enum import Enum, IntEnum
import copy

class Simulator():

    # *********************** Simulator routines ***********************
    # ************ DO NOT CALL ANY ROUTINES IN THIS SECTION ************
    # *********** ROUTINES FOR STUDENT USE CAN BE FOUND BELOW **********
    def __init__(self, RDT):
        self.RDT = RDT
        self.RDT.simulator = self
        self.continue_simulation = True
        self.event_list = []

        self.TRACE = 1          # For my debugging
        self.nsim = 0           # number of messages from 5 to 4 so far
        self.nsimmax = 0        # number of msgs to generate, then stop
        self.time = 0.000       #
        self.lossprob = 0       # probability that a packet is dropped
        self.corruptprob = 0    # probability that one bit is packet is flipped
        self.lmbda = 0          # arrival rate of messages from layer 5
        self.ntolayer3 = 0      # number sent into layer 3
        self.nlost = 0          # number lost in media
        self.ncorrupt = 0       # number corrupted by media

    def Setup(self):
        print("-----  Stop and Wait Network Simulator Version 1.1 -------- \n\n")
        self.nsimmax = int(input("Enter the number of messages to simulate: "))
        self.lossprob = float(input("Enter  packet loss probability [enter 0.0 for no loss]:"))
        self.corruptprob = float(input("Enter packet corruption probability [0.0 for no corruption]:"))
        self.lmbda = float(input("Enter average time between messages from sender's layer5 [ > 0.0]:"))
        self.TRACE = int(input("Enter TRACE:"))

        self.generate_next_arrival()

    def Simulate(self):

        self.RDT.A_Init()
        self.RDT.B_Init()

        while self.continue_simulation:
            # Check to see if we have any more events to simulate
            if len(self.event_list) == 0:
                self.continue_simulation = False
                self.trace("Simulator terminated at time {} after sending {} msgs from layer5\n".format(self.time, self.nsim), 0)
            else:
                cur_event = self.event_list.pop(0)

                self.trace("EVENT time: {}, type: {}, entity: {}".format(cur_event.evtime, cur_event.evtype, cur_event.eventity),2)

                self.time = cur_event.evtime # update time to next event time
                if self.nsim == self.nsimmax:
                    self.continue_simulation = False    #all done with simulation
                else:
                    if cur_event.evtype == EventType.FROM_LAYER5:
                        self.generate_next_arrival()    # set up future arrival

                        # fill in msg to give with string of same letter
                        j = self.nsim % 26
                        msg2give = ""
                        for i in range(0,19):
                            msg2give += chr(97 + j)

                        self.trace("MAINLOOP: data given to student: {}".format(msg2give), 2)

                        self.nsim += 1
                        if cur_event.eventity == EventEntity.A:
                            self.RDT.A_CommunicateWithApplicationLayer(msg2give)
                        else:
                            self.trace("ERROR: Attempting to communicate with the application layer on Host B", 1)

                    elif cur_event.evtype == EventType.FROM_LAYER3:
                        if cur_event.eventity == EventEntity.A:
                            self.RDT.A_CommunicateWithNetworkLayer(cur_event.pkt)
                        else:
                            self.RDT.B_CommunicateWithNetworkLayer(cur_event.pkt)

                    elif cur_event.evtype == EventType.TIMER_INTERRUPT:
                        if cur_event.eventity == EventEntity.A:
                            self.RDT.A_TimerInterrupt()
                        else:
                            self.trace("ERROR: Attempting to interrupt a timer on Host B", 1)

    def generate_next_arrival(self):
        self.trace("GENERATE NEXT ARRIVAL: creating new arrival",2)

        x = self.lmbda*random.uniform(0.0, 1.0)*2  # x is uniform on [0,2*lambda], having mean of lambda
        new_event = SimulatedEvent()
        new_event.evtime = self.time + x
        new_event.evtype = EventType.FROM_LAYER5
        if self.RDT.bidirectional and random.uniform(0.0, 1.0) > 0.5:
            new_event.eventity = EventEntity.B
        else:
            new_event.eventity = EventEntity.A
        self.insert_event(new_event)

    def insert_event(self, new_event):
        self.trace("INSERTEVENT: time is {}f".format(self.time),2)
        self.trace("INSERTEVENT: future time will be {}f".format(new_event.evtime),2)
        # If queue is empty, add as head and don't connect any adjacent events
        if len(self.event_list) == 0:
            self.event_list.append(new_event)
        else:
            # check to see if this event occurs before the first element
            if new_event.evtime < self.event_list[0].evtime:
                self.event_list.insert(0, new_event)
            # check to see if this event occurs after the last element\
            elif new_event.evtime > self.event_list[-1].evtime:
                self.event_list.append(new_event)
            else:
                for idx, e in enumerate(self.event_list):
                    if new_event.evtime < e.evtime:
                        self.event_list.insert(idx, new_event)
                        break

    def print_event_list(self, trace_level):
        for e in self.event_list:
            self.trace("Event time: {}, type: {} entity: {}".format(e.evtime, e.evtype, e.eventity),trace_level)


    # *********************** Student callable routines ***********************
    # ******** DO NOT CALL ANY ROUTINES IN Simulator ABOVE THESE LINES ********
    def stop_timer(self, entity):
        self.trace("STOP TIMER: stopping timer at {}".format(self.time), 2)
        for idx, e in enumerate(self.event_list):
            if e.evtype == EventType.TIMER_INTERRUPT and e.eventity == entity:
                self.event_list.pop(idx)    # Remove the first timer event associated with this entity
                return
        self.trace("Warning: unable to cancel your timer. It wasn't running.",0)

    def start_timer(self, entity, increment):
        self.trace("START TIMER: starting timer at {}".format(self.time),2)

        # Check to see if a timer has already been started
        for e in self.event_list:
            if e.evtype == EventType.TIMER_INTERRUPT and e.eventity == entity:
                self.trace("Warning: attempt to start a timer that is already started", 0)
                return

        new_event = SimulatedEvent()
        new_event.evtime = self.time + increment
        new_event.evtype = EventType.TIMER_INTERRUPT
        new_event.eventity = entity
        self.insert_event(new_event)

    def to_layer3(self, entity, packet):
        self.ntolayer3 += 1

        # Simulate losses
        if random.uniform(0.0, 1.0) < self.lossprob:
            self.nlost += 1
            self.trace("TOLAYER3: PACKET BEING LOST", 0)
            return

        # make a copy of the packet student just gave me since he/she may decide
        # to do something with the packet after we return back to him/her
        pkt = copy.deepcopy(packet)
        try:
            self.trace("TOLAYER3: seq: {}, ack {}, check: {}, {}".format(pkt.seqnum, pkt.acknum, pkt.checksum, pkt.payload), 2)
        except Exception:
            pass

        new_event = SimulatedEvent()
        new_event.evtype = EventType.FROM_LAYER3
        new_event.eventity = EventEntity((int(entity)+1) % 2)     # event occurs at the other entity
        new_event.pkt = pkt

        # finally, compute the arrival time of packet at the other end.
        # medium can not reorder, so make sure packet arrives between 1 and 10
        # time units after the latest arrival time of packets
        # currently in the medium on their way to the destination
        last_time = self.time
        for e in self.event_list:
            if e.evtype == EventType.FROM_LAYER3 and e.eventity == entity:
                last_time = e.evtime
        new_event.evtime = last_time + 1 + 9*random.uniform(0.0, 1.0)

        # simulate corruption
        if random.uniform(0.0, 1.0) < self.corruptprob:
            self.ncorrupt += 1
            self.trace("TOLAYER3: PACKET BEING CORRUPTED",0)
            x = random.uniform(0.0, 1.0)
            if x < 0.75:
                self.trace("CORRUPTING PACKET DATA", 1)
                pkt.payload += "Z"    # Corrupted packet
            elif x < 0.875:
                self.trace("CORRUPTING PACKET SEGMENT NUMBER", 1)
                pkt.seqnum = 999999
            else:
                self.trace("CORRUPTING PACKET ACK NUMBER", 1)
                pkt.acknum = 999999

        self.trace("TOLAYER3: scheduling arrival on other side", 2)
        self.insert_event(new_event)

    def to_layer5(self, entity, datasent):
        self.trace("TOLAYER5: data received: {}".format(datasent), 2)

    def trace(self, message, error_level):
        if error_level <= self.TRACE:
            print(message)



class SimulatedEvent():
    def __init__(self):
        self.evtime = 0
        self.evtype = None
        self.eventity = None
        self.pkt = None
        self.previous_event = None
        self.next_event = None


class Packet():
    def __init__(self):
        self.seqnum = 0
        self.acknum = 0
        self.checksum = 0
        self.payload = ""


class EventType(Enum):
    FROM_LAYER5 = 1
    FROM_LAYER3 = 2
    TIMER_INTERRUPT = 3


class EventEntity(IntEnum):
    A = 0
    B = 1
