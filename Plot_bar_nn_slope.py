import numpy as np
import matplotlib.pyplot as plt
import csv
from keras.models import load_model


computed = {}


def normalize(data, data_array, i):
    if i in computed:
        minim = computed[i][0]
        maxim = computed[i][1]
    else:
        minim = min(data_array)
        maxim = max(data_array)
        computed[i] = (minim, maxim)

    return (data-minim)/(maxim-minim)


path_windows = 'E:\Dropbox\TFG\TFG_code\dataset.csv'
path_linux = r'/home/aaron/Dropbox/TFG/TFG_code/dataset.csv'
path_windows3 = 'E:\Dropbox\TFG\TFG_code\\trained_model3_10_adamax_best.h5'
path_linux3 = r'/home/aaron/Dropbox/TFG/TFG_code/trained_model3_10_adamax_best.h5'

model = load_model(path_windows3)
x = []
y = []
with open(path_windows, mode='r') as dataset:
    csv_reader = csv.reader(dataset, delimiter=',')
    for row in csv_reader:
        x.append([float(x) for x in row[:-1]])
        y.append([float(x) for x in row[-1:]])

x = np.array(x)

combustion_total = [0]*3
electric_total = [0]*3
combustion_hit = [0]*3
electric_hit = [0]*3
for i, xi in enumerate(x):
    green_exp, normal_exp, dist, slope, charge, rem_normal, rem_green = xi
    norm_expected = 1 if green_exp == 1 else -1
    norm_dist = normalize(dist, x[:, 2], 2)
    norm_slope = normalize(slope, x[:, 3], 3)
    norm_charge = normalize(charge, x[:, 4], 4)
    norm_rem_normal = normalize(rem_normal, x[:, 5], 5)
    norm_rem_green = normalize(rem_green, x[:, 6], 6)

    sec = [norm_expected, norm_dist, norm_slope, norm_charge, norm_rem_normal, norm_rem_green]
    y_expected = y[i][0]

    if y_expected == 0:  # combustion
        if slope <= -1:
            combustion_total[0] += 1
        elif -1 < slope < 1:
            combustion_total[1] += 1
        elif 1 <= slope:
            combustion_total[2] += 1

    if y_expected == 1:  # electric
        if slope <= -1:
            electric_total[0] += 1
        elif -1 < slope < 1:
            electric_total[1] += 1
        elif slope >= 1:
            electric_total[2] += 1

    prediction = model.predict(np.array([sec]))

    if prediction[0][0] >= prediction[0][1]:  # combustion
        if y_expected == 0:  # combustion
            if slope <= -1:
                combustion_hit[0] += 1
            elif -1 < slope < 1:
                combustion_hit[1] += 1
            elif 1 <= slope:
                combustion_hit[2] += 1

    else:  # electric
        if y_expected == 1:  # electric
            if slope <= -1:
                electric_hit[0] += 1
            elif -1 < slope < 1:
                electric_hit[1] += 1
            elif 1 <= slope:
                electric_hit[2] += 1


result_combustion = [combustion_hit[i]/combustion_total[i] for i in range(3)]
result_electric = [electric_hit[i]/electric_total[i] for i in range(3)]

fig = plt.figure()
ax = fig.add_subplot(111)

ind = range(3)                # the x locations for the groups

width = 0.6                      # the width of the bars

rects1 = ax.bar(ind, result_electric, width, color="goldenrod")

#ax.set_xlim(-width,len(ind)+width)
#ax.set_ylim(min(result_combustion)-1,max(result_combustion)+1)
ax.set_ylabel('Proporción de acierto', fontsize=12)
ax.set_xlabel('Agrupación de tramos por intervalo de pendientes (grados) y número de tramos', fontsize=12)
#ax.set_title('Aciertos de la red neuronal para los tramos de combustión según su longitud.',fontsize=14)

xTickMarks = ["<=-1 ("+str(electric_total[0])+")", "(-1,1) ("+str(electric_total[1])+")", ">=1 ("+str(electric_total[2])+")"]
ax.set_xticks(ind)
xtickNames = ax.set_xticklabels(xTickMarks)
plt.setp(xtickNames, rotation=0, fontsize=10)

plt.show()