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

files = ["64x64_SPAD_2_block.csv", "64x64_SPAD_3_cyclic.csv"]
dfs = []

for f in files:
    dfs.append(pd.read_csv(f, index_col=0))

data = pd.concat(dfs)
data['Runtime'] = (data['Cycle '] * data.cycle_time).values / 1000 # Runtime in us

data.reset_index(drop=True, inplace=True)
#FILENAME = "64x64_SPAD.csv"
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
ax = fig.gca(projection='3d')
#ax.plot_trisurf(x, y, z, cmap=cm.jet, linewidth=0.2)
#ax.scatter(x, y, z)
#ax.scatter(x,z)
plt.xlabel('Total Area (mm^2)')
plt.ylabel('Runtime (ms)')
ax.set_zlabel(zlabel=Z_LABEL)

#data = pd.read_csv(FILENAME)
x = data.loc[:,X_LABEL].values
y = data.loc[:,Y_LABEL].values
z = data.loc[:,Z_LABEL].values
part = data.loc[:,"partition"].values
factors = data.loc[:,"factors"].values
spad_ports = data.loc[:,"spad_ports"].values
unrolling_factor_sub = data.loc[:,"unrolling_factor_norm"].values
unrolling_factor_row = data.loc[:,'unrolling_factor_row_sub'].values
print(data.describe())
speed = data.loc[:,"cycle_time"].values


l=[]
for i in range(0,9):
    l.append(None)


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
    if ass == 'cyclic':
        if c_crit == 1 :
            l[0] = ax.scatter(x[i],y[i],z[i],c='r', marker='^',alpha = alphas, s=150)
        elif c_crit == 2 :
            l[1] = ax.scatter(x[i],y[i],z[i],c='r', marker='o',alpha = alphas, s=150) 
        elif c_crit == 4 :
            l[2] = ax.scatter(x[i],y[i],z[i],c='r', marker='x',alpha = alphas, s=150)

        elif c_crit == 8 :
            l[3] = ax.scatter(x[i],y[i],z[i],c='r', marker='<',alpha = alphas, s=150)
        elif c_crit == 64:
            l[4] = ax.scatter(x[i],y[i],z[i],c='r', marker='>',alpha = alphas, s=150)
    elif ass == 'block':
        if c_crit == 64 :
            l[5] = ax.scatter(x[i],y[i],z[i],c='b', marker='^',alpha = alphas, s=150)
        elif c_crit == 128 :
            l[6] = ax.scatter(x[i],y[i],z[i],c='b', marker='o',alpha = alphas, s=150) 
        elif c_crit == 256 :
            l[7] = ax.scatter(x[i],y[i],z[i],c='b', marker='x',alpha = alphas, s=150)

        elif c_crit == 512 :
            l[8] = ax.scatter(x[i],y[i],z[i],c='b', marker='<',alpha = alphas, s=150)
    #if True: #row == 8 and sub == 16:
        #ax.scatter(x[i],y[i],z[i],c=color, marker=marker,alpha = alphas, s=150)

labels = ['cyclic, factor =1', 'cyclic, factor =2', 'cyclic, factor ==4', 'cyclic, factor =8', 'cyclic, factor =64','block, factor =64', 'block, factor =128', 'block, factor =256', 'block, factor =512']


chartBox = ax.get_position()
ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.6, chartBox.height])
ax.legend(l, labels,loc='upper center', bbox_to_anchor=(1.45, 0.8), shadow=True, ncol=2)


plt.show()
