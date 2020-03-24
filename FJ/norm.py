import numpy as np

def norm(data,norm_win):
    l_d = len(data)
    mean_d = np.zeros(l_d)
    d_abs = [abs(i) for i in data]
    for i in range(l_d):
        mean_d[i] = np.mean(d_abs[int(max(i-norm_win,0)):int(min(i+norm_win,l_d))])
        mean_d[i] = max(1,mean_d[i])
    data_norm = [data[i]/mean_d[i] for i in range(l_d)]
    return data_norm
