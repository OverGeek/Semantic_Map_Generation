import pandas as pd
import json
import sys

from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d

Hypothesis_no = int(input('Hypothesis (1/2/3/4): '))
if Hypothesis_no not in [1,2,3,4]:
    print('Invalid Hypothesis'); sys.exit()

with open(f"./Hypothesis_{Hypothesis_no}/world_frame_set_1_average_hypoth{Hypothesis_no}.txt") as f:
    data = json.load(f)

pos = ['Pos1', 'Pos2', 'Pos3', 'Pos4']

x,y,z = [],[],[]
lx, ly, lz = [],[],[]
sem = []
for key in data:
    i,j,k = [],[],[]

    subKeyList = []
    for subKey in data[key]:
        subKeyList.append(subKey)

    for p in pos:
        if p in subKeyList:     
            x.append(data[key][p]['X'])
            y.append(data[key][p]['Y'])
            z.append(data[key][p]['Z'])

            #for line plot
            if p == 'Pos1' or p == 'Pos2':
                i.append(data[key][p]['X'])
                j.append(data[key][p]['Y'])
                k.append(data[key][p]['Z'])
    if len(i) > 0:
        lx.append(i)
        ly.append(j)
        lz.append(k)
        sem.append(key)

#line plot
for i in range(len(lx)):
    plt.plot(lx[i], lz[i])
    plt.scatter(lx[i], lz[i])
    plt.text(lx[i][0], lz[i][0],sem[i])
plt.show()


#scatter plot
plt.scatter(x,z, s=2)
plt.xlabel('z')
plt.ylabel('x')
fig = plt.figure()
ax = plt.axes(projection="3d")
ax.scatter3D(x, z, y, c=z, s=2, cmap='hsv');
ax.set_xlabel('x')
ax.set_ylabel('z')
ax.set_zlabel('y')
plt.show()
