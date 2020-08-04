import numpy as np
import matplotlib.pyplot as plt

measurements = np.load("speed_benchmark_VM-Udoo.npz")

m = dict()
m["send_freq"] = measurements["send_freq"]
m["recv_freq"] = measurements["recv_freq"]


fig = plt.figure()

plt.plot(m["recv_freq"])

plt.xlim([0, len(m["recv_freq"])])

plt.xlabel("Tick", fontsize=14)
plt.ylabel("Recieving messages/s", fontsize=14)

plt.title(f"Send avg. {measurements['send_freq']:.2f} messages/s, recieve avg. {measurements['recv_freq'].mean():.2f} messages/s @ 1E6 messages with 128byte")

plt.grid(True)

plt.show()