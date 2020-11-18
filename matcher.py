import os as os
import json
import matplotlib.pyplot as plt
import os as os
import statistics
from skimage import io

import sys

Hypothesis_no = 1


def euclidean(point1, point2):
    return (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2


def main(seq=300):
    if Hypothesis_no == 3 or Hypothesis_no == 4:
        depth_image_path = f'./images/{seq}/depth'

    window_size = 6
    with open(f'./depths_seq22.json', 'r') as f:
        depth_data = json.load(f)

    annot_depth = []
    with open(f'./annot_seq22.txt', 'r') as f:
        # count = 0
        for line in f:
            # if count == 2994:
            #     break
            # count += 1
            bbox = json.loads(line)
            image_name = bbox["ID"]

            # for Hypotheses 3 and 4
            if Hypothesis_no == 3 or Hypothesis_no == 4:
                depth_map = io.imread(os.path.join(depth_image_path, image_name))

            # for Hypotheses 1 and 2
            depth_data_image = depth_data[image_name]

            corners = [[bbox["Xmin"], bbox["Ymin"]],
                       [bbox["Xmax"], bbox["Ymin"]],
                       [bbox["Xmin"], bbox["Ymax"]],
                       [bbox["Xmax"], bbox["Ymax"]]]

            for i, corner in enumerate(corners):
                # for Hypotheses 1 and 2
                distances = [(euclidean(corner, [depth[0], depth[1]]), depth[2]) for depth in depth_data_image
                             if bbox["Xmin"] <= depth[0] <= bbox["Xmax"] and
                             bbox["Ymin"] <= depth[1] <= bbox["Ymax"]]

                # for Hypotheses 3 and 4
                # depths = []
                # for y in range(int(max(0, corner[1] - window_size)), int(min(1079, corner[1] + window_size))):
                #     for x in range(int(max(0, corner[0] - window_size)), int(min(1919, corner[0] + window_size))):
                #         if bbox["Ymin"] <= y <= bbox["Ymax"] and bbox["Xmin"] <= x <= bbox["Xmax"]:
                #             depths.append(depth_map[y][x])

                # Hypothesis-1 #####################################################
                if Hypothesis_no == 1:
                    try:
                        min_idx = distances.index(min(distances))
                    except:
                        min_idx = -1
                    if min_idx >= 0:
                        corner_depth = distances[min_idx][1]
                    else:
                        corner_depth = -1.
                ####################################################################

                # Hypothesis-2 ######################################################
                elif Hypothesis_no == 2:
                    corner_depths = [depth[1] for depth in distances]
                    try:
                        corner_depth = sum(corner_depths) / len(corner_depths)
                    except:
                        corner_depth = -1.
                ######################################################################

                # Hypothesis-3 #######################################################
                # elif Hypothesis_no == 3:
                #     try:
                #         corner_depth = float(depth_map[round(corner[1])][round(corner[0])])
                #     except:
                #         corner_depth = -1.
                #######################################################################

                # Hypothesis-4 ########################################################
                # elif Hypothesis_no == 4:
                #     try:
                #         corner_depth = sum(depths) / len(depths)
                #     except:
                #         corner_depth = -1.
                #######################################################################

                bbox["Corner_" + str(i + 1) + "_depth"] = corner_depth

            annot_depth.append(bbox)

    with open(f"Hypothesis_{Hypothesis_no}/annot_depths_hypoth{Hypothesis_no}_seq22.txt", "w") as f:
        for bbox in annot_depth:
            json.dump(bbox, f)
            f.write('\n')


# seqs = [300, 370, 450, 530, 600, 700, 800, 900, 1000, 1100]
# for seq in seqs:
#     print(seq)
#     main(seq)
main()