import numpy as np
import matplotlib.pyplot as plt

a = np.loadtxt("/home/zhangh/MyProject/FreqJ/FJ/result_test.mat", delimiter=",")

c_min, c_max = 150, 600
delta, npts = 0.01, 800
f_min, f_max = 1/(npts*delta), 1
extent = [f_min, f_max, c_min, c_max]

for i in range(len(a)):
    for j in range(len(a[0])):
        if a[i][j] < 0:
            a[i][j] = 0

a = a/np.max(a)
plt.imshow(a.T, extent=extent, aspect='auto', origin='lower')
plt.colorbar()
plt.xlabel('Frequency(Hz)')
plt.ylabel('Phase Velocity(m/s)')
plt.show()
