from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Plot all designs as scatter points in 2D space.

FILENAME = "param_sweep_results_64x64_cache.xlsx"
# SHEET = 
X_LABEL = "Avg Power (mW)"
Y_LABEL = "Runtime (ms)"
# Z_LABEL = "P^2DP"


# Set OUTNAME to none if you don't want to save the figure
OUTNAME = None

data = pd.read_excel(FILENAME, sheet_name=0)
x = data.loc[:,X_LABEL].values
y = data.loc[:,Y_LABEL].values

fig = plt.figure()
plt.scatter(x, y)
plt.xlabel(X_LABEL)
plt.ylabel(Y_LABEL)
plt.show()