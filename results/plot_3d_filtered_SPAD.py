'''
64x64 Number of scratchpad ports is useless for runtime, area, AND power.
Block partition type requires more runs w/ diff factors, is very area and pwr efficient but does not move
runtime much.
Cyclic partition is expensive but effective.
Partition factor affects area significantly, and moves runtime and power a bit. Is on Paleo frontier 
so needs more sweeps.
'''

#import importlib
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


FILENAME = "64x64_SPAD.csv"
# SHEET = 
X_LABEL = "Total Area"
Y_LABEL = "Cycle "
#Y_LABEL = "Total Area"
Z_LABEL = "Avg Power"
#Z_LABEL = "Runtime (ms)"
# Z_LABEL = "P^2DP"


# Set OUTNAME to none if you don't want to save the figure
OUTNAME = None

fig = plt.figure()
ax = fig.gca(projection='3d')
#ax.plot_trisurf(x, y, z, cmap=cm.jet, linewidth=0.2)
#ax.scatter(x, y, z)
#ax.scatter(x,z)
plt.xlabel(X_LABEL)
plt.ylabel(Y_LABEL)
ax.set_zlabel(zlabel=Z_LABEL)

data = pd.read_csv(FILENAME)
x = data.loc[:,X_LABEL].values
y = data.loc[:,Y_LABEL].values
z = data.loc[:,Z_LABEL].values
part = data.loc[:,"partition"].values
factors = data.loc[:,"factors"].values
spad_ports = data.loc[:,"spad_ports"].values
unrolling_factor_sub = data.loc[:,"unrolling_factor_cols"].values
unrolling_factor_row = data.loc[:,'unrolling_factor_row_sub'].values
print(data.describe())
speed = data.loc[:,"cycle_time"].values

for i in range(0,len(x)):
    ass = part[i]
    fact = factors[i]
    bw = spad_ports[i]
 #   cache_sz = cache_size[i]
    #print('BANDWIDTH: ',bw)    
    sub = unrolling_factor_sub[i]
    row = unrolling_factor_row[i]
    cycle_time= speed[i]
    marker = None
    c_crit = fact
    #c_crit = int(cache_size[i][:-2])
    
    alphas = 0.6
    if cycle_time == 5:
        marker = 'o'
    elif cycle_time == 10:
        marker = '^'
    if c_crit == 1 :
        color='g'
    elif c_crit == 16 :
        color = 'b' 
    elif c_crit == 32 :
        color = 'y'
    elif c_crit == 64 :
        color = 'k'
    if True: #row == 8 and sub == 16:
        ax.scatter(x[i],y[i],z[i],c=color, marker=marker,alpha = alphas, s=150)



plt.show()
