from qgis.core import *
import networkx as nx
import matplotlib.pyplot as plt
import math


def selectById(szam):
    for feature in features:
        if szam == feature.id():
            return features.index(szam)

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
            geom1c = geom1.buffer(distance, 20)
            geom2c = geom2.buffer(distance, 20)
            intersection=geom1c.intersection(geom2c)
            area=intersection.area()
            distances.append(area)
            if distance < max_distance_for_graph:
                graph.add_edge(features[i].id(), features[k].id(), weight=area)

def stats():
    print(f"CRS: {layer.crs()}")
    print(f"Csúcsok száma: {graph.number_of_nodes()}")
    print(f"Élek száma: {graph.number_of_edges()}")
    print(f"max táv: {max(distances)}")
    print(f"min táv: {min(distances)}")
    print(f"átl táv: {sum(distances) / len(distances)}")

def showGraph():
    pos = nx.get_node_attributes(graph, 'pos')
    nx.draw(graph, pos, with_labels=False, node_size=20)
    rounded_labels = {
        (u, v): f"{d['weight']:.2f}"
        for u, v, d in graph.edges(data=True)
    }
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=rounded_labels)
    plt.show()

def createLayer():
    name = f"new_{layer.name()}"
    crs = layer.crs()
    geometry = layer.geometry()


def transformCRS():
    target_crs = QgsCoordinateReferenceSystem("EPSG:3857")
    output_path = "/tmp/layer_temp.shp"

    error = QgsVectorFileWriter.writeAsVectorFormat(
        input_layer,
        output_path,
        "UTF-8",
        target_crs,
        driverName="ESRI Shapefile"
    )

    if error == QgsVectorFileWriter.NoError:
        layer = QgsVectorLayer(output_path, "Réteg EOV-ban", "ogr")
        QgsProject.instance().addMapLayer(layer)
        print("Sikeresen átalakítva és betöltve.")
    else:
        print("Hiba történt a mentés során.")
    return layer

# Beállítások
max_distance_for_graph = 2  # Maximális éltávolság méterben a gráfhoz adáshoz
max_distance_for_merge = 1  # Maximális éltávolság méterben az összeolvasztáshoz
feet = 0.3048   # láb váltószáma

# Réteg betöltése
layer = iface.activeLayer()
#if layer.crs() is "EPSG:4326":
#    layer = transformCRS()
features = list(layer.getFeatures())

# Gráf és térbeli index inicializálása
graph = nx.Graph()
spatial_index = QgsSpatialIndex()
distances = []

createGraph()




stats()
showGraph()








