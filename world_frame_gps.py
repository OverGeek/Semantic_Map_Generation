import json
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
import re
import copy


def main(seq=300):
    cameraFrame = []
    worldFrame = []
    data = []
    Xroad = []
    Yroad = []
    finalPos = {}
    sync = []
    theta = np.radians(0)
    c, s = np.cos(theta), np.sin(theta)
    rotation = [[1.0, 0.0, 0.0, 0.0], [0.0, c, -s, 0.0], [0.0, s, c, 0.0]]

    # FILE NAMES
    camera_frame_input_file = f"./Hypothesis_1/camera_frame_set_1_hypoth1_seq22.txt"
    robot_coordinates = "cc1dataset coordinates.xlsx"
    output_file = f"./Hypothesis_1/world_frame_set_1_hypoth1_seq22.txt"
    name_position = "./Positions_seq22.txt"
    # name_position_1 = "Positions_seq22_1.txt"
    baseline = 1.20008

    with open(camera_frame_input_file) as f:
        for line in f:
            cameraFrame.append(json.loads(line))

    name = []

    with open(name_position) as f:
        for line in f:
            name.append(json.loads(line))
        f.close()

    # with open(name_position_1) as f:
    #     for line in f:
    #         name.append(json.loads(line))
    #     f.close()
    print(len(name))
    f = open(output_file, "w+")
    # print(int(cameraFrame[0]["ID"][:-4]))
    for i in range(min(len(cameraFrame), len(name))):
        try:
            # print(cameraFrame[i]["ID"])
            # if "+" in cameraFrame[i]["ID"][:-4]:
            #     var = cameraFrame[i]["ID"][:-4].split("+")
            # elif "-" in cameraFrame[i]["ID"][:-4]:
            #     var = cameraFrame[i]["ID"][:-4].split("-")
            #     var[1] = -1 * int(var[1])
            # else:
            #     var = cameraFrame[i]["ID"][:-4]

            # print("var", var)
            # if isinstance(var, list) and len(var) > 1:
            #     position = int(var[0])
            #     angle = np.radians((int(var[1])) * np.pi / 180)
            # else:
            #     position = int(var)
            #     angle = np.radians(0)

            # print("Position", position, "angle", angle)
            # found = False
            # for j in range(len(name)):
            #     # print(cameraFrame[i]['ID'], name[j]['ID'])
            #     name_of_file = 'left' + str(name[j]['ID']).zfill(6) + '.png'
            #     # print(name_of_file)
            #     if (name_of_file == cameraFrame[i]['ID']):
            #         idx = j
            #         found = True
            #         break

            # if not found:
            #     print('not found')
            #     continue

            # x_cc1 = name[idx]['X']
            # y_cc1 = name[idx]['Y']
            # angle = name[idx]['angle']
            # sin, cos = np.sin(angle), np.cos(angle)
            # x_unrotated = (x_cc1*np.sin(72 * (np.pi / 180)) + baseline / 2) / 100
            # y_unrotated = 0
            # z_unrotated = (y_cc1 + x_cc1 * np.cos(72 * (np.pi / 180)))/100
            # x_unrotated = (369 * np.sin(72 * (np.pi / 180)) + baseline / 2) / 100
            # y_unrotated = 0
            # z_unrotated = (-1 * abs(position) - (369 * np.cos(72 * (np.pi / 180)))) / 100

            # unrotated_matrix = [[1.0, 0.0, 0.0, x_unrotated], [0.0, 1.0, 0.0, y_unrotated], [0.0, 0.0, 1.0, z_unrotated], [0.0, 0.0, 0.0, 1.0]]

            # rotation_matrix = [[cos, 0.0, -sin, 0.0], [0.0, 1.0, 0.0, 0.0], [sin, 0.0, cos, 0.0], [0.0, 0.0, 0.0, 1.0]]

            # rotated_world_coordinates = [[1.0, 0.0, 0.0, 0.0],
            #                              [0.0, 1.0, 0.0, 0.0],
            #                              [0.0, 0.0, 1.0, 0.0],
            #                              [0.0, 0.0, 0.0, 1.0]]

            rotated_world_coordinates = name[i]["Matrix"]

            mat = cameraFrame[i]["Mat"]
            finalPos["ID"] = cameraFrame[i]["ID"]
            finalPos["Name"] = cameraFrame[i]["Name"]
            # print(cameraFrame[i]['ID'], finalPos["Name"],end=" ")
            corner_world = []
            for i2 in range(len(mat)):
                # print("MAT", mat[i])
                finalPos_ = []
                object_matrix = [[1.0, 0.0, 0.0, mat[i2][1]], [0.0, 1.0, 0.0, mat[i2][2]], [0.0, 0.0, 1.0, mat[i2][3]],
                                 [0.0, 0.0, 0.0, 1.0]]

                object_world_coordinates = np.dot(rotated_world_coordinates, object_matrix)
                data.append(object_world_coordinates)
                finalPos_.append(object_world_coordinates[0][3])
                finalPos_.append(object_world_coordinates[1][3])
                finalPos_.append(object_world_coordinates[2][3])
                finalPos_.append(mat[i2][0])
                finalPos_.append(1 / finalPos_[0])
                corner_world.append(copy.deepcopy(finalPos_))
            finalPos["corners"] = corner_world
            json_data = json.dumps(finalPos)
            f.write(json_data + str("\n"))
            # print(finalPos["Corner_name"],finalPos["X"],finalPos["Y"],finalPos["Z"],end=" ")
            # print("@@@@",finalPos)
            # print()
        except Exception as e:
            print(e)

    xs = []
    ys = []

    # print(data)

    data_copy = []
    """
    k = 3
    print(len(data))
    for i in range(len(data) - 3):
        count = 0
        for j in range(i-3, i+3):
            #print(len(data[i][0]))
            dist = np.sqrt(np.square(data[i][0][3]- data[j][0][3]) + np.square(data[i][1][3] - data[j][1][3]))
            if(dist < 6):
                count = count + 1
        if(count >= k):
            print(i)
            data_copy.append(data[i])
    """
    # for i in range(len(worldFrame)):
    #   Xroad.append(worldFrame[i]['Position'][0])
    #   Yroad.append(worldFrame[i]['Position'][2])
    for i in range(len(data)):
        xs.append(data[i][0][3])
        ys.append(data[i][2][3])
        # print(str(data[i][0][3]) + "," + str(data[i][1][3]) + "," + str(data[i][2][3]) + "\n")

    # print(xs)
    # print(ys)

    # plt.scatter(Xroad,Yroad, color = 'blue')
    plt.scatter(xs, ys, color="red")
    # plt.scatter(gt['X'], gt['Y'], color = 'green')
    plt.show()
    # print(cameraFrame[0]['Mat'])
    # print(worldFrame[0]['Matrix'])


# seqs = [300, 370, 450, 530, 600, 700, 800, 900, 1000, 1100]
# for seq in seqs:
#     print(seq)
#     main(seq)
main()