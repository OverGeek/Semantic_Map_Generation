import json
import math


def dist(points1, points2):
    dist = 0
    for point1, point2 in zip(points1, points2):
        dist += math.sqrt((point1[0] - point2[0]) ** 2 +
                          (point1[1] - point2[1]) ** 2 +
                          (point1[2] - point2[2]) ** 2)

    return dist / len(points1)


averaged_objs = []
with open('../Hypothesis_1/world_frame_set_1_average1.txt', 'r') as f:
    averaged_objs = json.load(f)

obj_world_coords = []
with open('./world_frame_set_1.txt', 'r') as f:
    for line in f:
        obj_world_coords.append(json.loads(line))

uv_coords = []
with open('./annotation.txt') as f:
    for line in f:
        uv_coords.append(json.loads(line))

assigned_coords = {}
for row in obj_world_coords:
    assigned_coords[row["ID"]] = []

for i in range(0, len(obj_world_coords), 4):
    img_name = obj_world_coords[i]["ID"]
    obj_name = obj_world_coords[i]["Name"].split('_')[0]

    corner_coords = []

    for corner_id in range(4):
        corner_coords.append([obj_world_coords[i + corner_id]["X"] / 1000.,
                              obj_world_coords[i + corner_id]["Y"] / 1000.,
                              obj_world_coords[i + corner_id]["Z"] / 1000.])

    avg_obj_dist = {}

    for obj, data in averaged_objs.items():
        if obj.split('_')[0] == obj_name:
            avg_coords = []
            for corner_name, val in data.items():
                avg_coords.append([val["X"], val["Y"], val["Z"]])

            n = len(avg_coords)
            corner_coords = corner_coords[:n]
            avg_obj_dist[obj] = dist(corner_coords, avg_coords)

    key_min = min(avg_obj_dist.keys(), key=(lambda k: avg_obj_dist[k]))

    for uv_coord in uv_coords:
        if uv_coord["ID"] == img_name and uv_coord["Name"] == obj_world_coords[i]["Name"]:
            u1, v1 = uv_coord["Xmin"], uv_coord["Ymin"]
            u2, v2 = uv_coord["Xmax"], uv_coord["Ymin"]
            u3, v3 = uv_coord["Xmin"], uv_coord["Ymax"]
            u4, v4 = uv_coord["Xmax"], uv_coord["Ymax"]

    img_dict = {obj_name: [[[u1, v1], averaged_objs[key_min]["Pos1"]["X"], averaged_objs[key_min]["Pos1"]["Y"], averaged_objs[key_min]["Pos1"]["Z"]],
                           [[u2, v2], averaged_objs[key_min]["Pos2"]["X"], averaged_objs[key_min]["Pos2"]["Y"], averaged_objs[key_min]["Pos2"]["Z"]],
                           [[u3, v3], averaged_objs[key_min]["Pos3"]["X"], averaged_objs[key_min]["Pos3"]["Y"], averaged_objs[key_min]["Pos3"]["Z"]],
                           [[u4, v4], averaged_objs[key_min]["Pos4"]["X"], averaged_objs[key_min]["Pos4"]["Y"], averaged_objs[key_min]["Pos4"]["Z"]]]}
    assigned_coords[img_name].append(img_dict)

