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
def calculate_i(w, c, g_rw, r, dr):
    r_size = len(r)
    k = w/c
    i_result = (g_rw[-1]*r[-1]*jn(1, k*r[-1]) - g_rw[0]*r[0]*jn(1, k*r[0]))/k
    for i in range(r_size-1):
        rl = r[i]
        ru = r[i+1]
        b = (g_rw[i+1]-g_rw[i])/dr[i]
        i_result += b*(ru*jn(0, k*ru)-rl*jn(0, k*rl))/k**2-b*b_int(k*rl,k*ru)/k**3
    return i_result


delta, npts = 0.2, 1500
c_min, c_max, dc = 3, 4.4, 0.005
f_min, f_max, df = 1/(npts*delta), 0.5, 1/(npts*delta)
c_scale = np.linspace(c_min, c_max, int((c_max-c_min)/dc)+1)
f_scale = np.linspace(f_min, f_max, int((f_max-f_min)/df)+1)
nf, nc = len(f_scale), len(c_scale)
I_wc = np.zeros((nf, nc))

# read sac file
sacfile_list = open('get_dist/dist_s.dat')
r_scale, st1s, st2s = [], [], []
gf_num = 0
sacfile = sacfile_list.readline()
while sacfile:
    if gf_num == 0:
        r_scale.append(float(sacfile.split()[0]))
        st1s.append(sacfile.split()[1])
        st2s.append(sacfile.split()[2])
        gf_num = gf_num + 1
    else:
        dist = float(sacfile.split()[0])
        if dist - r_scale[-1] > 0.01:
            r_scale.append(dist)
            st1s.append(sacfile.split()[1])
            st2s.append(sacfile.split()[2])
            gf_num = gf_num + 1
    sacfile = sacfile_list.readline()
sacfile_list.close()

gf_path = '/home/zhangh/Data/cor_pws'
os.chdir(gf_path)

d_r = [r_scale[i+1]-r_scale[i] for i in range(gf_num-1)]
G_rw = np.zeros((gf_num, nf))
for i in range(gf_num):
    sacfile_name = 'COR_'+st1s[i]+'_'+st2s[i]+'.SAC'
    st = read(sacfile_name)
    data = st[0].data
    data = data[1501:1501+npts]
    dist = r_scale[i]
    c_b, c_e = c_min, c_max
    win_b, win_e =int(dist/(c_e*delta)), int(dist/(c_b*delta))
    # data = norm.norm_win(data,win_b,win_e)
    g_f = np.imag(np.fft.rfft(data))/npts
    G_rw[i] = g_f[1:nf+1]


def func(params):
    index = params[0]
    w = params[2][index]*2*np.pi
    g_w = params[3][:, index]
    c = params[1]
    r_scale_ = params[4]
    d_r_ = params[5]
    return calculate_i(w, c, g_w, r_scale_, d_r_)


# multiple processing
param_list = list(itertools.product(range(nf), c_scale, [f_scale], [G_rw], [r_scale], [d_r]))
pool = multiprocessing.Pool(processes=40)
cnt = 0
for y in pool.imap(func, param_list):
    i = int(cnt / nc)
    j = int(cnt % nc)
    I_wc[i][j] = y
    cnt = cnt+1
    sys.stdout.write('done %d/%d\r' % (cnt, len(param_list)))

np.savetxt("/home/zhangh/MyProject/FreqJ/XJ/result_s_raw.mat", I_wc, fmt="%.5e", delimiter=",")
