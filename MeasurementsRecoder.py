import sys
import signal
import struct
import numpy as np
import paho.mqtt.client as mqtt


class MeasurementsRecoder:
    def __init__(self, address, port, client_id, topic, qos, keep_alive, measurements_cnt, active_adc_pins):
        self.measurements_cnt = measurements_cnt
        self.measurements_finished = 0
        self.measurements_indexer = np.zeros(active_adc_pins, dtype=np.int32)
        self.measurements = np.zeros((active_adc_pins, measurements_cnt, 2))

        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.topic = topic
        self.qos = qos
        
        self.active_adc_pins = active_adc_pins

        self.client.connect(address, port, keep_alive)

    def start(self):
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        self.client.subscribe(self.topic, qos=self.qos)

    def on_message(self, client, userdata, msg):
        try:
            # See adc_reading.h in simple-c-client why struct is packed like this
            data = struct.unpack("@HQBI", msg.payload)
            value = data[0] / 0xFFF0 * 1.8
            seq_no = data[1]
            pin_no = data[2]
            status = data[3]

            if self.measurements_indexer[pin_no] == self.measurements_cnt:
                self.measurements_finished += 1
                if self.measurements_finished == self.active_adc_pins:
                    self.client.disconnect()
                    with open("measurements.npy", "wb") as file:
                        np.save(file, self.measurements)
                return 0

            self.measurements[pin_no, self.measurements_indexer[pin_no], 0] = seq_no
            self.measurements[pin_no, self.measurements_indexer[pin_no], 1] = value
            self.measurements_indexer[pin_no] += 1

            if self.measurements_indexer[pin_no] % 1000 == 0:
                print(f"Pin {pin_no} is at {self.measurements_indexer[pin_no]} measurements")

        except Exception:
            import traceback
            print(traceback.format_exc())

    def signal_handler(self, sig, frame):
        self.client.disconnect()
        with open("measurements.npy", "wb") as file:
            np.save(file, self.measurements)
        print("Got interrupted, saving...")
        sys.exit(0)

if __name__ == "__main__":
    ADDRESS = "192.168.178.16"
    PORT = 1883
    CLIENTID = "mfd-py"
    TOPIC = "lfd1/#"
    QOS = 0
    KEEP_ALIVE = 30  # s
    MEASUREMENTS_CNT = 50000  # @100Hz per pin -> 500s = 8.3min, Wrap around of libpruio RB at 10000 per pin
    ACTIVE_ADC_PINS = 4

    measurements_recorder = MeasurementsRecoder(ADDRESS, PORT, CLIENTID, TOPIC, QOS, KEEP_ALIVE,
                                                MEASUREMENTS_CNT, ACTIVE_ADC_PINS)
                                              
    # Attach signal handler for SIGINT
    signal.signal(signal.SIGINT, measurements_recorder.signal_handler)

    measurements_recorder.start()