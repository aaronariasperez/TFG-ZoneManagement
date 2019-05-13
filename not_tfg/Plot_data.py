from sklearn.decomposition import PCA
from sklearn import svm
import csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


x = []
y = []

path_windows = 'E:\Dropbox\TFG\TFG_code\dataset.csv'
path_linux = r'/home/aaron/Dropbox/TFG/TFG_code/dataset.csv'

with open(path_windows, mode='r') as dataset:
    csv_reader = csv.reader(dataset, delimiter=',')
    for row in csv_reader:
        x.append([float(x) for x in np.take(row,[2,3,4,5,6])])
        y.append([float(x) for x in row[-1:]])

x = np.array(x)
y = np.array(y)
pca = PCA(n_components=2)
pca.fit(x)

PCA(copy=True, n_components=2, whiten=False)

x = pca.transform(x)

ind = np.argwhere(y==0)[:,0]
ind2 = np.argwhere(y==1)[:,0]

plt.scatter(x[ind, 0], x[ind, 1], c='gray')
plt.scatter(x[ind2, 0], x[ind2, 1], c='goldenrod')

plt.show()