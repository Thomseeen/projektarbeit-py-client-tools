import paho.mqtt.client as mqtt
from time import time, sleep
import random


BROKER = "192.168.178.16"
MESSAGES_CNT = 100000
PAYLOAD_LEN = 128
TOPIC = "test"

rcpt_counter = 0

def on_disconnect(client, userdata, rc):
    elapsed = time() - T0
    print(f"Sending {MESSAGES_CNT / elapsed} massages/s")

def on_message(client, userdata, msg):
    global T1, rcpt_counter
    rcpt_counter += 1
    if rcpt_counter % 1000 == 0:
        T2 = time()
        print(f"Receiveing {1000 / (T2 - T1)} messages/s")
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