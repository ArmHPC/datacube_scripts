import geopandas as gpd
from shapely.geometry import Point


def readShapefile(filename):
    return gpd.read_file(filename)


def isPointInsideShapefile(shapefile, lat, lon):
    # Create a Point geometry
    point = Point(lon, lat)

    return shapefile.contains(point).any()

    # print("Is the point inside the shapefile?", is_inside)