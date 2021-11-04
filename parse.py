import numpy as np
from calculations import normalize


def parse_data(input_file):
    file = open(input_file, "r")
    lines = file.readlines()
    restrictions = [int(li.strip()) for li in lines[0].split(",")]
    lines = lines[1:]
    line_list = []
    for line in lines:
        line = line.strip().replace("\"", "")
        line_list.append([float(li) for i, li in enumerate(line.split(",")) if len(li) > 0 and restrictions[i] == 1])
    return line_list


def parse_gt_data(input_file):
    file = open(input_file, "r")
    lines = file.readlines()
    d = []
    restrictions = [int(li.strip()) for li in lines[0].split(",")]
    lines = lines[1:]
    temp_dict = {}
    for line in lines:
        line = line.strip().replace("\"", "")
        line_list = []
        cat = None
        for i, li in enumerate(line.split(",")):
            if len(li) == 0:
                continue
            if restrictions[i] == 0:
                cat = li
            elif restrictions[i] == 1:
                line_list.append(float(li))
        if len(line_list) > 1:
            temp_dict[tuple(line_list)] = cat
            d += [line_list]
    return d, temp_dict


def read_data(filename, norm=True):
    if filename == 'data/iris.csv' or filename == 'data/mammal_milk.csv':
        data, gt_dict = parse_gt_data(filename)
    else:
        data = parse_data(filename)
        gt_dict = None

    if norm:
        temp = np.array(data).T
        temp = np.array([normalize(arr) for arr in temp]).T
        new_data = [arr.tolist() for arr in temp]
        if gt_dict is not None:
            new_dict = {}
            for i, value in enumerate(new_data):
                new_dict[tuple(value)] = gt_dict[tuple(data[i])]
            gt_dict = new_dict.copy()
        data = new_data

    data_type = None
    if len(data[0]) == 2:
        data_type = "2D"

    if len(data[0]) == 3:
        data_type = "3D"

    return data, gt_dict, data_type
