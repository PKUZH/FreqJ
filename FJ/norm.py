import numpy as np


def norm_mean(data, win_b, win_e, norm_win):
    d_abs = [abs(i) for i in data[win_b:win_e]]
    for i in range(win_b, win_e):
        mean_d = np.mean(d_abs[int(max(i-win_b-norm_win, 0)): \
        int(min(i-win_b+norm_win, win_e-win_b))])
        data[i] = data[i]/mean_d
    return data


def norm_one(data, win_b, win_e):
    for i in range(win_b, win_e):
        if data[i] > 0:
            data[i] = 1
        elif data[i] < 0:
            data[i] = -1
    return data


def norm_win(data, win_b, win_e):
    for i in range(len(data)):
        if i < win_b or i > win_e:
            data[i] = 0
    return data
