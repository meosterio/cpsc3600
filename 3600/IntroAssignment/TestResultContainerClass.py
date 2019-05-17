from collections import defaultdict
import statistics

class TestResultContainer(dict):
    """docstring for TestResultContainer."""
    def __init__(self):
        #super(TestResultContainer, self).__init__()
        self.my_dict = {'throughput': [], 'rtt': [], 'connection_status': []}

    def add(self, throughput, rtt, connection_status, tp, rtt_val, cs):
        self.my_dict[throughput].append(tp)
        self.my_dict[rtt].append(rtt_val)
        self.my_dict[connection_status].append(cs)

    def avg(self, list):
        a = (sum(self.my_dict[list]) / float(len(self.my_dict[list])))
        return a;

    def std(self, list):
        s = statistics.stdev(self.my_dict[list])
        s = round(s,3)
        return s;

    def prnt(self, list):
        trc = TestResultContainer()
        avg = trc.avg(list)
        std = trc.std(list)
        print ("The average and standard deviation of ",list," are ",avg," and ",std)
