from obspy.core import *
import matplotlib.pyplot as plt
import os


def norm(data):
    for i in range(len(data)):
        if data[i] > 0:
            data[i] = 1
        elif data[i] < 0:
            data[i] = -1
        else:
            data[i] = 0
    return data


gf_path = '/home/zhangh/Data/GFs/model_shallow/gzz'
os.chdir(gf_path)

npts = 512
delta = 0.01
t_scale = [i*delta for i in list(range(npts))]
p1 = plt.subplot(111)
for i in range(10, 500, 20):
    d = i+1
    if d < 10:
        st = read('fz.tz_000'+str(d)+'.SAC')
    elif d < 100:
        st = read('fz.tz_00'+str(d)+'.SAC')
    else:
        st = read('fz.tz_0'+str(d)+'.SAC')

    # st = st.filter('lowpass', freq = 25.0)

    data = st[0].data[0:npts]
    # data = norm(data)
    data_plot = [i*10e9+d for i in data]
    p1.plot(t_scale, data_plot, lw=1, color='black')
plt.xlabel('Time/s', size=15)
plt.ylabel('Distance/m', size=15)
plt.show()
