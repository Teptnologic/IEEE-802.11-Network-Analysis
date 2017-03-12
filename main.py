from math import log, exp
import random
import queue

import GEL
import event
import packet

# configurations
MAXBUFFER = int(input("Please enter the MAXBUFFER size for the packets queue: "))
service_rate = float(input("Please enter the service rate: "))
arrival_rate = float(input("Please enter the arrival rate: "))

def generate_arrival_time():
    u = random.random()
    a = ((-1 / arrival_rate) * log(1 - u))
    return(1 * exp(a))
    # return a
def generate_service_time():
    u = random.random()
    return ((-1 / service_rate) * log(1 - u))
def generate_packet():
    return packet.Packet(generate_service_time())

# statistics
total_server_busy_time = 0
total_active_packets_length = 0
total_packet_queue_length = 0
total_packets = 0
total_active_packets = 0
total_dropped_packets = 0

current_time = 0
server_busy_start_time = -1

# initialize
packet_queue = queue.Queue(MAXBUFFER)
event_list = GEL.GEL()

# simulate
event_list.schedule("arrival", generate_arrival_time(), generate_packet())

for i in range(100000):
    event = event_list.pop()
    current_time = event.time
    # print(event.time)
    if event.type == "arrival":
        event_list.schedule("arrival", current_time + generate_arrival_time(), generate_packet())
        if total_active_packets == 0:
            total_active_packets_length += total_active_packets
            total_packet_queue_length += packet_queue.qsize()
            total_packets += 1
            event_list.schedule("departure", current_time + event.packet.service_time, event.packet)
            total_active_packets += 1
            if server_busy_start_time == -1:
                server_busy_start_time = current_time
        elif (total_active_packets < MAXBUFFER + 1) or (MAXBUFFER == 0):
            total_active_packets_length += total_active_packets
            total_packet_queue_length += packet_queue.qsize()
            total_packets += 1
            packet_queue.put(event.packet)
            total_active_packets += 1
        else:
            total_dropped_packets += 1
    elif event.type == "departure":
        total_active_packets -= 1
        if total_active_packets == 0:
            if server_busy_start_time != -1:
                total_server_busy_time += current_time - server_busy_start_time
                server_busy_start_time = -1
        if total_active_packets > 0:
            next_packet = packet_queue.get()
            event_list.schedule("departure", current_time + next_packet.service_time, next_packet)

if server_busy_start_time != -1:
    total_server_busy_time += current_time - server_busy_start_time

# results
print("--------------------------------------")
print("Server utilization:", end=' ')
print(total_server_busy_time / current_time)
print("Average active packets length:", end=' ')
print(total_active_packets_length / total_packets)
print("Average packets queue length:", end=' ')
print(total_packet_queue_length / total_packets)
print("Packet drop rate:", end=' ')
print(total_dropped_packets / total_packets)
print("Total Packet dropped:", end=' ')
print(total_dropped_packets)
print("--------------------------------------")
