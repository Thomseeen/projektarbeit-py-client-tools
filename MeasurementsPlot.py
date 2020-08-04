import numpy as np
import matplotlib.pyplot as plt

measurements = np.load("measurements.npz")

print(f"Got measurements  {measurements}")
print(f"First entry value is {measurements['value'][0][0]}")

deltas = np.zeros((measurements["seq_no"].shape[0], measurements["seq_no"].shape[1]), dtype=np.float)

m = dict()
m["seq_no"] = measurements["seq_no"]
m["value"] = measurements["value"]
m["time"] = measurements["time"]

for pin_no in range(m["seq_no"].shape[0]):
    for index in range(m["seq_no"].shape[1] - 1):
        if m["seq_no"][pin_no, index] + 1 != m["seq_no"][pin_no, index + 1]:
            print(f"Missing seq_no {m['seq_no'][pin_no, index] + 1} for pin {pin_no}")
        deltas[pin_no, index] = m["time"][pin_no, index + 1] - m["time"][pin_no, index]
        
print(f"Average delta between measurements for all pins: {deltas.mean()}")

fig, axes = plt.subplots(m["seq_no"].shape[0], 2)

for pin_no, ax in enumerate(axes):
        ax[0].plot(m["seq_no"][pin_no, :])
        ax[1].plot(deltas[pin_no])

plt.show()
