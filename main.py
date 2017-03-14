import GEL
import event
import packet
import host

# SIFS = 0.05 msec and DIFS = 0.1 msec. Your CSMA/CA implementation can sense the channel every 0.01 msec.
# the wireless channel capacity is 11 Mbps
# arrival_rate = float(input("Please enter the arrival rate: "))
arrival_rate = 0.1
# number_of_host = int(input("Please enter number of hosts: "))
number_of_host = 10

host_list = list()

for i in range(number_of_host):
    host_list.append(host.host(arrival_rate))

for i in range(100000):  # 100000 msec
    for host in host_list:
        # do stuff
