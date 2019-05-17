from TestResultContainer import TestResultContainer

if __name__ == "__main__":
    trc = TestResultContainer()     #create object
    count = 0                       #initialize counter
    try:
        while True:
            print("")
            print ("Input values from a single test:")
            while True:
                tp = input("Throughput? ")      #get user input
                try:
                    tp = float(tp)
                    if (tp < 0):
                        print("Enter a nonnegative value") #error checking
                        continue
                    break
                except ValueError:
                    print("Enter a float value")    #error checking
            while True:
                rtt = input("RTT? ")        #get user input
                try:
                    rtt = float(rtt)
                    if (rtt < 0):
                        print("Enter a nonnegative value")  #error checking
                        continue
                    break
                except ValueError:
                    print("Enter a float value")    #error checking
            while True:
                cs = input("Connection Status? ")       #get user input
                try:
                    cs = float(cs)
                    if (cs < 0):
                        print("Enter a nonnegative value")  #error checking
                        continue
                    break
                except ValueError:
                    print("Enter a float value")    #error checking

            trc.add('Throughput', 'RTT', 'Connection_Status', tp, rtt, cs)
                    #add input results to the dictionary
            count = count + 1       #increase counter
    except KeyboardInterrupt:
        pass

    trc.write_to_json(trc.my_dict) #write to json file

    print ("")      #print output
    print ("")
    print ("You have entered ",count," test results.")
    trc.prnt('Throughput')
    trc.prnt('RTT')
    trc.prnt('Connection_Status')
