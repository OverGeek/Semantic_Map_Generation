import pandas as pd
import json

data = pd.read_excel('./data231020.xlsx')
data = data[["X", "Y", "Z", "Rotation Along Y"]]
data = data.to_numpy()
with open('name_position.txt', 'a+') as f:
    for i in range(data.shape[0]):
        row = {"ID": str(i).zfill(6)+"_rgb.png",
               "X": data[i][0],
               "Y": data[i][1],
               "Z": data[i][2],
               "Angle": data[i][3]}

        json.dump(row, f)
        f.write('\n')
