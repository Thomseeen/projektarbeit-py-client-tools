import numpy as np
import matplotlib.pyplot as plt

measurements = np.load("delay_benchmark_VM-Udoo-10kHz.npz")

m = dict()
m["recv_timestamps"] = measurements["recv_timestamps"]
m["send_timestamps"] = measurements["send_timestamps"]

delays = m["recv_timestamps"] - m["send_timestamps"]


fig = plt.figure()

plt.plot(delays*1000)

plt.xlim([0, len(delays)])
plt.ylim([0, 50])

plt.xlabel("Message no.", fontsize=14)
plt.ylabel("Delay in ms", fontsize=14)

plt.title(f"Delay avg. {delays.mean()*1000:.2f} ms @ 1E5 messages with 128byte and 10kHz sending-rate")

plt.grid(True)

plt.show()