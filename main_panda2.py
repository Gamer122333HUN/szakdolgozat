import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt



def process_shapefile(shapefile_path):
    g = gpd.read_file(shapefile_path)
    return gpd.GeoSeries(g["geometry"]).to_crs("EPSG:3857")

def createGraph():

    centroid = gdf.centroid
    i = 0
    for item in centroid:
        graph.add_node(i, pos=(item.x, item.y))

        i+=1


    # Élek hozzáadása
    geoms = gdf.copy()

    i=0
    for item in gdf:
        geoms = geoms.iloc[1:]
        asd = geoms.distance(item, align=False)
        k = 1
        for item2 in asd:
            if item2 < max_distance_for_graph:
                graph.add_edge(i, k, weight=item2)
            k+=1
        i+=1


def showGraph():

    pos = nx.get_node_attributes(graph, 'pos')
    fig, ax = plt.subplots(figsize=(10, 10))

    nx.draw(graph, pos, ax=ax, with_labels=True, node_size=20)
    rounded_labels = {
        (u, v): f"{d['weight']:.2f}"
        for u, v, d in graph.edges(data=True)
    }

    #labels = nx.get_edge_attributes(graph, 'weight')
    #nx.draw_networkx_edge_labels(graph, pos, edge_labels=rounded_labels)
    gdf.plot(ax=ax, markersize=500, zorder=1)
    plt.show()

#shapefile_path = "asd.shp"űs

shapefile_path = "shapefiles/alaska/trees.shp"
gdf = process_shapefile(shapefile_path)
graph = nx.Graph()
max_distance_for_graph = 50000





process_shapefile(shapefile_path)
createGraph()
showGraph()
print(graph)


