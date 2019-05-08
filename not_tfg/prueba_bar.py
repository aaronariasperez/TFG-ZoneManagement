import numpy as np
import matplotlib.pyplot as plt
import csv

fig = plt.figure()
ax = fig.add_subplot(111)

path_windows2 = 'E:\Dropbox\TFG\TFG_code\\route.csv'
path_linux2 = r'/home/aaron/Dropbox/TFG/TFG_code/route.csv'

result = [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0]
slopes = []
distances = []
types = []
with open(path_linux2, mode='r') as data:
    csv_reader = csv.reader(data, delimiter=',')
    for row in csv_reader:
        slopes.append(float(row[2]))
        distances.append(float(row[3]))
        types.append(int(row[1]))


N = len(slopes)

ind = np.arange(N)                # the x locations for the groups

width = 1                      # the width of the bars

colors = []
for t in result:
    if t == 0:
        colors.append('gray')
    else:
        colors.append('goldenrod')

rects1 = ax.bar(ind, slopes, width, color=colors)

#ax.set_xlim(-width,len(ind)+width)
ax.set_ylim(min(slopes)-1,max(slopes)+1)
ax.set_ylabel('Pendiente en grados', fontsize=21)
ax.set_title('En amarillo los tramos asignados en eléctrico.',fontsize=21)
xmarks = ['0']
aux = [' ']*(182-2)
xmarks = xmarks + aux + ['182']
xTickMarks = xmarks
ax.set_xticks(ind)
xtickNames = ax.set_xticklabels(xTickMarks)
plt.setp(xtickNames, rotation=45, fontsize=18)

plt.show()