import math
import os
import random
import matplotlib.pyplot as plt
import numpy as np

# Constants. Radius of tubes
r_N2_out1 = 20
r_N2_in1 = 22
r_N2_in2 = 68
r_N2_out2 = 70
r_NH3_2 = 90

Flow_GaCl = 100  # sccm
Flow_N2 = 2000
Flow_NH3 = 1500

# Reading number of iterations. Recommended not less than 10**7
N = int(input("Enter the value of N: "))

# Variables. Diffusion
mc = 1
D = 1.5
dt = 1.0e-5
dl = math.sqrt(12 * D * 100 * dt)

# Initial coordinates
x = 45
y = 10

# Flow speed
v_N2 = (Flow_N2 + Flow_GaCl) * 1000.0 / 60.0 * 1300.0 / 300.0 / (math.pi * (r_N2_in2 - 45) ** 2)
v_NH3 = Flow_NH3 * 1000.0 / 60.0 * 1300.0 / 300.0 / (math.pi * ((r_NH3_2 - 45) ** 2 - (r_N2_out2 - 45) ** 2))

# Initialize array
a = [[0.0 for _ in range(631)] for _ in range(631)]

for mc in range(1, N + 1):
    if (x < r_N2_in2) and (x > r_N2_in1):
        v = v_N2
    else:
        v = v_NH3

    y = y + dt * v
    xp = x + dl * (random.random() - 0.5)
    yp = y + dl * (random.random() - 0.5)

    ok = 1

    if xp < 0 or xp > r_NH3_2:
        ok = 0

    if yp < 10:
        if (xp > r_N2_in2) and (xp < r_N2_out2):
            ok = 0
        if (xp < r_N2_in1) and (xp > r_N2_out1):
            ok = 0

    if yp < 0 or yp > 90:
        ok = 0

    if ok == 1:
        x = xp
        y = yp
    else:
        x = (42 * random.random() + 24)
        y = 10

    xi = round(x * 7)
    yi = round(y * 7)

    if 0 <= xi <= 630 and 0 <= yi <= 630:
        a[xi][yi] += 1 / N

# Save the result to a file
current_directory = os.path.dirname(os.path.abspath(__file__))
file_name = "diff_GaCl_no_tube.txt"
file_path = os.path.join(current_directory, file_name)
with open(file_path, 'w') as file:
    for i in range(631):
        for j in range(631):
            file.write(f"{a[i][j]:12.9f} ")
        file.write("\n")

print(f"Results saved to {file_path}")


# Read the data from the file
with open(file_path, 'r') as file:
    data = [line.strip().split() for line in file]

# Convert data to a numpy array
data = np.array(data, dtype=float)

# Plot the data
plt.imshow(data, cmap='hot', interpolation='nearest')
plt.colorbar()
plt.title('Simulation Results')
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.show()

