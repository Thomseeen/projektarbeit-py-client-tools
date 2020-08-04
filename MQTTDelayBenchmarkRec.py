from time import time, sleep

import random
import numpy as np
import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt


BROKER = "192.168.178.16"
MESSAGES_CNT = 10000
PAYLOAD_LEN = 256
SEND_PERIOD = 0.001 # seconds
TOPIC = "test"

recv_counter = 0

def on_disconnect(client, userdata, rc):
    print(f"Finished sending")

def on_message(client, userdata, msg):
    global recv_timestamps, recv_counter
    recv_timestamps[recv_counter] = time()
    recv_counter += 1

sending_client = mqtt.Client()
sending_client.on_disconnect = on_disconnect
sending_client.connect(BROKER)
sending_client.loop_start()

listening_client = mqtt.Client()
listening_client.connect(BROKER)
listening_client.on_message = on_message
listening_client.subscribe(TOPIC)
listening_client.loop_start()

# Create some random data
random_strings = [''.join(chr(random.getrandbits(8)) for _ in range(PAYLOAD_LEN)) for _ in range(MESSAGES_CNT)]

# Structure to hold timestamps
send_timestamps = np.zeros(MESSAGES_CNT)
recv_timestamps = np.zeros(MESSAGES_CNT)


for ii, string in enumerate(random_strings):
    sleep(SEND_PERIOD)
    send_timestamps[ii] = time()
    sending_client.publish(TOPIC, string)

sending_client.disconnect()
sleep(SEND_PERIOD * MESSAGES_CNT * 2)
listening_client.disconnect()

np.savez("delay_benchmark_VM-Udoo-1kHz.npz",
    recv_timestamps=recv_timestamps,
    send_timestamps=send_timestamps)
