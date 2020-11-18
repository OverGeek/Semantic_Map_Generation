import os as os
import json
import matplotlib.pyplot as plt

X = []
Y = []
with open('./Hypothesis_4/camera_frame_set_1_hypoth4.txt', 'r') as f:
    for line in f:
        data = json.loads(line)
        for corner in data["Mat"]:
            X.append(corner[1])
            Y.append(corner[3])

plt.scatter(X, Y)
plt.show()