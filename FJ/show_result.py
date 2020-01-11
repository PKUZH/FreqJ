import numpy as np
import matplotlib.pyplot as plt
a = np.loadtxt("/home/zhangh/MyProject/FreqJ/FJ/result0.mat",delimiter=",")
cmin,cmax = 100,600
delta,npts = 0.0125,2048
fmin,fmax = 1/(npts*delta),25
extent = [fmin,fmax,cmin,cmax]
#a = np.vstack((a0,a1,a2))
for i in range(len(a)):
    for j in range(len(a[0])):
        if a[i][j]<0:
            a[i][j]=0
a = a/np.max(a)
plt.imshow(a.T,extent=extent,aspect='auto',origin='lower')
plt.colorbar()
plt.xlabel('Frequency(Hz)')
plt.ylabel('Phase Velocity(m/s)')
plt.show()
