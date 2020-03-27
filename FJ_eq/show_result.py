import numpy as np
import matplotlib.pyplot as plt

a = np.loadtxt("/home/zhangh/MyProject/FreqJ/FJ_eq/result_test.mat", delimiter=",")

c_min, c_max = 3.1, 4.7
delta, npts = 0.1, 4096
f_min, f_max = 1/(npts*delta), 0.5
extent = [f_min, f_max, c_min, c_max]
for i in range(len(a)):
    for j in range(len(a[0])):
        if a[i][j] < 0:
            a[i][j] = 0
        if np.max(a[i])>0:
            a[i]=a[i]/np.max(a[i])
# a = a/np.max(a)
plt.imshow(a.T, extent=extent, aspect='auto', origin='lower')
plt.colorbar()
plt.xlabel('Frequency(Hz)')
plt.ylabel('Phase Velocity(m/s)')
plt.show()
