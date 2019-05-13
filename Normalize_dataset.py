import csv
import numpy as np


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


# ****Read dataset from csv and reformat it****
x = []
y = []

path_windows = 'E:\Dropbox\TFG\TFG_code\dataset.csv'
path_linux = r'/home/aaron/Dropbox/TFG/TFG_code/dataset.csv'

with open(path_windows, mode='r') as dataset:
    csv_reader = csv.reader(dataset, delimiter=',')
    for row in csv_reader:
        x.append([float(x) for x in row[:-1]])
        y.append([float(x) for x in row[-1:]])

x = np.array(x)

with open('norm_dataset.csv', mode='w', newline='') as dataset:
    dataset_writer = csv.writer(dataset, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for i, xi in enumerate(x):
        green_exp, normal_exp, dist, slope, charge, rem_normal, rem_green = xi
        norm_expected = 1 if green_exp == 1 else -1
        norm_dist = normalize(dist, x[:, 2], 2)
        norm_slope = normalize(slope, x[:, 3], 3)
        norm_charge = normalize(charge, x[:, 4], 4)
        norm_rem_normal = normalize(rem_normal, x[:, 5], 5)
        norm_rem_green = normalize(rem_green, x[:, 6], 6)

        dataset_writer.writerow([norm_expected, norm_dist, norm_slope, norm_charge, norm_rem_normal, norm_rem_green, y[i][0]])
