import numpy as np

with open("measurements.npy", "rb") as file:
  measurements = np.load(file)

print(f"Faking wrong index {measurements[0, 1111, 0]}")
measurements[2, 2222, 0] += 1

with open("measurements.npy", "wb") as file:
    np.save(file, measurements)