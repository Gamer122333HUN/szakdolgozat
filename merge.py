from qgis.core import (
    QgsVectorLayer,
    QgsField,
    QgsFields,
    QgsFeature,
    QgsProject,
    QgsWkbTypes
)
import networkx as nx
import matplotlib.pyplot as plt
import math


def createGraph():
    # Centroidok kiszámítása és csúcsok hozzáadása
    for feature in features:
        centroid = feature.geometry().centroid().asPoint()
        fid = feature.id()
        spatial_index.addFeature(feature)
        graph.add_node(fid, pos=centroid)

    # Élek hozzáadása
    for i in range(len(features) - 1):
        for k in range(i + 1, len(features)):
            geom1 = features[i].geometry()
            geom2 = features[k].geometry()
            shortest_line = geom1.shortestLine(geom2)
            distance = shortest_line.length() #*feet
            distances.append(distance)
            if distance < max_distance_for_graph:
                graph.add_edge(features[i].id(), features[k].id(), weight=distance)

def stats():
    print(f"CRS: {layer.crs()}")
    print(f"Csúcsok száma: {graph.number_of_nodes()}")
    print(f"Élek száma: {graph.number_of_edges()}")
    print(f"max táv: {max(distances)}")
    print(f"min táv: {min(distances)}")
    print(f"átl táv: {sum(distances) / len(distances)}")

def showGraph():
    plt.figure(figsize=(6, 6))  # Új ablak/ábra nyitása
    pos = nx.get_node_attributes(graph, 'pos')
    nx.draw(graph, pos, with_labels=True, node_size=20)
    rounded_labels = {
        (u, v): f"{d['weight']:.2f}"
        for u, v, d in graph.edges(data=True)
    }
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=rounded_labels)
    plt.show()

def createLayer():
    layer_name = f"new_{layer.name()}"
    crs = "EPSG:3857"
    geometry = "Polygon"

    new_layer = QgsVectorLayer(f"{geometry}?crs={crs}", layer_name, "memory")
    dpr = new_layer.dataProvider()

    dpr.addAttributes([
        QgsField("id", QVariant.Int)
    ])
    new_geometries = mergeCompatible()
    new_layer.updateFields()


    if new_geometries:
        print("sikeres összeolvasztás")
        for i, geom in enumerate(new_geometries):
            feat = QgsFeature()
            feat.setGeometry(geom)  # geom: QgsGeometry típus
            feat.setAttributes([i])  # Attribútum értékek
            dpr.addFeature(feat)
    else:
        print("nem sikerült összeolvasztani")

    new_layer.updateExtents()
    QgsProject.instance().addMapLayer(new_layer)

def getFeatureId(szam):
    for feature in temp_features:
        if feature.id() == szam:
            return feature
    return None

def mergeCompatible():
    edges = sorted(graph.edges(data='weight'), key=lambda x: x[2])
    geometries = []
    print(edges)
    for edge in edges:
        if edge[2] < max_distance_for_merge:
            if getFeatureId(edge[0]) is not None and getFeatureId(edge[1]) is not None:
                new_geometry = QgsGeometry.combine(getFeatureId(edge[0]).geometry(), getFeatureId(edge[1]).geometry())
                geometries.append(new_geometry)
                temp_features.remove(getFeatureId(edge[1]))
            '''for edge2 in graph.edges(edge[1], data='weight'):
                if edge2[1] != edge[0]:
                    if edge[1] == edge2[1] and edge[2] > edge2[2]:
                        graph[edge[0]][edge[1]]['weight'] = edge2[2]
            graph.remove_node(edge[1])'''

    return geometries







# Beállítások
max_distance_for_graph = 10  # Maximális éltávolság méterben a gráfhoz adáshoz
max_distance_for_merge = 2  # Maximális éltávolság méterben az összeolvasztáshoz
feet = 0.3048   # láb váltószáma

# Réteg betöltése
layer = iface.activeLayer()
features = list(layer.getFeatures())
temp_features = features.copy()

# Gráf és térbeli index inicializálása
graph = nx.Graph()
spatial_index = QgsSpatialIndex()
distances = []
createGraph()
showGraph()
createLayer()
stats()
showGraph()










