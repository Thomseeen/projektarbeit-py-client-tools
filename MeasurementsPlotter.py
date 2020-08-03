import numpy as np
import matplotlib.pyplot as plt

with open("measurements.npy", "rb") as file:
    measurements = np.load(file)

print(f"Got measurements with shape {measurements.shape}")
print(f"First entry is {measurements[0][0]}")

for pin_no in range(measurements.shape[0]):
    for index in range(measurements.shape[1] - 1):
        if measurements[pin_no, index, 0] + 1 != measurements[pin_no, index + 1, 0]:
            print(f"Missing seq_no {measurements[pin_no, index, 0] + 1} for pin {pin_no}")

fig, axes = plt.subplots(measurements.shape[0])

for pin_no, ax in enumerate(axes):
    ax.plot(measurements[pin_no, :, 0])

plt.show()
