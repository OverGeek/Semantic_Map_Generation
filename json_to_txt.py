import os as os
import json


def main(seq=300):
    with open('./bbox_seq22.json', 'r') as f:
        bboxes_data = json.load(f)

    with open(f"./annot_seq22.txt", 'a+') as f:
        for img_name, bboxes in bboxes_data.items():
            if len(img_name) > 14:
                continue
            for bbox in bboxes:
                row = {"ID": img_name,
                       "Name": bbox[0],
                       "Xmin": bbox[1],
                       "Ymin": bbox[2],
                       "Xmax": bbox[3],
                       "Ymax": bbox[4]}

                json.dump(row, f)
                f.write('\n')


# seqs = [300, 370, 450, 530, 600, 700, 800, 900, 1000, 1100]
# for seq in seqs:
#     print(seq)
#     main(seq)
main()
