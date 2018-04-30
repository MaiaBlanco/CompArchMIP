'''
This file generates plot for 60 64x64 cache runs informed by previous analysis.
This plot shows different cache sizes for Avg power vs Runtime and Avg Power vs Total Area


'''

#import importlib
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.font_manager import FontProperties



FILENAME = "smart_64x64_CACHE.csv"
# SHEET = 
X_LABEL = "Total Area"
Y_LABEL = "Runtime"
#Y_LABEL = "Total Area"
Z_LABEL = "Avg Power"
#Z_LABEL = "Runtime (ms)"
# Z_LABEL = "P^2DP"


# Set OUTNAME to none if you don't want to save the figure
OUTNAME = None

fig = plt.figure()
#ax = fig.gca(projection='3d')
ax = fig.gca()
#ax.plot_trisurf(x, y, z, cmap=cm.jet, linewidth=0.2)
#ax.scatter(x, y, z)
#ax.scatter(x,z)
plt.xlabel('Total Area (mm^2)')
plt.ylabel('Avg Power (mW)')
#ax.set_zlabel(zlabel=Z_LABEL)

data = pd.read_csv(FILENAME)
x = data.loc[:,X_LABEL].values
y = data.loc[:,Y_LABEL].values
z = data.loc[:,Z_LABEL].values
cache_assoc = data.loc[:,"cache_assoc"].values
cache_bw = data.loc[:,"cache_bandwidth"].values
cache_size = data.loc[:,"cache_size"].values
unrolling_factor_sub = data.loc[:,"unrolling_factor_sub"].values
unrolling_factor_num = data.loc[:,'unrolling_factor_norm'].values
unrolling_factor_row = data.loc[:,'unrolling_factor_row_sub'].values
print(data.describe())
speed = data.loc[:,"cycle_time"].values
all_markers = []
all_colors = []


l=[]
for i in range(0,4):
    l.append(None)

for i in range(0,len(x)):
    ass = cache_assoc[i]
    bw = int(cache_bw[i])
 #   cache_sz = cache_size[i]
    #print('BANDWIDTH: ',bw)    
    sub = unrolling_factor_sub[i]
    num = unrolling_factor_num[i]
    row = unrolling_factor_row[i]
    cycle_time= speed[i]
    marker = None
    #c_crit = sub
    c_crit = int(cache_size[i][:-2])
    label = ""
    x[i] = x[i] /1000/1000
    '''alphas = 0.6
    if row == 1:
        marker = 'o'
        label = label + "row = 1"
    elif row == 16:
        marker = '^'
        label = label + "row = 16"
    elif row == 64:
        marker = 'x'
        label = label + "row = 64"
    if c_crit == 1 :
        color='g'
        label = label + ", column= 1"
    elif c_crit == 8 :
        color = 'b' 
        label = label + ", column= 8"
    elif c_crit == 16 :
        color == 'r'
        label = label + ", column= 16"
    elif c_crit == 32 :
        color = 'y'
        label = label + ", column= 32"
    elif c_crit == 64 :
        color = 'k'
        label = label + ", column= 64"
    all_markers.append(marker)
    all_colors.append(color)

    ax.scatter( y[i],z[i],c=color, marker=marker,alpha = alphas, s=150, edgecolors = 'none', label = 'color')'''

    alphas = 0.6

    if sub == 16:

        if c_crit == 8:
            l[0] = ax.scatter( x[i],z[i],c='b', marker='o',alpha = alphas, s=150, edgecolors = 'none', label = 'color')

        elif c_crit == 16:
            l[1] = ax.scatter( x[i],z[i],c='r', marker='o',alpha = alphas, s=150, edgecolors = 'none', label = 'color')

        elif c_crit == 32:
            l[2] = ax.scatter( x[i],z[i],c='y', marker='o',alpha = alphas, s=150, edgecolors = 'none', label = 'color')

        elif c_crit == 64:
            l[3] = ax.scatter( x[i],z[i],c='k', marker='o',alpha = alphas, s=150, edgecolors = 'none', label = 'color')




labels = ['cache size = 8kB', 'cache size = 16kB', 'cache size = 32kB', 'cache size = 64kB', ]



chartBox = ax.get_position()
ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.6, chartBox.height])
ax.legend(l, labels,loc='upper center', bbox_to_anchor=(1.45, 0.8), shadow=True, ncol=1)

#plt.legend(l, labels, loc = 1)

plt.title("Average Power vs Total Area for Various Cache Sizes with a Fixed Unroll Factors")

plt.show()
