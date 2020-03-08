from obspy.core import *
import matplotlib.pyplot as plt
import os

path = os.path.abspath('..')
gf_path = path+'/GFs/model2'
os.chdir(gf_path)

npts = 4000
delta = 0.0125
t_scale = [i*delta for i in list(range(npts))]
p1 = plt.subplot(111)
for i in range(500):
    d = i+1
    if d < 10:
        st = read('fz.tz_000'+str(d)+'.SAC')
    elif d < 100:
        st = read('fz.tz_00'+str(d)+'.SAC')
    else:
        st = read('fz.tz_0'+str(d)+'.SAC')

    # st = st.filter('lowpass', freq = 25.0)

    data = st[0].data[0:npts]
    data_plot = data*10e8+d
    p1.plot(t_scale, data_plot, lw=0.5, color='black')
plt.show()
