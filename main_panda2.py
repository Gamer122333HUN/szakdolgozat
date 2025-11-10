import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt



def process_shapefile(shapefile_path):
    g = gpd.read_file(shapefile_path)
    return gpd.GeoSeries(g["geometry"])

def createGraph():
    i = 0
    for geom in gdf:
        centroid = geom.centroid()
        fid = i
        graph.add_node(fid, pos=centroid)

        i+=1

    # Élek hozzáadása
    for i in range(len(gdf) - 1):
        for k in range(i + 1, len(gdf)):
            shortest_line = gdf[i].shortestLine(gdf[k])
            distance = shortest_line.length()
            #distances.append(distance)
            if distance < max_distance_for_graph:
                graph.add_edge(i, k, weight=distance)

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

def showMap():
    gdf.plot()
    plt.show()

shapefile_path = "asd.shp"
gdf = process_shapefile(shapefile_path)
graph = nx.Graph()
max_distance_for_graph = 3000





process_shapefile(shapefile_path)
createGraph()
showGraph()
showMap()


