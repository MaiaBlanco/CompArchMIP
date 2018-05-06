'''
This file generates plot for 60 64x64 cache runs informed by previous analysis.
The plot shows that unrolling the row factor does not give much increase in performance,
Note that mem and FU area scalings are different and should be considered separately.
However whole area is the primary concern overall.

Cache changes area and energy significantly. Does not change runtime as much.
Row unrolling change runtime minimally. Seems not to change area, but this may be becuase of relative scale
with reference to the memory (cache) scaling.
Col unrolling from 1 to 8 has huge change; recommend looking at intermediate values in this range.
Diminishing returns for all cache sizes and row unrolls when col unroll scales further.


'''

#import importlib
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


#FILENAME = "smart_64x64_CACHE.csv"
FILENAME = "64x64_CACHE_SMART_2.csv"
# SHEET = 
X_LABEL = "MEM Area"
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
cache_assoc = data.loc[:,"cache_assoc"].values
cache_bw = data.loc[:,"cache_bandwidth"].values
cache_size = data.loc[:,"cache_size"].values
cache_line = data.loc[:,"cache_line_sz"].values
unrolling_factor_sub = data.loc[:,"unrolling_factor_sub"].values
unrolling_factor_num = data.loc[:,'unrolling_factor_norm'].values
unrolling_factor_row = data.loc[:,'unrolling_factor_row_sub'].values
print(data.describe())
speed = data.loc[:,"cycle_time"].values

for i in range(0,len(x)):
    ass = cache_assoc[i]
    bw = int(cache_bw[i])
    #print('BANDWIDTH: ',bw)    
    sub = unrolling_factor_sub[i]
    num = unrolling_factor_num[i]
    row = sub #cache_line[i]
    #unrolling_factor_row[i]
    cycle_time= speed[i]
    marker = None
    color='w'
    c_crit = cache_line[i] 
    sz = int(cache_size[i][:-2])
    
    alphas = 0.6
    if sz == 8:
        marker = 'o'
    elif sz  == 16:
        marker = '^'
    elif sz == 32:
        marker = 'x'
#    if c_crit == 1 :
#        color='g'
#    elif c_crit == 8 :
#        color = 'b' 
#    elif c_crit == 16 :
#        color == 'r'
#        #marker = '*'
    if c_crit == 32 :
        color = 'y'
    elif c_crit == 64 :
        color = 'k'
    if sub == 64:
        ax.scatter(x[i],y[i],z[i],c=color, marker=marker,alpha = alphas, s=150)



plt.show()
