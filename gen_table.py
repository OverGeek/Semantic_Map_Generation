import pandas as pd
import json
import sys

Hypothesis_no = int(input('Hypothesis (1/2/3/4): '))
if Hypothesis_no not in [1,2,3,4]:
    print('Invalid Hypothesis'); sys.exit()

depth_data = []
with open(f"./Hypothesis_{Hypothesis_no}/annot_depths_hypoth{Hypothesis_no}.txt") as f:
    for line in f:
        depth_data.append(json.loads(line))

pos_data = []
with open(f"./Hypothesis_{Hypothesis_no}/world_frame_set_1_hypoth{Hypothesis_no}.txt") as f:
    for line in f:
        pos_data.append(json.loads(line))

arr_data = []
for i in range(len(depth_data)):
    row = [depth_data[i]["ID"], depth_data[i]["Name"]]
    corner_no = 1
    for j in range(i*4, i*4+4):
        row.append([pos_data[j]["X"], pos_data[j]["Y"], pos_data[j]["Z"]])
        row.append(1. / ((depth_data[i]["Corner_" + str(corner_no) + "_depth"]) + 1e-12))

    arr_data.append(row)

data = pd.DataFrame(arr_data, columns=['Image ID', 'Object ID', 'Corner1 Position', 'Corner1 Conf',
                                       'Corner2 Position', 'Corner2 Conf', 'Corner3 Position', 'Corner3 Conf',
                                       'Corner4 Position', 'Corner4 Conf'])

data.to_csv(f"./Hypothesis_{Hypothesis_no}/table_hypoth{Hypothesis_no}.csv")
