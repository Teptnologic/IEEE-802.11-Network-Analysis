from math import log
import random
import host
import frame

# constants
# a host can sense the channel every 0.01 msec
BASE_TIME = 100  # 0.01 ms * BASE_TIME = 1 ms
ACK_PROCESS_TIME = 64 * 8 / (11 * (10 ** 6)) * (10 ** 3) * BASE_TIME
DEFAULT_DIFS = 0.1 * BASE_TIME  # 0.1 ms
DEFAULT_SIFS = 0.05 * BASE_TIME  # 0.05 ms
DEFAULT_BACKOFF = 1 * BASE_TIME  # TODO: use actual number

BITS_PER_BYTE = 8
WIRELESS_CAPACITY = (11 * (10 ** 6))  # 11 Mbps
SENSE_CHANNEL_INTERVAL = 100  # 0.01 ms

# configurations
# backoff_time_cap = float(input("Please enter the backoff time cap (ms): "))
backoff_time_cap = 10
# arrival_rate = float(input("Please enter the arrival rate: "))
arrival_rate = 0.1
# number_of_host = int(input("Please enter number of hosts: "))
number_of_host = 10


def generate_frame_size():
    u = random.random()
    return ((-1 / 1544) * log(1 - u)) * BITS_PER_BYTE


def generate_arrival_time():
    u = random.random()
    return ((-1 / arrival_rate) * log(1 - u)) * (10 ** 3) * BASE_TIME


def generate_backoff_time():
    u = random.random()
    return u * backoff_time_cap * BASE_TIME


def generate_process_time():
    return generate_frame_size() / WIRELESS_CAPACITY * (10 ** 3) * BASE_TIME


def generate_destination():
    u = random.random()
    return int(u * number_of_host)


# statistics
conflict_times = 0

# initializations
hosts = []
arrival_times = []
channel = []
for i in range(number_of_host):
    hosts.append(host.Host(DEFAULT_DIFS, DEFAULT_SIFS))
    arrival_times.append(generate_arrival_time())

# main
for current_time in range(10 * (10 ** 3) * BASE_TIME):
    channel_is_idle = len(channel) == 0
    channel_has_conflicts = len(channel) > 1
    # update statistics
    if channel_has_conflicts:
        conflict_times += 1
    # schedule data frames
    for i in range(number_of_host):
        current_host = hosts[i]
        arrival_time = arrival_times[i]
        if arrival_time <= 0:
            data_frame = frame.Frame(
                generate_process_time(),
                i,
                generate_destination(),
                False
            )
            current_host.schedule(data_frame)
            arrival_times[i] = generate_arrival_time()
        else:
            arrival_times[i] -= 1
    # update frames in channel
    for current_frame in channel:
        current_frame.process_time -= 1
        current_frame.is_dirty = channel_has_conflicts
        if current_frame.process_time <= 0:
            ack_frame = frame.Frame(
                generate_process_time(),
                current_frame.destination,
                current_frame.source,
                True,
            )
            hosts[current_frame.destination].schedule(ack_frame)
    # remove delivered frames in channel
    channel[:] = [x for x in channel if x.process_time > 0]
    # send frames
    for current_host in hosts:
        data_frame = current_host.sent_frame(
            channel_is_idle,
            generate_backoff_time()
        )
        if data_frame is not None:
            channel.append(data_frame)
            current_host.reset(DEFAULT_DIFS, DEFAULT_SIFS)

# results
print(conflict_times)
