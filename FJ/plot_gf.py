from obspy.core import *
import matplotlib.pyplot as plt
import os
def norm(data):
    for i in range(len(data)):
        if data[i]>0:
            data[i] = 1
        elif data[i]<0:
            data[i] = -1
        else:
            data[i] = 0
    return data

path = os.path.abspath('..')
gf_path = path+'/GFs/model2'
os.chdir(gf_path)

npts = 4000
delta = 0.0125
t_scale = [i*delta for i in list(range(npts))]
p1 = plt.subplot(111)
for i in range(110,121):
    d = i+1
    if d < 10:
        st = read('fz.tz_000'+str(d)+'.SAC')
    elif d < 100:
        st = read('fz.tz_00'+str(d)+'.SAC')
    else:
        st = read('fz.tz_0'+str(d)+'.SAC')

    # st = st.filter('lowpass', freq = 25.0)

    data = st[0].data[0:npts]
    data = norm(data)
    data_plot = [i/5+d for i in data]
    p1.plot(t_scale, data_plot, lw=0.5, color='black')
plt.show()
