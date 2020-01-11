from obspy.core import *
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import itertools
import multiprocessing
from scipy.special import jn
from scipy.integrate import *
import sys

def B(r):
    f = lambda x:jn(0,x)
    B = quad(f,0,r)
    return B[0]

def calculate_I(w,c,g_rw,r):
    rsize = len(r)
    dr = r[1]-r[0]
    I = 0
    k = w/c
    for i in range(rsize-1):
        rl = r[i]
        ru = r[i+1]
        b = (g_rw[i+1]-g_rw[i])/dr
        dI1 = g_rw[i+1]*ru*jn(1,k*ru)/k+b*(k*ru*jn(0,k*ru)-B(k*ru))/k**3
        dI2 = g_rw[i+1]*ru*jn(1,k*ru)/k+b*(k*rl*jn(0,k*rl)-B(k*rl))/k**3
        I = I+dI1-dI2
    return I

path = os.path.abspath('..')
gf_path = path+'/GFs/model2'
os.chdir(gf_path)

gf_num = 500
delta,npts = 0.0125,2048

G_rw = np.zeros((gf_num,int(npts/2)))
for i in range(gf_num):
    d = i+1
    if d <10:
        st = read('fz.tz_000'+str(d)+'.SAC')
    elif d<100:
        st = read('fz.tz_00'+str(d)+'.SAC')
    else:
        st = read('fz.tz_0'+str(d)+'.SAC')
    data = st[0].data
    data = data[0:npts]
    g_f = np.imag(np.fft.rfft(data))/npts
    G_rw[i] = g_f[1:]

cmin,cmax,dc = 150,600,0.5
rmin,rmax,dr = 1,500,1
fmin,fmax,df = 1/(npts*delta),25,1/(npts*delta)
c_scale = np.linspace(cmin,cmax,int((cmax-cmin)/dc)+1)
r_scale = np.linspace(rmin,rmax,int((rmax-rmin)/dr)+1)
f_scale = np.linspace(fmin,fmax,int((fmax-fmin)/df)+1)
nf,nc = len(f_scale),len(c_scale)
I_wc = np.zeros((nf,nc))
'''
num = 0
for i in range(len(f_scale)):
    w = f_scale[i]*2*np.pi
    g_rw = G_rw[:,i]
    for j in range(len(c_scale)):
        c = c_scale[j]
        I_wc[i,j] = calculate_I(w,c,g_rw,r_scale)
    num = num+1
    print(num)
    np.savetxt("/home/zhangh/MyProject/freqj/FJ/result0.mat", I_wc,fmt="%.3e", delimiter=",")
'''
paramlist = list(itertools.product(range(nf),c_scale,[f_scale],[G_rw],[r_scale]))
def func(params):
    i = params[0]
    w = params[2][i]*2*np.pi
    g_w = params[3][:,i]
    c = params[1]
    r_scale = params[4]
    return calculate_I(w,c,g_w,r_scale)

pool = multiprocessing.Pool(processes=56)
cnt = 0
for y in  pool.imap(func,paramlist):
    i = int(cnt/nc)
    j = int(cnt%nc)
    I_wc[i][j] = y
    cnt = cnt+1
    sys.stdout.write('done %d/%d\r' % (cnt, len(paramlist)))
np.savetxt("/home/zhangh/MyProject/FreqJ/FJ/result0.mat", I_wc,fmt="%.5e", delimiter=",")
