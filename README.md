# IEEE-802.11-Network-Analysis

1. After sending out a packet, the transmission for the sender will pause until it receives an ACK for previously sent frame. But, the sender should not wait forever. So, there will be a time-out period, after which the sender re-transmits the packet. Explore the time-out values of 5ms, 10ms, 15ms and see how it affects the network.

2. After a few number of re-transmissions, if there is no ACK received, the sender will discard the frame. Maximum number of re-transmissions is 3 for our study.

3. ACK should be put on the back of the queue.

4. Random back-off timer would sense the channel every 0.01 ms. If the channel is free, counter value counts down. If the channel is busy, the counter value remains unchanged.
