import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

measurements = np.load("measurements_BBB-BBB-100Hz.npz")

print(f"Got measurements  {measurements}")
print(f"First entry value is {measurements['value'][0][0]}")

m = dict()
m["seq_no"] = measurements["seq_no"]
m["value"] = measurements["value"]
m["time"] = measurements["time"]

deltas = np.zeros((m["seq_no"].shape[0], m["seq_no"].shape[1] - 1), dtype=np.float)

for pin_no in range(m["seq_no"].shape[0]):
    deltas[pin_no] = np.diff(m["time"][pin_no]) * 1000


fig = plt.figure(figsize=(12, 8), dpi=80)

sns.distplot(deltas, bins=100)
plt.xlim([0, 30])

plt.xlabel("Delta to last measurement in ms", fontsize=20)
plt.ylabel("Density", fontsize=20)

plt.xticks(fontsize=14, color="grey")
plt.yticks(fontsize=14, color="grey")

plt.title(f"99% percentile {np.percentile(deltas, 99.7):.2f} ms\n@ 2E5 measurements per pin at 100Hz samplerate", fontsize=18)

plt.grid(True)

plt.show()