import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

files = [""]
dfs = []

for f in files:
	dfs.append(pd.read_csv(f))

df = pd.concat(dfs)