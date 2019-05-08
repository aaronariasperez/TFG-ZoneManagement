import glob

paths = []

for p in glob.glob('datasets/*'):
    print(p)
    paths.append(p)

f_dataset = open('dataset.csv', 'w')
for path in paths:
    f_aux = open(path, 'r')
    for line in f_aux:
        f_dataset.write(line)
