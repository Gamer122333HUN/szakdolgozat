import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
from shapely import MultiPolygon
import time


def process_shapefile(shapefile_path):
    temp = gpd.read_file(shapefile_path)
    temp.crs = "EPSG:3857"
    return temp

def createGraph():

    centroid = gdf.centroid
    i = 0
    for item in centroid:
        graph.add_node(i, pos=(item.x, item.y))

        i+=1

    # Élek hozzáadása
    i=0
    for item in gdf["geometry"]:
        geoms = gdf["geometry"].copy()
        geoms = geoms.iloc[i+1:]
        asd = geoms.distance(item, align=False)
        k = i+1
        for item2 in asd:
            if item2 < max_distance_for_graph:
                graph.add_edge(i, k, weight=item2)
            k+=1
        i+=1



def merge_polygons():
    return


def showGraph_plotter():

    pos = nx.get_node_attributes(graph, 'pos')
    fig, ax = plt.subplots(figsize=(10, 10))

    nx.draw(graph, pos, ax=ax, with_labels=True, node_size=20)
    rounded_labels = {
        (u, v): f"{d['weight']:.2f}"
        for u, v, d in graph.edges(data=True)
    }

    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=rounded_labels)
    #gdf.plot(ax=ax, markersize=500, zorder=1)
    plt.show()

def showGraph_plotly():
    fig = go.Figure()
    polygondb = 0
    for _, row in gdf.iterrows():
        if type(row.geometry) == MultiPolygon:
            polygons = row.geometry
            for polygon in polygons.geoms:
                x, y = np.array(polygon.exterior.xy)
                fig.add_trace(go.Scattermap(
                    lon=x,
                    lat=y,
                    mode='lines',
                    line=dict(width=2, color='blue'),
                    name=str(row.get('name', 'Polygon'))
                ))
                polygondb+=1
        else:
            x, y = np.array(row.geometry.exterior.xy)
            fig.add_trace(go.Scattermap(
                lon=x,
                lat=y,
                mode='lines',
                line=dict(width=2, color='blue'),
                name=str(row.get('name', 'Polygon'))
            ))
            polygondb+=1

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=5,
        mapbox_center={"lat": gdf.geometry.centroid.y.mean(), "lon": gdf.geometry.centroid.x.mean()},
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    print("megrajzolt poligonok darabszáma: ", polygondb)
    fig.show()



start = time.time()
#shapefile_path = "asd.shp"
#shapefile_path = "shapefiles/alaska/trees.shp"
#shapefile_path = "shapefiles/andorra/gadm41_AND_1.shp"
shapefile_path = "shapefiles/hungary/gadm41_HUN_2.shp"
#shapefile_path = "shapefiles/bahamas/gadm41_BHS_1.shp"
#shapefile_path = "shapefiles/cabo_verde/gadm41_CPV_1.shp"
#gdf = process_shapefile(shapefile_path)
gdf = gpd.read_file("szeged.geojson")
graph = nx.Graph()
max_distance_for_graph = 1




createGraph()
showGraph_plotter()
showGraph_plotly()
print(graph)


end = time.time()
print(f"Futási idő: {end - start:.3f} másodperc")

