class Point:
    def __init__(self):
        self.seen = False
        self.label = None

    def set_label(self, group):
        self.seen = True
        self.label = group


def get_distance(points):
    pass


def label_neighbors(point, distances, epsilon, group):
    for neighbor in distances[point][distances[point] <= epsilon]:
        if not neighbor.seen:
            neighbor.set_label(group)
            label_neighbors(neighbor, distances, epsilon, group)


def dbscan(points, epsilon, density):
    distances = get_distance(points)

    core_points = []
    # finding core points
    for point in distances:
        if (distances[point] <= epsilon).sum() >= density:
            core_points.append(point)

    group = 0
    for point in core_points:
        if not point.seen:
            group += 1
            point.set_label(group)
            label_neighbors(point, distances, epsilon, group)

    return points
