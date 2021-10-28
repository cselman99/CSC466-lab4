def closest_point(distances):
    pass


def h_clustering(points, threshold):
    point_distances = get_distance(points)
    clusters = {}
    # should use average link in most cases
    # single link extends in weird directions
    # complete link builds spheres
    while len(point_distances) > 1:
        cluster, distance = closest_points(point_distances)
        clusters[cluster] = distance
        point_distances = merge_clusters(point_distances, cluster)

    final = {}
    for cluster in clusters.keys():
        if clusters[cluster] < threshold:
            final[cluster] = clusters[cluster]

    # need to consider single points that are left out

    return final
