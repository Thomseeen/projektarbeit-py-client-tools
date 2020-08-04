import numpy as np
import matplotlib.pyplot as plt

measurements = np.load("delay_benchmark_BBB-Udoo-1kHz.npz")

m = dict()
m["recv_timestamps"] = measurements["recv_timestamps"]
m["send_timestamps"] = measurements["send_timestamps"]

delays = m["recv_timestamps"] - m["send_timestamps"]


fig = plt.figure(figsize=(12, 8), dpi=80)

plt.plot(delays*1000)

plt.xlim([0, len(delays)])
#plt.ylim([0, 50])

plt.xlabel("Message no.", fontsize=20)
plt.ylabel("Delay in ms", fontsize=20)

plt.xticks(fontsize=14, color="grey")
plt.yticks(fontsize=14, color="grey")

plt.title(f"Delay avg. {delays.mean()*1000:.2f} ms @ 1E4 messages with 128byte and 1kHz sending-rate", fontsize=18)

plt.grid(True)

plt.show()