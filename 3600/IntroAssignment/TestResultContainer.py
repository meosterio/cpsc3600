import statistics
import json

class TestResultContainer(dict):
    """docstring for TestResultContainer."""
    def __init__(self):
        #super(TestResultContainer, self).__init__()
        self.my_dict = {'Throughput': [], 'RTT': [], 'Connection_Status': []}

    """function adds the values to the dictionary"""
    def add(self, throughput, rtt, connection_status, tp, rtt_val, cs):
        self.my_dict[throughput].append(tp)
        self.my_dict[rtt].append(rtt_val)
        self.my_dict[connection_status].append(cs)

    """calculates standard deviation of list"""
    def std(self, list):
        s = statistics.stdev(self.my_dict[list])
        s = round(s,3)
        return s;

    """calculates the average of the list"""
    def avg(self, list):
        a = (sum(self.my_dict[list]) / float(len(self.my_dict[list])))
        a = round(a,3)
        return a;

    """writes the list values to a json file"""
    def write_to_json(self, my_dict):
        with open('results.json', 'w') as fp:
            json.dump(my_dict, fp)

    def prnt(self, list):
        avg = self.avg(list)
        std = self.std(list)
        print ("The average and standard deviation of",list,"are ",avg," and ",std)
