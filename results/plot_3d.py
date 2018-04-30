from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


FILENAME = "smart_64x64_CACHE.csv"
# SHEET = 
#X_LABEL = "cycle_time"
#Y_LABEL = "cache_size_kB"
Z_LABEL = "Avg Power"
Y_LABEL = "Cycle "
X_LABEL = "Total Area"


ALPHA=0.6

# Set OUTNAME to none if you don't want to save the figure
OUTNAME = None

#data = pd.read_excel(FILENAME, sheet_name=0)
data = pd.read_csv(FILENAME)
print(data.columns)
x = data.loc[:,X_LABEL].values
y = data.loc[:,Y_LABEL].values
z = data.loc[:,Z_LABEL].values

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.scatter(x, y, z, c='k', alpha=ALPHA)
plt.xlabel(X_LABEL)
plt.ylabel(Y_LABEL)
ax.set_zlabel(zlabel=Z_LABEL)
plt.show()
