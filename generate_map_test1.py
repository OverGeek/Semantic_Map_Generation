import sys
import csv
import ast

from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d



Hypothesis_no = int(input('Hypothesis (1/2/3/4): '))
if Hypothesis_no not in [1,2,3,4]:
    print('Invalid Hypothesis'); sys.exit()


#TODO: get semantics used in groundtruth if map w.r.t groundtruth is to be gernerated
semantic_list = ['door_entryLeft', 'door_entryRight', 'door_MTechLab', 'door_2154',
                 'door_corridorEnd', 'door_corridorEndRight', 'door_Suneel', 'door_Sunny',
                 'door_unnamed',
                 'alphabet_A', 'alphabet_B', 'alphabet_C', 'alphabet_D', 'alphabet_E',
                 'alphabet_F', 'alphabet_G', 'alphabet_H', 'alphabet_I', 'alphabet_J',
                 'alphabet_K','alphabet_L']

c2m = 1; convert2m = True
if convert2m:
    c2m = 1/1000

choose_fromList = True
x,y,z = [],[],[]
map_file = f"./Hypothesis_{Hypothesis_no}/table_hypoth{Hypothesis_no}.csv"
with open(map_file, 'r') as csvfile:
    csvread = csv.reader(csvfile)

    firstline = True
    for row in csvread:
        if firstline:
            firstline = False; continue

        if choose_fromList:
            if row[2] in semantic_list:
                points = [ast.literal_eval(row[3]), ast.literal_eval(row[5]),
                          ast.literal_eval(row[7]), ast.literal_eval(row[9])]
        else:
            points = [ast.literal_eval(row[3]), ast.literal_eval(row[5]),
                      ast.literal_eval(row[7]), ast.literal_eval(row[9])]
        for p in points:
            x.append(p[0]*c2m)
            y.append(p[1]*c2m)
            z.append(p[2]*c2m)
        

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