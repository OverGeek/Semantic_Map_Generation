import json

with open('./annot_3n4.json', 'r') as f:
    src_json = json.load(f)

with open('annot_3n4.txt', 'a+') as f:
    for img_name, bboxes in src_json.items():
        for bbox in bboxes:
            row = {"ID": img_name,
                   "Name": bbox[0],
                   "Xmin": bbox[1],
                   "Ymin": bbox[2],
                   "Xmax": bbox[3],
                   "Ymax": bbox[4]}

            json.dump(row, f)
            f.write('\n')
