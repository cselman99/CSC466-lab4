import sys

import numpy as np
from parse import read_data
from calculations import graph, print_accuracy, average_linking


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


def build_dendrogram(tree, string, spaces):
    if tree is None:
        return
    elif tree.dist == 0:  # Found a leaf node
        new_t = [str(element) for element in tree.value[0]]
        data = ",".join(new_t)
        content = "\t" * spaces + f"<leaf height= \"0\" data =\"{data}\"/>\n"
        string.append(content)
    elif spaces == 0:  # We are on the first iteration (root node)
        string.append(f"<tree height = \"{tree.dist}\">\n")
        build_dendrogram(tree.child1, string, spaces + 1)  # Traverse right
        build_dendrogram(tree.child2, string, spaces + 1)  # Traverse left
        string.append("</tree>\n")
    else:
        content = "\t" * spaces + f"<node height = \"{tree.dist}\">\n"
        string.append(content)
        build_dendrogram(tree.child1, string, spaces + 1)  # Traverse right
        build_dendrogram(tree.child2, string, spaces + 1)  # Traverse left
        string.append("\t" * spaces + "</node>\n")


# profile = cProfile.Profile()
# profile.runcall(h_clustering, data_norm, 0.2)
# ps = pstats.Stats(profile)
# ps.print_stats()


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        threshold = 1
        if len(sys.argv) == 3:
            threshold = float(sys.argv[2])

        filename = sys.argv[1]
        data, gt_dict, data_type = read_data(filename)

        # final_clusters, tree = h_clustering(data, 0.8)  # for iris
        final_clusters, tree = h_clustering(data, threshold)  # for 4clusters
        s = []
        build_dendrogram(tree, s, 0)
        f = open("dendrogram.txt", "w")
        f.writelines(s)
        f.close()

        if "mammal_milk" in filename:
            for i, cluster in enumerate(final_clusters):
                print("------------------------------------")
                print("Cluster %d" % (i + 1))
                for animal in cluster:
                    print(gt_dict[tuple(animal)])
                print()
        elif gt_dict is not None:
            print_accuracy(final_clusters, gt_dict)

        graph('H Clustering at t = 6.5', "out2D.png", final_clusters, data_type)
