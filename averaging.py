import json
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def main(seq):
    object_world_cords = []
    distance_threshhold = 10
    distance_threshhold_min = 5

    over_write_semantic_map = False

    if os.path.exists("./Hypothesis_1/world_frame_set_1_average.txt"):
        with open("./Hypothesis_1/world_frame_set_1_average.txt", "r") as f:
            if os.stat("./Hypothesis_1/world_frame_set_1_average.txt").st_size == 0:
                semantic_database = {}
            else:
                semantic_database = json.loads(f.read())
            f.close()
    else:
        semantic_database = {}

    with open(f"./Hypothesis_1/world_frame_set_1_hypoth1_{seq}.txt", "r") as f:
        objects = set()
        for line in f:
            line_dict = json.loads(line)
            objects.add(line_dict["Name"])
            object_world_cords.append(line_dict)
        f.close()

    # semantic_database = {}
    if len(semantic_database) == 0 or over_write_semantic_map == True:
        for line_dict in object_world_cords:
            obj_name = line_dict["Name"] + "_0"
            if obj_name not in semantic_database:
                semantic_database[obj_name] = {}
                for corner in line_dict["corners"]:
                    X, Y, Z, corner_name, conf = corner
                    conf = 1 / Z

                    semantic_database[obj_name][corner_name] = {}

                    semantic_database[obj_name][corner_name]["num_X"] = X * conf
                    semantic_database[obj_name][corner_name]["denom_X"] = conf

                    semantic_database[obj_name][corner_name]["num_Y"] = Y * conf
                    semantic_database[obj_name][corner_name]["denom_Y"] = conf

                    semantic_database[obj_name][corner_name]["num_Z"] = Z * conf
                    semantic_database[obj_name][corner_name]["denom_Z"] = conf

                    semantic_database[obj_name][corner_name]["X"] = semantic_database[obj_name][corner_name]["num_X"] / \
                                                                    semantic_database[obj_name][corner_name]["denom_X"]
                    semantic_database[obj_name][corner_name]["Y"] = semantic_database[obj_name][corner_name]["num_Y"] / \
                                                                    semantic_database[obj_name][corner_name]["denom_Y"]
                    semantic_database[obj_name][corner_name]["Z"] = semantic_database[obj_name][corner_name]["num_Z"] / \
                                                                    semantic_database[obj_name][corner_name]["denom_Z"]

    for line_dict in object_world_cords:
        name_obj = line_dict["Name"]
        maximum_obj_id = 0
        for obj_instance in semantic_database:
            if obj_instance.startswith(name_obj + "_"):
                maximum_obj_id += 1
        while (name_obj + "_" + str(maximum_obj_id)) in semantic_database:
            maximum_obj_id += 1

        for corner in line_dict["corners"]:
            X, Y, Z, corner_name, conf = corner
            conf = 1 / Z
            world_coord = np.array([X, Y, Z]).reshape(3, 1)
            dist = []
            coorDist = []
            for obj_instance in semantic_database:
                if obj_instance.startswith(name_obj) and corner_name in semantic_database[obj_instance]:
                    clustered_world_coord = np.array(
                        [
                            semantic_database[obj_instance][corner_name]["X"] / 1000,
                            semantic_database[obj_instance][corner_name]["Y"] / 1000,
                            semantic_database[obj_instance][corner_name]["Z"] / 1000,
                        ]
                    ).reshape(3, 1)
                    dist.append(
                        np.linalg.norm((np.array(world_coord).reshape(3, 1) - np.array(clustered_world_coord).reshape(3,
                                                                                                                      1)) / 1000))
                    coorDist.append([clustered_world_coord, obj_instance])
            if len(dist) > 0:
                idx = np.argmin(dist)
                if dist[idx] > distance_threshhold:
                    obj_instance = name_obj + "_" + str(maximum_obj_id + 1)
                    if obj_instance not in semantic_database:
                        semantic_database[obj_instance] = {}

                    semantic_database[obj_instance][corner_name] = {}

                    semantic_database[obj_instance][corner_name]["num_X"] = world_coord[0, 0] * 1 / world_coord[2, 0]
                    semantic_database[obj_instance][corner_name]["num_Y"] = world_coord[1, 0] * 1 / world_coord[2, 0]
                    semantic_database[obj_instance][corner_name]["num_Z"] = world_coord[2, 0] * 1 / world_coord[2, 0]

                    semantic_database[obj_instance][corner_name]["denom_X"] = (1 / world_coord[2, 0])
                    semantic_database[obj_instance][corner_name]["denom_Y"] = (1 / world_coord[2, 0])
                    semantic_database[obj_instance][corner_name]["denom_Z"] = (1 / world_coord[2, 0])

                    semantic_database[obj_instance][corner_name]["Z"] = (
                            semantic_database[obj_instance][corner_name]["num_Z"]
                            / semantic_database[obj_instance][corner_name]["denom_Z"]
                    )
                    semantic_database[obj_instance][corner_name]["Y"] = (
                            semantic_database[obj_instance][corner_name]["num_Y"]
                            / semantic_database[obj_instance][corner_name]["denom_Y"]
                    )
                    semantic_database[obj_instance][corner_name]["X"] = (
                            semantic_database[obj_instance][corner_name]["num_X"]
                            / semantic_database[obj_instance][corner_name]["denom_X"]
                    )
                if dist[idx] < distance_threshhold_min:
                    obj_instance = coorDist[idx][1]
                    semantic_database[obj_instance][corner_name]["num_X"] = \
                        semantic_database[obj_instance][corner_name][
                            "num_X"
                        ] + (world_coord[0, 0] * 1 / world_coord[2, 0])

                    semantic_database[obj_instance][corner_name]["num_Y"] = \
                        semantic_database[obj_instance][corner_name][
                            "num_Y"
                        ] + (world_coord[1, 0] * 1 / world_coord[2, 0])

                    semantic_database[obj_instance][corner_name]["num_Z"] = \
                        semantic_database[obj_instance][corner_name][
                            "num_Z"
                        ] + (world_coord[2, 0] * 1 / world_coord[2, 0])

                    semantic_database[obj_instance][corner_name]["denom_Z"] += 1 / world_coord[2, 0]
                    semantic_database[obj_instance][corner_name]["denom_Y"] += 1 / world_coord[2, 0]
                    semantic_database[obj_instance][corner_name]["denom_X"] += 1 / world_coord[2, 0]

                    semantic_database[obj_instance][corner_name]["Z"] = (
                            semantic_database[obj_instance][corner_name]["num_Z"]
                            / semantic_database[obj_instance][corner_name]["denom_Z"]
                    )
                    semantic_database[obj_instance][corner_name]["Y"] = (
                            semantic_database[obj_instance][corner_name]["num_Y"]
                            / semantic_database[obj_instance][corner_name]["denom_Y"]
                    )
                    semantic_database[obj_instance][corner_name]["X"] = (
                            semantic_database[obj_instance][corner_name]["num_X"]
                            / semantic_database[obj_instance][corner_name]["denom_X"]
                    )

    plot_dict = {}

    objs = set()
    for obj, data in semantic_database.items():
        objs.add(obj.split('_')[0])

    for obj in objs:
        plot_dict[obj] = [[], []]

    for obj, data in semantic_database.items():
        for corner_no in range(1, 5):
            try:
                plot_dict[obj.split('_')[0]][0].append(data[f"Pos{corner_no}"]["X"])
                plot_dict[obj.split('_')[0]][1].append(data[f"Pos{corner_no}"]["Z"])
            except Exception as e:
                print(e)
                continue

    for obj, data in plot_dict.items():
        plt.scatter(data[0], data[1])

    plt.savefig(f'./Hypothesis_1/plot_{seq}.png')

    with open('./Hypothesis_1/world_frame_set_1_average.txt', 'w') as f:
        json_data = json.dumps(semantic_database, indent=4, sort_keys=True)
        f.write(json_data)
        f.close()


seqs = [300, 370, 450, 530, 600, 700, 800, 900, 1000, 1100]
for seq in seqs:
    print(seq)
    main(seq)
