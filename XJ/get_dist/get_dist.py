#!/usr/bin/python3
# created by zhangh

import os
from obspy.clients.iris import Client

# get station data 
sta_list = open('station.dat')
sta = sta_list.readline()
st_names, st_los, st_las = [], [], []
st_num = 0
while sta:
    st_num = st_num + 1
    net, st_name, st_lo, st_la, st_ev = sta.split()
    st_names.append(st_name)
    st_los.append(float(st_lo))
    st_las.append(float(st_la))
    sta = sta_list.readline()
sta_list.close()

# get cor_SAC
sac_file_path = '/home/zhangh/Data/cor_pws'
sac_file_list = os.listdir(sac_file_path)
sac_num = 0

dists, sta1s, sta2s = [], [], []
for sac_file in sac_file_list:
    part = sac_file.split('.')[0].split('_')
    if len(part) == 3:
        sta1 = part[1]
        sta2 = part[2]
    elif len(part) == 4:
        if part[2] == '1':
            sta1 = part[1] + '_1'
            sta2 = part[3]
        else:
            sta1 = part[1]
            sta2 = part[2] + '_1'
    else:
        sta1 = part[1] + '_1'
        sta2 = part[3] + '_1'

    # if (sta1[0] in ['A','C','J'] or (sta1[0]=='D' and sta1 != 'DOC')) \
    # and (sta2[0] in ['A','C','J'] or (sta2[0]=='D' and sta2 != 'DOC')):

    if (sta1[0] == 'B' or sta1 == 'KMI' or sta1 == 'DOC') and (sta2[0] == 'B' or sta2 == 'KMI' or sta2 == 'DOC'):
        sac_num = sac_num + 1
        p1 = st_names.index(sta1)
        p2 = st_names.index(sta2)
        st_lo1, st_la1, st_lo2, st_la2 = st_los[p1], st_las[p1], st_los[p2], st_las[p2]
        client = Client()
        result = client.distaz(stalat=st_la1, stalon=st_lo1, evtlat=st_la2, evtlon=st_lo2)
        dist = int(result['distancemeters']) / 10 ** 3
        dists.append(dist)
        sta1s.append(sta1)
        sta2s.append(sta2)

for i in range(sac_num - 1):
    for j in range(i + 1, sac_num):
        if dists[i] > dists[j]:
            td, t1, t2 = dists[i], sta1s[i], sta2s[i]
            dists[i], sta1s[i], sta2s[i] = dists[j], sta1s[j], sta2s[j]
            dists[j], sta1s[j], sta2s[j] = td, t1, t2

dist_file = open('dist_s.dat', 'w')
for i in range(sac_num):
    dist_file.write(str(dists[i]) + ' ' + sta1s[i] + ' ' + sta2s[i] + '\n')

dist_file.close()
