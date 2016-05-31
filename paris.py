from math import radians, cos, sin, asin, sqrt
import folium
from folium.features import PolyLine

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def closest_node(coords, location):
    dmin = float('inf')
    closest = None
    for i in range(len(coords)):
        d = haversine(coords[i][1], coords[i][0], location.longitude, location.latitude)
        if d < dmin:
            closest = i
            dmin = d
    return closest

def read_graph():
    with open('paris.txt') as f:
        lines = f.read().splitlines()
        N, M, T, C, S = map(int, lines[0].split())
        paris_coords = []
        for i in range(1, N + 1):
            paris_coords.append(list(map(float, lines[i].split())))  # Read coords
        paris_graph = {node: [] for node in range(N)}
        weight = {node: {} for node in range(N)}
        visited = {node: {} for node in range(N)}
        distance = {node: {} for node in range(N)}
        for i in range(N + 1, N + M + 1):
            start, end, nb_directions, duration, length = map(int, lines[i].split())
            paris_graph[start].append(end)
            weight[start][end] = duration
            distance[start][end] = length
            visited[start][end] = False
            if nb_directions == 2:
                paris_graph[end].append(start)
                weight[end][start] = duration
                distance[end][start] = length
                visited[end][start] = False
    return N, paris_graph, weight, distance, visited, paris_coords

def display(paris_coords, path):
    paris_viz = folium.Map(location=(48.8330293, 2.3618845), tiles='Stamen Watercolor', zoom_start=13)
    paris_viz.add_children(PolyLine(map(lambda node: paris_coords[node], path), weight=10, color='blue'))
    return paris_viz

def angle_between(p1, p2):
    return atan2(p2[1] - p1[1], p2[0] - p1[0])

def node_value(path, neighbor):
    node = path[-1]
    return distance[node][neighbor]
    if len(path) > 1:
        return (angle_between(paris_coords[neighbor], paris_coords[path[-1]]) - angle_between(paris_coords[path[-1]], paris_coords[path[-2]]))
    else:
        return 0
    # return randint(0, 1000)
    # return 0
    return distance[node][neighbor] / weight[node][neighbor]
