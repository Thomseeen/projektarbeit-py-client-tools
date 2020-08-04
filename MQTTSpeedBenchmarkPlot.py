import numpy as np
import matplotlib.pyplot as plt

measurements = np.load("speed_benchmark_BBB-Udoo.npz")

m = dict()
m["send_freq"] = measurements["send_freq"]
m["recv_freq"] = measurements["recv_freq"]


fig = plt.figure(figsize=(12, 8), dpi=80)

plt.plot(m["recv_freq"])

plt.xlim([0, len(m["recv_freq"])])

plt.xticks(fontsize=14, color="grey")
plt.yticks(fontsize=14, color="grey")

plt.xlabel("Tick", fontsize=20)
plt.ylabel("Recieving messages/s", fontsize=20)

plt.title(f"Send avg. {measurements['send_freq']:.2f} messages/s, recieve avg. {measurements['recv_freq'].mean():.2f} messages/s\n@ 1E5 messages with 128byte", fontsize=18)

plt.grid(True)

plt.show()