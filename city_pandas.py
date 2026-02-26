import networkx as nx
import time
import geopandas as gpd
import re
import matplotlib.pyplot as plt




def remove_Points():
    pattern = r"^node.*"
    szamok = []
    for i in range(0, len(gdf["id"])):
        if re.search(pattern, gdf.iloc[i]['id']):
            szamok.append(i)
    gdf.drop(szamok, inplace=True)



def createGraph():

    centroid = gdf.centroid
    for i in range(0,len(centroid)-1):
        if(gdf.iloc[i]['id']):
            graph.add_node(gdf.iloc[i]['id'], pos=(centroid[i].x, centroid[i].y))

    # Élek hozzáadása
    for i in range(0, len(gdf["id"])-1):
        geom = gpd.GeoSeries(gdf.iloc[i]['geometry'])
        print(geom.buffer(0.0003))

        '''geoms = gdf["geometry"].copy()
        geoms = geoms.iloc[i+1:]
        asd = geoms.distance(item, align=False)
        k = i+1
        for item2 in asd:
            if item2 < max_distance_for_graph:
                graph.add_edge(i, k, weight=item2)
            k+=1
        i+=1'''

def showGraph_plotter():

    pos = nx.get_node_attributes(graph, 'pos')
    fig, ax = plt.subplots(figsize=(100, 100))

    nx.draw(graph, pos, ax=ax, with_labels=True, node_size=30)
    rounded_labels = {
        (u, v): f"{d['weight']:.2f}"
        for u, v, d in graph.edges(data=True)
    }

    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=rounded_labels)
    #gdf.plot(ax=ax, markersize=500, zorder=1)
    plt.show()

def showMap():
    gdf.plot()
    plt.show()

def teszt():
    gdf2 = gpd.GeoDataFrame({"id",})



graph = nx.Graph()
gdf = gpd.GeoDataFrame(gpd.read_file("szegednk.geojson"))
#remove_Points()
#createGraph()
#showMap()
#showGraph_plotter()
