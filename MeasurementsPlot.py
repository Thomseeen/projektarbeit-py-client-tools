import numpy as np
import matplotlib.pyplot as plt

measurements = np.load("measurements.npz")

print(f"Got measurements  {measurements}")
print(f"First entry value is {measurements['value'][0][0]}")

m = dict()
m["seq_no"] = measurements["seq_no"]
m["value"] = measurements["value"]
m["time"] = measurements["time"]

deltas = np.zeros((m["seq_no"].shape[0], m["seq_no"].shape[1]), dtype=np.float)

for pin_no in range(m["seq_no"].shape[0]):
    for index in range(m["seq_no"].shape[1] - 1):
        if m["seq_no"][pin_no, index] + 1 != m["seq_no"][pin_no, index + 1]:
            print(f"Missing seq_no {m['seq_no'][pin_no, index] + 1} for pin {pin_no}")
        deltas[pin_no, index] = m["time"][pin_no, index + 1] - m["time"][pin_no, index]
        

fig = plt.figure(figsize=(12, 8), dpi=80)

for pin_no in range(deltas.shape[0]):
        plt.plot(deltas[pin_no] * 1000)

plt.xlim([0, len(deltas[0])])

plt.xlabel("Measurement no.", fontsize=20)
plt.ylabel("Delta to last measurement in ms", fontsize=20)

plt.xticks(fontsize=14, color="grey")
plt.yticks(fontsize=14, color="grey")

plt.title(f"Delta avg. {deltas.mean()*1000:.2f} ms @ 2E5 measurements per pin at 100Hz samplerate", fontsize=18)

plt.grid(True)

plt.show()
