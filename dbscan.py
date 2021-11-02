import sys

import numpy as np
import pandas as pd
from parse import read_data
from calculations import graph


class Point:
    def __init__(self, info):
        self.seen = False
        self.label = None
        self.info = info

    def set_label(self, group):
        self.seen = True
        self.label = group


def get_distances(df, cont_df, cat_df):
    cols = []
    for i in range(df.shape[0]):
        result = None
        # Manhattan
        # if ord_df.shape[1] > 0:
        #     ord_result = (ord_df - ord_df.iloc[i]).abs().sum(axis=1)
        #     result = ord_result

        # Euclidian
        if cont_df.shape[1] > 0:
            cont_result = np.sqrt(((cont_df - cont_df.iloc[i]) ** 2).sum(axis=1))
            if result is None:
                result = cont_result
            else:
                result += cont_result

        # Dice
        if cat_df.shape[1] > 0:
            cat_result = (cat_df != cat_df.iloc[i]).astype(int)
            cat_result /= cat_df.shape[1]
            if result is None:
                result = cat_result
            else:
                result += cat_result

        cols.append(result)

    return pd.concat(cols, axis=1)


def label_neighbors(point, distances, epsilon, group, points, core_points):
    visit = []
    for neighbor in distances[point][distances[point] <= epsilon].index:
        if not points[neighbor].seen:
            points[neighbor].set_label(group)
            if neighbor in core_points:
                visit.append(neighbor)
    for neighbor in visit:
        label_neighbors(neighbor, distances, epsilon, group, points, core_points)


def dbscan(df, cont_df, cat_df, epsilon, density):
    distances = get_distances(df, cont_df, cat_df)

    core_points = set()
    points = {}
    # finding core points
    for point in distances:
        points[point] = Point(df.iloc[point, :])
        if (distances[point] <= epsilon).sum() >= density:
            core_points.add(point)

    group = 0
    for point in core_points:
        if not points[point].seen:
            group += 1
            points[point].set_label(group)
            label_neighbors(point, distances, epsilon, group, points, core_points)

    return points


if __name__ == "__main__":
    # 2, 2 for accidents
    # 5, 3 for many clusters
    # 7, 3 for 4 clusters
    # .001, 3 for moon data
    # .01, 3 for ring
    # .78, 2 for iris (not good between virginica and versicolor)
    # 1.75, 2 for mammal milk
    epsilon = 2
    density = 2

    if len(sys.argv) == 2:
        filename = sys.argv[1]
        data, gt_dict, data_type = read_data(filename)

        df = pd.DataFrame(data, columns=[i for i in range(len(data[0]))])

        cont_df = df[[i for i in range(len(data[0]))]].astype(float)
        categorical_df = df[[]]

        ps = dbscan(df, cont_df, categorical_df, epsilon, density)
        groups = {}
        temp = {}
        j = -1
        for i, p in enumerate(ps):
            if ps[p].label is None:
                ps[p].label = j
                j -= 1
            if ps[p].label not in groups:
                groups[ps[p].label] = []
                temp[ps[p].label] = []
            groups[ps[p].label].append(ps[p].info.values)
            temp[ps[p].label].append(gt_dict[tuple(ps[p].info.values)])
        print(temp.keys())
        print(temp)

        graph("DBSCAN at e=2 and # points=2", "", [groups[key] for key in groups.keys()], data_type)
