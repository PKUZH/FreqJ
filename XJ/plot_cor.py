import matplotlib.pyplot as plt
import numpy as np
import os
from obspy.core import *

sacfile_list = open('dist.dat')
os.chdir('/home/zhangh/Data/cor_pws')

tscale = np.linspace(-150,150,1501)
sacfile = sacfile_list.readline()
fig = plt.subplot(111)
count = 0
while sacfile:
    if count%20==0: 
        dist, st1, st2 = sacfile.split()
        dist = float(dist)
        sacfile_name = 'COR_'+st1+'_'+st2+'.SAC'
        st = read(sacfile_name)
        data = st[0].data[750:2251]
        dmax = max(data)
        data_plot = [ i*10/dmax+dist for i in data]
        fig.plot(tscale,data_plot,'black')
    sacfile = sacfile_list.readline()
    count = count+1
fig.set_xlabel('Time/s', fontsize=15)
fig.set_ylabel('Distance/km', fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.show()
sacfile_list.close()
