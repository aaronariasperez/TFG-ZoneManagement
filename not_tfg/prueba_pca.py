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

with open(path_linux, mode='r') as dataset:
    csv_reader = csv.reader(dataset, delimiter=',')
    for row in csv_reader:
        x.append([float(x) for x in np.take(row,[0,1,2,4,5,6])])
        y.append([float(x) for x in row[-1:]])

x = np.array(x)
y = np.array(y)
pca = PCA(n_components=2)
pca.fit(x)

PCA(copy=True, n_components=2, whiten=False)

x = pca.transform(x)

ind = np.argwhere(y==0)[:,0]
ind2 = np.argwhere(y==1)[:,0]


h = .5  # step size in the mesh

# we create an instance of SVM and fit out data. We do not scale our
# data since we want to plot the support vectors
C = 1.0  # SVM regularization parameter
svc = svm.SVC(kernel='linear', C=C).fit(x, y)
#rbf_svc = svm.SVC(kernel='rbf', gamma=0.7, C=C).fit(x, y)
#poly_svc = svm.SVC(kernel='poly', degree=2, C=C).fit(x, y)
#lin_svc = svm.LinearSVC(C=C).fit(x, y)

# create a mesh to plot in
x_min, x_max = x[:, 0].min() - 1, x[:, 0].max() + 1
y_min, y_max = x[:, 1].min() - 1, x[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
np.arange(y_min, y_max, h))

Z = svc.predict(np.c_[xx.ravel(), yy.ravel()])

# Put the result into a color plot
Z = Z.reshape(xx.shape)
plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)

# Plot also the training points
plt.scatter(x[:, 0], x[:, 1], c=y[:, 0], cmap=plt.cm.coolwarm)
plt.xlabel('x1')
plt.ylabel('x2')
plt.xlim(xx.min(), xx.max())
plt.ylim(yy.min(), yy.max())
plt.xticks(())
plt.yticks(())
plt.title('prueba')

plt.show()