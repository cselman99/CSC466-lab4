import sys
import numpy as np
import parse
from calculations import distance, normalize
import matplotlib.pyplot as plt


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
    clusters = [Node([p]) for p in points.tolist()]
    distance_arr = np.zeros((len(clusters), len(clusters)), dtype=float)
    while len(distance_arr) > 1:
        min_dist = None
        c1 = None
        c2 = None
        for i in range(len(clusters)):
            for j in range(len(clusters)):
                if i == j:
                    continue
                # Only calculate distance if dist_arr value has not been previously calculated
                distance_arr[i, j] = distance(clusters[i].value, clusters[j].value) \
                    if distance_arr[i, j] == 0 else distance_arr[i, j]
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
    # for dist, cluster in dendrogram.items():
    #     if dist <= threshold:
    #         final.append(cluster)
    # need to consider single points that are left out
    return final_list

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

if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        data = parse.parseData(filename)
        data_norm = normalize(np.asarray(data, dtype=float))  # possible issue with normalization

        final_clusters = h_clustering(data_norm, 1.4)
        colors = ["red","green","blue","yellow","pink","black","orange","purple","beige","brown","gray","cyan","magenta"]
        for i, c in enumerate(final_clusters):
            x_coords = []
            y_coords = []
            for coords in c:
                x_coords.append(coords[0])
                y_coords.append(coords[1])
            x_coords = np.asarray(x_coords)
            y_coords = np.asarray(y_coords)
            plt.scatter(x_coords, y_coords, color=colors[i % len(colors)])
        # plt.show()
        plt.savefig("out.png")
