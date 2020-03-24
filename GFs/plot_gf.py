from obspy.core import *
import matplotlib.pyplot as plt
import os
import norm

path = os.path.abspath('.')
gf_path = path+'/model_deep/deep_sac/'
os.chdir(gf_path)

npts = 1024
delta = 0.25
norm_win = int(3/delta)
t_scale = [i*delta for i in list(range(npts))]
p1 = plt.subplot(111)
for i in range(80):
    d = (i+1)*5
    if i < 9:
        st = read('seis.tz_000'+str(i+1)+'.SAC')
    elif i < 99:
        st = read('seis.tz_00'+str(i+1)+'.SAC')
    else:
        st = read('seis.tz_0'+str(i+1)+'.SAC')

    # st = st.filter('lowpass', freq = 25.0)

    data = st[0].data[0:npts]
    #data = norm.norm(data,norm_win)
    if i%5 == 0:
        data_plot = [data[i]*(10**1)+d for i in range(npts)]
        p1.plot(t_scale, data_plot, lw=0.5, color='black')
plt.show()
