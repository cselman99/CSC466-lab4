import sys
from collections import Counter

import numpy as np
import parse
from calculations import *
import cProfile
import pstats


class Node:
    value = None
    child1 = None
    child2 = None
    dist = None

    def __init__(self, value, c1: 'Node' = None, c2: 'Node' = None, dist: float = 0):
        self.value = value
        self.child1 = c1
        self.child2 = c2
        self.dist = dist

    def __repr__(self):
        return str(self.value) + " dist: " + str(self.dist) + " " + str(self.child1) + " , " + str(self.child2)



# should use average link in most cases
# single link extends in weird directions
# complete link builds spheres

def h_clustering(points, threshold):
    if isinstance(points, list):
        clusters = [Node([p]) for p in points]
    else:
        clusters = [Node([p]) for p in points.tolist()]
    c_len = len(clusters)
    distance_arr = np.zeros((c_len, c_len), dtype=float)
    while len(distance_arr) > 1:
        c_len = len(clusters)
        min_dist = None
        c1 = None
        c2 = None
        for i in range(c_len):
            for j in range(c_len):
                if i == j:
                    continue
                # Only calculate distance if dist_arr value has not been previously calculated
                # distance_arr[i, j] = centroid_distance(clusters[i].value, clusters[j].value) \
                #     if distance_arr[i, j] == 0 else distance_arr[i, j]
                distance_arr[i, j] = average_linking(clusters[i].value, clusters[j].value) \
                    if distance_arr[i, j] == 0 else distance_arr[i, j]
                # distance_arr[i, j] = single_link(clusters[i].value, clusters[j].value) \
                #     if distance_arr[i, j] == 0 else distance_arr[i , j]
                cur_dist = distance_arr[i, j]
                if min_dist is None or cur_dist < min_dist:
                    min_dist = cur_dist
                    c1 = i
                    c2 = j
        # Merge C1 and C2 clusters
        new_node = Node(clusters[c1].value + clusters[c2].value, clusters[c1], clusters[c2], min_dist)
        clusters[c1] = new_node
        # Done using c2 point, now we can pop
        clusters.remove(clusters[c2])

        # Calculate minimum distance values between merged points
        for t in range(len(distance_arr[c1])):
            if t != c1 and t != c2:
                distance_arr[c1][t] = min(distance_arr[c1][t], distance_arr[c2][t])
        # Remove c2 row and column
        distance_arr = np.delete(distance_arr, c2, axis=0)
        distance_arr = np.delete(distance_arr, c2, axis=1)

    final_list = []
    get_threshold_nodes(clusters[0], threshold, final_list)
    return final_list, clusters[0]


def get_threshold_nodes(root, threshold, final_list):
    if root is None:
        return
    if root.dist == 0:  # Found a leaf node
        final_list.append(root.value)
        return
    if root.dist > threshold:
        get_threshold_nodes(root.child1, threshold, final_list)  # Check right
        get_threshold_nodes(root.child2, threshold, final_list)  # Check left
    else:
        final_list.append(root.value)
    return


def buildDendrogram(T, s, spaces):
    if T is None:
        return
    elif T.dist == 0:  # Found a leaf node
        new_t = [str(element) for element in T.value[0]]
        data = ",".join(new_t)
        content = "\t" * spaces + f"<leaf height= \"0\" data =\"{data}\"/>\n"
        s.append(content)
    elif spaces == 0:  # We are on the first iteration (root node)
        s.append(f"<tree height = \"{T.dist}\">\n")
        buildDendrogram(T.child1, s, spaces + 1)  # Traverse right
        buildDendrogram(T.child2, s, spaces + 1)  # Traverse left
        s.append("</tree>\n")
    else:
        content = "\t" * spaces + f"<node height = \"{T.dist}\">\n"
        s.append(content)
        buildDendrogram(T.child1, s, spaces + 1)  # Traverse right
        buildDendrogram(T.child2, s, spaces + 1)  # Traverse left
        s.append("\t" * spaces + "</node>\n")
    return


# profile = cProfile.Profile()
# profile.runcall(h_clustering, data_norm, 0.2)
# ps = pstats.Stats(profile)
# ps.print_stats()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        if filename == 'data/iris.csv' or filename == 'data/mammal_milk.csv':
            data, gt_dict = parse.parseGTData(filename)
            print(gt_dict)
        else:
            data = parse.parseData(filename)
            gt_dict = None
        # data_norm = normalize(np.asarray(data, dtype=float))

        # final_clusters, T = h_clustering(data, 0.8)  # for iris
        final_clusters, T = h_clustering(data, 1)  # for 4clusters
        s = []
        buildDendrogram(T, s, 0)
        f = open("dendrogram.txt", "w")
        f.writelines(s)
        f.close()

        if gt_dict is not None:
            print_accuracy(final_clusters, gt_dict)

        # For 2D datasets
        # graph2D('H Clustering at t = 6.5', "out2D.png", final_clusters)

        # For 3D datasets
        graph3D('H Clustering at t = 1', "out3D.png", final_clusters)
