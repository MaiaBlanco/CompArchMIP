
# coding: utf-8

# In[93]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


# In[94]:


files = ["smart_64x64_CACHE.csv", "64x64_CACHE_SMART_2.csv"]
brk_col = "Avg FU Dynamic Power"
outputs = ["Total Area", "Avg Power", "Runtime"]

dfs = []

for f in files:
	dfs.append(pd.read_csv(f, index_col=0))

df = pd.concat(dfs)
df.drop(['arrays','memory_type'], axis=1, inplace=True)


# In[95]:


inputs = df.columns.tolist()[:df.columns.tolist().index("Avg FU Dynamic Power")]
inputs


# In[96]:


df['Runtime'] = (df['Cycle '] * df.cycle_time).values


# In[97]:


input_data = df.loc[:,inputs]
output_data = df.loc[:,outputs]


# In[98]:


dat = output_data.as_matrix()


# In[99]:


def is_pareto_efficient(costs):
    """
    :param costs: An (n_points, n_costs) array
    :return: A (n_points, ) boolean array, indicating whether each point is Pareto efficient
    """
    is_efficient = np.ones(costs.shape[0], dtype = bool)
    for i, c in enumerate(costs):
        if is_efficient[i]:
            is_efficient[is_efficient] = np.any(costs[is_efficient]<=c, axis=1)  # Remove dominated points
    return is_efficient


# In[100]:


mask = is_pareto_efficient(dat)


# In[103]:


data = output_data[mask].sort_values(outputs)


# In[109]:


fig = plt.figure()
ax = fig.gca(projection='3d')
X_LABEL = outputs[0]
Y_LABEL = outputs[1]
Z_LABEL = outputs[2]
plt.xlabel(outputs[0])
plt.ylabel(outputs[1])
ax.set_zlabel(zlabel=outputs[2])
x = data.loc[:,X_LABEL].values
y = data.loc[:,Y_LABEL].values
z = data.loc[:,Z_LABEL].values
color = 'r'
alphas = 0.8
marker = 'o'
ax.scatter(x,y,z,c=color, marker=marker,alpha = alphas, s=150)
# ax.plot(x,y,z,c=color, marker=marker,alpha = alphas)
for xv, yv, zv, l in zip(x, y, z, [str(x) for x in data.index.values.tolist()]):
    ax.text(xv, yv, zv, l)
plt.show()


# Do a 2d plot of each view:

