import sys

import numpy as np
import pandas as pd
from parse import parseData


class Point:
    def __init__(self):
        self.seen = False
        self.label = None

    def set_label(self, group):
        self.seen = True
        self.label = group


def get_distances(df, ord_df, cont_df, cat_df):
    cols = []
    for i in range(df.shape[0]):
        result = None
        # Manhattan
        if ord_df.shape[1] > 0:
            ord_result = (ord_df - ord_df.iloc[i]).abs().sum(axis=1)
            result = ord_result

        # Euclidian
        if cont_df.shape[1] > 0:
            cont_result = ((cont_df - cont_df.iloc[i]) ** 2).sum(axis=1)
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
    for neighbor in distances[point][distances[point] <= epsilon].index:
        if not points[neighbor].seen:
            points[neighbor].set_label(group)
            if neighbor in core_points:
                label_neighbors(neighbor, distances, epsilon, group, points, core_points)


def dbscan(df, ord_df, cont_df, cat_df, epsilon, density):
    distances = get_distances(df, ord_df, cont_df, cat_df)

    core_points = set()
    points = {}
    # finding core points
    for point in distances:
        points[point] = Point()
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
    epsilon = 5
    density = 4

    if len(sys.argv) == 2:
        filename = sys.argv[1]
        data = parseData(filename)

        df = pd.DataFrame(data, columns=[i for i in range(len(data[0]))])

        ordinal_df = df[[0, 1]].astype(int)
        cont_df = df[[]].astype(float)
        categorical_df = df[[]]

        ps = dbscan(df, ordinal_df, cont_df, categorical_df, epsilon, density)
        for p in ps:
            print(ps[p].label)
