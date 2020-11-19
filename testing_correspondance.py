import json
from correspondence_matcher import correspondence_matcher

obj_file = "./pred_seq22.json"
char_obj_file = './char_images.json'

with open(obj_file, "rb") as f:
	obj_list = json.load(f)

with open(char_obj_file, "rb") as f:
	char_obj_list = json.load(f)

image = "left003169.png"
char_image = "000023_rgb.png"

bbox_1 = char_obj_list[char_image]
bbox_2 = obj_list[image]


correspondence_matcher(bbox_1, bbox_2)