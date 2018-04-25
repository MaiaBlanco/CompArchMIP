from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


FILENAME = "param_sweep_results_64x64_cache.xlsx"
# SHEET = 
X_LABEL = "cycle_time"
Y_LABEL = "cache_size_kB"
# Z_LABEL = "Avg Power (mW)"
Z_LABEL = "Runtime (ms)"
# Z_LABEL = "P^2DP"


# Set OUTNAME to none if you don't want to save the figure
OUTNAME = None

data = pd.read_excel(FILENAME, sheet_name=0)
x = data.loc[:,X_LABEL].values
y = data.loc[:,Y_LABEL].values
z = data.loc[:,Z_LABEL].values

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_trisurf(x, y, z, cmap=cm.jet, linewidth=0.2)
plt.xlabel(X_LABEL)
plt.ylabel(Y_LABEL)
ax.set_zlabel(zlabel=Z_LABEL)
plt.show()