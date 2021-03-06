from obspy.core import *
import numpy as np
import os
import itertools
import multiprocessing
from scipy.special import jn
from scipy.integrate import *
import sys
import norm


# function B is the integral of J0
def b_int(r1, r2):
    j_0 = lambda x: jn(0, x)
    b_result = quad(j_0, r1, r2)
    return b_result[0]


# calculate the frequency-Bessel spectrogram
def calculate_i(w, c, g_rw, r):
    r_size = len(r)
    d_r = r[1]-r[0]
    k = w/c
    i_result = (g_rw[-1]*r[-1]*jn(1, k*r[-1]) - g_rw[0]*r[0]*jn(1, k*r[0]))/k
    for i in range(r_size-1):
        rl = r[i]
        ru = r[i+1]
        b = (g_rw[i+1]-g_rw[i])/d_r
        i_result += b*(ru*jn(0, k*ru)-rl*jn(0, k*rl))/k**2 - b_int(k*rl, k*ru)*b/k**3
    return i_result


def read_sac(gf_index):
    if gf_index < 10:
        return read('fz.tz_000'+str(gf_index)+'.SAC')
    elif gf_index < 100:
        return read('fz.tz_00'+str(gf_index)+'.SAC')
    else:
        return read('fz.tz_0'+str(gf_index)+'.SAC')


gf_path = '/home/zhangh/Data/GFs/model_shallow/gzz'
os.chdir(gf_path)

# number of green functions, delta t & npts
gf_num, delta, npts = 500, 0.01, 800
c_min, c_max, dc = 150, 600, 0.2
r_min, r_max, dr = 1, 100, 1 
f_min, f_max, df = 1/(npts*delta), 25, 1/(npts*delta)

c_scale = np.linspace(c_min, c_max, int((c_max-c_min)/dc)+1)
r_scale = np.linspace(r_min, r_max, int((r_max-r_min)/dr)+1)
f_scale = np.linspace(f_min, f_max, int((f_max-f_min)/df)+1)
nf, nc = len(f_scale), len(c_scale)
I_wc = np.zeros((nf, nc))


G_rw = np.zeros((gf_num, nf))
for i in range(gf_num):
    st = read_sac(i+1)
    data = st[0].data
    data = data[0:npts]
    # normalize method
    # data = norm.norm_one(data)
    g_f = np.imag(np.fft.rfft(data))/npts
    G_rw[i] = g_f[1:nf+1]


def func(params):
    index = params[0]
    w = params[2][index]*2*np.pi
    g_w = params[3][:, index]
    c = params[1]
    r_scale_ = params[4]
    return calculate_i(w, c, g_w, r_scale_)


# multiple processing
param_list = list(itertools.product(range(nf), c_scale, [f_scale], [G_rw], [r_scale]))
pool = multiprocessing.Pool(processes=30)
cnt = 0
for y in pool.imap(func, param_list):
    i = int(cnt / nc)
    j = int(cnt % nc)
    I_wc[i][j] = y
    cnt = cnt+1
    sys.stdout.write('done %d/%d\r' % (cnt, len(param_list)))


np.savetxt("/home/zhangh/MyProject/FreqJ/FJ/result_shallow.mat", I_wc, fmt="%.5e", delimiter=",")
