import random
from time import time, sleep

import numpy as np
import paho.mqtt.client as mqtt


BROKER = "192.168.178.16"
MESSAGES_CNT = 1000000
PAYLOAD_LEN = 128
TOPIC = "test"

rcpt_counter = 0

measurements = dict()
measurements["send_freq"] = 0.0
measurements["recv_freq"] = list()

def on_disconnect(client, userdata, rc):
    global measurements
    elapsed = time() - T0
    print(f"Sending {MESSAGES_CNT / elapsed} massages/s")
    measurements["send_freq"] = MESSAGES_CNT / elapsed

def on_message(client, userdata, msg):
    global T1, rcpt_counter, measurements
    rcpt_counter += 1
    if rcpt_counter % 1000 == 0:
        T2 = time()
        print(f"Receiveing {1000 / (T2 - T1)} messages/s")
        measurements["recv_freq"].append(1000 / (T2 - T1))
        T1 = T2

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
ramdom_strings = [''.join(chr(random.getrandbits(8)) for _ in range(PAYLOAD_LEN)) for _ in range(MESSAGES_CNT)]

T0 = T1 = time()

for string in ramdom_strings:
    sending_client.publish(TOPIC, string)

sending_client.disconnect()

sleep(20)
listening_client.disconnect()

np.savez("speed_benchmark.npz",
    send_freq=np.array(measurements["send_freq"]),
    recv_freq=np.array(measurements["recv_freq"]))
        