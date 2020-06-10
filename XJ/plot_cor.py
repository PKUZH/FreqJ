import matplotlib.pyplot as plt
import numpy as np
import os
from obspy.core import *

sac_file_list = open('dist.dat')
os.chdir('/home/zhangh/Data/cor_pws')

t_scale = np.linspace(-150, 150, 1501)
sac_file = sac_file_list.readline()
fig = plt.subplot(111)
count = 0
while sac_file:
    if count % 20 == 0:
        dist, st1, st2 = sac_file.split()
        dist = float(dist)
        sac_file_name = 'COR_'+st1+'_'+st2+'.SAC'
        st = read(sac_file_name)
        data = st[0].data[750:2251]
        d_max = max(data)
        data_plot = [i*10/d_max+dist for i in data]
        fig.plot(t_scale, data_plot, 'black')
    sac_file = sac_file_list.readline()
    count = count+1
fig.set_xlabel('Time/s', fontsize=15)
fig.set_ylabel('Distance/km', fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.show()
sac_file_list.close()
