#import importlib
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


FILENAME = "smart_64x64_CACHE.xlsx"
# SHEET = 
X_LABEL = "Total Area"
Y_LABEL = "Runtime (ms)"
#Y_LABEL = "Total Area"
Z_LABEL = "Avg Power (mW)"
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

data = pd.read_excel(FILENAME, sheet_name=0)
x = data.loc[:,X_LABEL].values
y = data.loc[:,Y_LABEL].values
z = data.loc[:,Z_LABEL].values
cache_assoc = data.loc[:,"cache_assoc"].values
cache_bw = data.loc[:,"cache_bandwidth"].values
cache_size = data.loc[:,"cache_size_kB"].values
unrolling_factor_sub = data.loc[:,"unrolling_factor_sub"].values
unrolling_factor_num = data.loc[:,'unrolling_factor_num'].values
unrolling_factor_row = data.loc[:,'unrolling_factor_row_sub'].values
print(data.describe())
speed = data.loc[:,"cycle_time"].values

for i in range(0,len(x)):
    ass = cache_assoc[i]
    bw = int(cache_bw[i])
    cache_sz = cache_size[i]
    #print('BANDWIDTH: ',bw)    
    sub = unrolling_factor_sub[i]
    num = unrolling_factor_num[i]
    row = unrolling_factor_row[i]
    cycle_time= speed[i]
    marker = None

    alphas = 0.6

    '''if cycle_time == 10 and bw==4 and ass == 1 and cache_sz == 16:
        #if sub ==16 and num == 16:
        #    marker = "o"
        #elif sub == 32 and num ==32:
        #    marker = None
        if row == 1:
            marker = 'o'
        elif row == 8:
            marker = '^'
        if sub == 16 and num ==16:
            ax.scatter(x[i],y[i],z[i],c='r', marker=marker, alpha=alphas)
        elif sub == 16 and num == 32:
            ax.scatter(x[i],y[i],z[i],c='b', marker = marker,alpha = alphas)
        elif sub == 32 and num == 16:
            ax.scatter(x[i],y[i],z[i],c='k', marker = marker,alpha = alphas)
        elif sub == 32 and num == 32:
            ax.scatter(x[i],y[i],z[i],c='y', marker = marker,alpha = alphas)'''
    ax.scatter(x[i],y[i],z[i],c='b',alpha = alphas)

plt.show()
