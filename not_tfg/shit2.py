import math
import numpy as np

dist = 2400
time = dist*0.001 / 20
h = round(time)
m = round(time%1*60)
print(h)
print(m)

print(np.random.normal(0.5,0.1))