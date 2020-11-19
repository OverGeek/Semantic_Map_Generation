def find_dist(bbox1, bbox2):
    Xcenter1 = (bbox1[0] + bbox1[2]) / 2
    Ycenter1 = (bbox1[1] + bbox1[3]) / 2

    Xcenter2 = (bbox2[0] + bbox2[2]) / 2
    Ycenter2 = (bbox2[1] + bbox2[3]) / 2

    return (Xcenter2 - Xcenter1) ** 2 + (Ycenter2 - Ycenter1) ** 2


def correspondence_matcher(char_bbox_list, bbox_list):
    char_objs = len(char_bbox_list)
    char_mat = {}
    for i in range(len(char_bbox_list)):
        for j in range(i + 1, len(char_bbox_list)):
            dist = find_dist(char_bbox_list[i], char_bbox_list[j])
            char_mat[dist] = [i, j]

    mat = {}
    for i in range(len(bbox_list)):
        for j in range(i + 1, len(bbox_list)):
            dist = find_dist(bbox_list[i], bbox_list[j])
            mat[dist] = [i, j]

    assigned_pairs = {}  # objects-->char_objects
    for dist, obj_pair in mat.items():
        closest_char_dist = min(char_mat.keys(), key=(lambda k: abs(k-dist)))
        assigned_pairs[obj_pair[0]] = char_mat[closest_char_dist][0]
        assigned_pairs[obj_pair[1]] = char_mat[closest_char_dist][1]
