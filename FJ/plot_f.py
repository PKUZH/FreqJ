from obspy.core import *
import numpy as np
import matplotlib.pyplot as plt
import os

path = os.path.abspath('..')
gf_path = path+'/GFs/model2'
os.chdir(gf_path)

npts = 4000
delta = 0.0125
f_max = 1/(2*delta)
f_scale = np.linspace(0, f_max, int(npts/2)+1)
t_scale = [i*delta for i in list(range(npts))]
d = 1
p1 = plt.subplot(111)
while d <= 100:
    if d < 10:
        st = read('fz.tz_000'+str(d)+'.SAC')
    elif d < 100:
        st = read('fz.tz_00'+str(d)+'.SAC')
    else:
        st = read('fz.tz_0'+str(d)+'.SAC')
    st = st.filter('lowpass', freq=25.0)
    data = st[0].data[0:npts]
    g_f = np.imag(np.fft.rfft(data))/npts
    p1.plot(f_scale, g_f, lw=0.2, color='black')
    d = d+1
plt.show()
