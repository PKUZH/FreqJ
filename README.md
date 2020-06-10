# FreqJ
F-J (Frequency-Bessel Method) is a higher-mode rayleigh dispersion curve imaging method.
This repo is an open-source version of F-J, includes:

### Dispersion
Calculate theoretical Higher-Mode Dispersion curve of Rayleigh Wave using generalized R/T method  and secular functions
##### main.m
Calculate dispersion curve of given layer model  
use *cal_det.m* & *find_zero.m*
##### draw_secular.m
Show secular function of each layer
##### show_result.m
Show calculated dispersion curve

### FJ
Extract Higher-Mode Dispersion curve using F-J method
##### main.py
data IO and calculating, all in one
##### plot_gf.py
plot Green function and sort in distance between two stations
##### norm.py
Three different methods of normalization:
1. norm_mean: averaging on a time window
2. norm_one: one bite
3. norm_win: only use data in time window

### XJ
An example of application on Xiao Jiang Fault Zone
##### get_dist
Some pre-processing of station metadata
##### main.py
Similar to *main.py* in **FJ**, only data input is changed

If you have any question or comment, please contact me, thanks in advance!