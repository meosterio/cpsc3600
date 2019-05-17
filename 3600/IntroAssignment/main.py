import json
from TestResultContainerClass import TestResultContainer

def write_to_json(self, my_dict):
    with open('results.json', 'w') as fp:
        json.dump(my_dict, fp)

if __name__ == "__main__":
    trc = TestResultContainer()
    count = 0
    try:
        while True:
            print("")
            print ("Input values from a single test:")
            while True:
                tp = input("Throughput? ")
                try:
                    tp = float(tp)
                    if (tp < 0):
                        print("Enter a nonnegative value")
                        continue
                    break
                except ValueError:
                    print("Enter a float value")
            while True:
                rtt = input("RTT? ")
                try:
                    rtt = float(rtt)
                    if (rtt < 0):
                        print("Enter a nonnegative value")
                        continue
                    break
                except ValueError:
                    print("Enter a float value")
            while True:
                cs = input("Connection Status? ")
                try:
                    cs = float(cs)
                    if (cs < 0):
                        print("Enter a nonnegative value")
                        continue
                    break
                except ValueError:
                    print("Enter a float value")

            trc.add('throughput', 'rtt', 'connection_status', tp, rtt, cs)
            count = count + 1
    except KeyboardInterrupt:
        pass

    print ("")
    print ("")
    print ("You have entered ",count," test results.")
    trc.prnt('throughput')
    trc.prnt('rtt')
    trc.prnt('connection_status')

#    avg = trc.avg('throughput')
#    std = trc.std('throughput')
#    print ("The average and standard deviation of Throughput are ",avg," and ",std)
#    avg = trc.avg('rtt')
#    std = trc.std('rtt')
#    print ("The average and standard deviation of RTT are ",avg," and ",std)
#    avg = trc.avg('connection_status')
#    std = trc.std('connection_status')
#    print ("The average and standard deviation of Connection Status are ",avg," and ",std)
