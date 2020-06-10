import numpy as np
import matplotlib.pyplot as plt

a = np.loadtxt("/home/zhangh/MyProject/FreqJ/XJ/result_raw.mat", delimiter=",")

c_min, c_max = 3, 4.4
delta, npts = 0.2, 1500
f_min, f_max = 1/(npts*delta), 0.5
extent = [f_min, f_max, c_min, c_max]

for i in range(len(a)):
    for j in range(len(a[0])):
        if a[i][j] > 0:
            a[i][j] = 0
        else:
            a[i][j] = -a[i][j]
    if np.max(a[i])>0:
        a[i] = a[i]/np.max(a[i])

plt.imshow(a.T, extent=extent, aspect='auto', origin='lower')
plt.colorbar()
plt.xlabel('Frequency(Hz)')
plt.ylabel('Phase Velocity(m/s)')
plt.show()
