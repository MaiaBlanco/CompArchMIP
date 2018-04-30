'''
Cyclic is more expensive than block in area but not in leakage power. It is more expensive in dynamic memory power,
but this is again because cyclic unleased more compute capability for unrolled hardware loops.
Chunk size has no effect, neither does spad_ports (suspect this is a bug).

'''


#import importlib
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


FILENAME = "64x64_SPAD_4_DMACHUNK.csv"
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
unrolling_factor_sub = data.loc[:,"unrolling_factor_sub"].values
unrolling_factor_row = data.loc[:,'unrolling_factor_row_sub'].values
chunk = data.loc[:,'dma_chunk_size'].values
print(data.describe())
speed = data.loc[:,"cycle_time"].values

for i in range(0,len(x)):
    fact = factors[i]
    bw = spad_ports[i]
 #   cache_sz = cache_size[i]
    #print('BANDWIDTH: ',bw)    
    sub = unrolling_factor_sub[i]
    row = unrolling_factor_row[i]
    cycle_time= speed[i]
    marker = None
    c_crit = part[i]
    #c_crit = int(cache_size[i][:-2])
    
    alphas = 0.6
    if bw == 2:
        marker = '.'
    elif bw == 4:
        marker = 'o'
    elif bw == 8:
        marker = 'v'
    elif bw == 16:
        marker = '^'
    elif bw == 32:
        marker = '>'
    elif bw == 64:
        marker = '<'
    if c_crit == 'cyclic' :
        color='g'
    elif c_crit == 'block' :
        color = 'b' 
    elif c_crit == 256:
        color = 'y'
    elif c_crit == 512 :
        color = 'k'
    if True :
        ax.scatter(x[i],y[i],z[i],c=color, marker=marker,alpha = alphas, s=150)



plt.show()
