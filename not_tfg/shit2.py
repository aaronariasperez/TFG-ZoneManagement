import math
import numpy as np
import csv
from ast import literal_eval as make_tuple
import sys
import random
import matplotlib.pyplot as plt

a = [1, 1, 3 ,5 ,6]
print(np.mean(a))

print(np.random.exponential(0.1))

a = [np.random.exponential(0.3) for i in range(100000)]

num_bins = 1000
f, ax = plt.subplots(1)
n, bins, patches = ax.hist(a, num_bins, facecolor='blue', alpha=0.5)
ax.set_xlim(xmin=0)
plt.show(f)

#a = [random.gauss(0, 0.25) for i in range(100000)]
#
#num_bins = 1000
#f, ax = plt.subplots(1)
#n, bins, patches = ax.hist(a, num_bins, facecolor='blue', alpha=0.5)
#ax.set_xlim(xmin=-1.5)
#plt.show(f)