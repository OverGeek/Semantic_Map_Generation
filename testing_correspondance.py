import json
from correspondence_matcher import correspondence_matcher

obj_file = "./seq22_annot.json"

with open(obj_file, "rb") as f:
	obj_list = json.load(f)

image_1 = "left000001.png"
image_2 = "left000006.png"

bbox_1 = obj_list[image_1]
bbox_2 = obj_list[image_2]


correspondence_matcher(bbox_1, bbox_2)