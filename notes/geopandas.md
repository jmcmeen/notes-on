# Introduction to GeoPandas

## Table of Contents

- [What is GeoPandas](#what-is-geopandas)
- [Installation](#installation)
- [GeoDataFrame Basics](#geodataframe-basics)
- [Reading Spatial Data](#reading-spatial-data)
- [Creating GeoDataFrames](#creating-geodataframes)
- [Coordinate Reference Systems](#coordinate-reference-systems)
- [Geometric Operations](#geometric-operations)
- [Spatial Joins](#spatial-joins)
- [Spatial Queries](#spatial-queries)
- [Plotting](#plotting)
- [Dissolve and Aggregate](#dissolve-and-aggregate)
- [Overlay Operations](#overlay-operations)
- [Distance and Area Calculations](#distance-and-area-calculations)
- [Geocoding](#geocoding)
- [Writing Spatial Data](#writing-spatial-data)
- [Integration with Folium](#integration-with-folium)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is GeoPandas

GeoPandas extends the popular Pandas library with spatial data capabilities. It combines the data manipulation power of Pandas with the geometric operations of Shapely and the file I/O of Fiona, providing a high-level interface for working with geospatial data in Python.

```python
import geopandas as gpd
from shapely.geometry import Point

# GeoPandas = Pandas + spatial capabilities
# A GeoDataFrame is a Pandas DataFrame with a geometry column
gdf = gpd.GeoDataFrame({
    "city": ["San Francisco", "New York", "Chicago"],
    "population": [874961, 8336817, 2693976],
    "geometry": [
        Point(-122.4194, 37.7749),   # (longitude, latitude)
        Point(-73.9857, 40.7484),
        Point(-87.6298, 41.8781)
    ]
}, crs="EPSG:4326")  # set coordinate reference system

# All Pandas operations work on GeoDataFrames
print(gdf[gdf["population"] > 1000000])  # filter rows
print(gdf["population"].mean())           # compute statistics

# Plus spatial operations
print(gdf.area)          # area of each geometry
print(gdf.centroid)      # centroid of each geometry
print(gdf.total_bounds)  # bounding box of all geometries
```

---

## Installation

```python
# Install with pip
# pip install geopandas

# Install with conda (recommended, handles system dependencies)
# conda install -c conda-forge geopandas

# GeoPandas depends on:
# - pandas: data manipulation
# - shapely: geometric operations
# - fiona: file I/O (reads/writes spatial formats)
# - pyproj: coordinate transformations
# - pyogrio: fast I/O engine (optional, faster than fiona)

# Optional dependencies for additional functionality:
# pip install contextily     # basemaps for plotting
# pip install folium         # interactive web maps
# pip install mapclassify    # classification schemes for choropleth maps
# pip install rtree          # spatial indexing for faster queries

# Verify installation
import geopandas as gpd
print(gpd.__version__)
print(gpd.show_versions())
```

---

## GeoDataFrame Basics

The GeoDataFrame is the core data structure in GeoPandas.

```python
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon, LineString

# A GeoDataFrame has one special column: the geometry column
gdf = gpd.GeoDataFrame({
    "name": ["Park A", "Park B", "Park C"],
    "area_acres": [50, 120, 30],
    "geometry": [
        Polygon([(-122.43, 37.77), (-122.41, 37.77),
                 (-122.41, 37.79), (-122.43, 37.79)]),
        Polygon([(-122.45, 37.75), (-122.43, 37.75),
                 (-122.43, 37.77), (-122.45, 37.77)]),
        Polygon([(-122.40, 37.78), (-122.39, 37.78),
                 (-122.39, 37.79), (-122.40, 37.79)])
    ]
}, crs="EPSG:4326")

# The geometry column is a GeoSeries
print(type(gdf.geometry))           # <class 'geopandas.GeoSeries'>
print(gdf.geometry.name)            # "geometry" (column name)

# Access geometry properties
print(gdf.geometry.geom_type)       # geometry type of each row
print(gdf.geometry.is_valid)        # check if geometries are valid
print(gdf.geometry.bounds)          # bounding box per geometry
print(gdf.total_bounds)             # bounding box of entire dataset

# Inspect the GeoDataFrame like a regular DataFrame
print(gdf.head())
print(gdf.dtypes)                   # geometry column shows as "geometry"
print(gdf.shape)                    # (rows, columns)
print(gdf.columns.tolist())

# Multiple geometry columns are possible
# Set the active geometry column
gdf["centroid_geom"] = gdf.geometry.centroid
gdf = gdf.set_geometry("centroid_geom")  # switch active geometry
gdf = gdf.set_geometry("geometry")       # switch back
```

---

## Reading Spatial Data

GeoPandas can read many spatial file formats.

```python
import geopandas as gpd

# Read a shapefile (most common GIS format)
gdf = gpd.read_file("data/neighborhoods.shp")
# Automatically reads the .shp, .shx, .dbf, and .prj companion files

# Read a GeoJSON file
gdf = gpd.read_file("data/parks.geojson")

# Read a GeoPackage (modern alternative to shapefiles)
gdf = gpd.read_file("data/city_data.gpkg", layer="buildings")

# Read from a URL
gdf = gpd.read_file("https://example.com/data/boundaries.geojson")

# Read a KML file
gpd.io.file.fiona.drvsupport.supported_drivers["KML"] = "rw"  # enable KML
gdf = gpd.read_file("data/places.kml")

# Read only specific rows (for large files)
gdf = gpd.read_file("data/large_dataset.shp", rows=1000)  # first 1000 rows

# Read with bounding box filter (only features in this area)
gdf = gpd.read_file(
    "data/buildings.shp",
    bbox=(-122.45, 37.75, -122.40, 37.80)  # (minx, miny, maxx, maxy)
)

# Read with SQL-like filter (attribute filter)
gdf = gpd.read_file(
    "data/cities.gpkg",
    where="population > 100000"  # only load large cities
)

# Inspect after reading
print(f"Shape: {gdf.shape}")
print(f"CRS: {gdf.crs}")
print(f"Geometry types: {gdf.geom_type.unique()}")
print(f"Bounds: {gdf.total_bounds}")
print(gdf.head())
```

---

## Creating GeoDataFrames

Build GeoDataFrames from coordinates, DataFrames, or WKT strings.

```python
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon, LineString
from shapely import wkt

# From a Pandas DataFrame with lat/lon columns
df = pd.DataFrame({
    "name": ["San Francisco", "New York", "Chicago", "Seattle"],
    "lat": [37.7749, 40.7484, 41.8781, 47.6062],
    "lon": [-122.4194, -73.9857, -87.6298, -122.3321],
    "population": [874961, 8336817, 2693976, 737015]
})

# Convert to GeoDataFrame using points_from_xy
gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df["lon"], df["lat"]),  # (x=lon, y=lat)
    crs="EPSG:4326"
)
print(gdf)

# From a list of Shapely geometries
polygons = [
    Polygon([(-122.43, 37.77), (-122.41, 37.77),
             (-122.41, 37.79), (-122.43, 37.79)]),
    Polygon([(-122.45, 37.75), (-122.43, 37.75),
             (-122.43, 37.77), (-122.45, 37.77)])
]
gdf = gpd.GeoDataFrame(
    {"name": ["Zone A", "Zone B"], "zone_type": ["residential", "commercial"]},
    geometry=polygons,
    crs="EPSG:4326"
)

# From WKT (Well-Known Text) strings
df = pd.DataFrame({
    "name": ["Route 1", "Route 2"],
    "wkt": [
        "LINESTRING(-122.42 37.78, -122.41 37.77, -122.40 37.78)",
        "LINESTRING(-122.43 37.79, -122.42 37.78, -122.41 37.79)"
    ]
})
df["geometry"] = df["wkt"].apply(wkt.loads)  # parse WKT to Shapely objects
gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")
gdf = gdf.drop(columns=["wkt"])  # remove the WKT string column

# From a dictionary of coordinates (creating polygons)
import numpy as np

# Create a grid of square polygons
cells = []
for x in np.arange(-122.5, -122.3, 0.02):
    for y in np.arange(37.7, 37.85, 0.02):
        cell = Polygon([
            (x, y), (x + 0.02, y),
            (x + 0.02, y + 0.02), (x, y + 0.02)
        ])
        cells.append(cell)

grid = gpd.GeoDataFrame(geometry=cells, crs="EPSG:4326")
grid["cell_id"] = range(len(grid))
```

---

## Coordinate Reference Systems

Managing CRS is essential for accurate spatial analysis.

```python
import geopandas as gpd

# Check the CRS of a GeoDataFrame
gdf = gpd.read_file("data/cities.geojson")
print(gdf.crs)              # EPSG:4326 (WGS84, lat/lon in degrees)
print(gdf.crs.to_epsg())    # 4326
print(gdf.crs.name)         # "WGS 84"
print(gdf.crs.is_geographic)  # True (uses degrees)
print(gdf.crs.is_projected)   # False (not in meters/feet)

# Set CRS for data that has no CRS defined
gdf = gdf.set_crs("EPSG:4326")
# or with WKT error handling
gdf = gdf.set_crs("EPSG:4326", allow_override=True)  # override existing CRS

# Transform (reproject) to a different CRS
# to_crs transforms coordinates; set_crs only declares the CRS

# Transform to UTM Zone 10N (meters) for distance/area calculations
gdf_utm = gdf.to_crs("EPSG:32610")
print(gdf_utm.crs.axis_info)  # units are now meters

# Transform to Web Mercator (for web mapping)
gdf_web = gdf.to_crs("EPSG:3857")

# Transform to an equal-area projection (for area calculations)
gdf_equal_area = gdf.to_crs("EPSG:6933")  # World Cylindrical Equal Area

# Common CRS codes:
# EPSG:4326  - WGS84 (GPS coordinates, lat/lon in degrees)
# EPSG:3857  - Web Mercator (Google Maps, OpenStreetMap, units in meters)
# EPSG:32610 - UTM Zone 10N (western US, units in meters)
# EPSG:2163  - US National Atlas Equal Area
# EPSG:27700 - British National Grid

# Transform using a proj4 string (for custom projections)
gdf_custom = gdf.to_crs("+proj=aea +lat_1=29.5 +lat_2=45.5 +datum=WGS84")
```

---

## Geometric Operations

Shapely-powered operations on GeoSeries and GeoDataFrames.

```python
import geopandas as gpd

# Load example data
neighborhoods = gpd.read_file("data/neighborhoods.geojson")
points = gpd.read_file("data/locations.geojson")

# Buffer: expand geometries by a distance
# Must be in a projected CRS for meaningful distance units
neighborhoods_utm = neighborhoods.to_crs("EPSG:32610")
buffered = neighborhoods_utm.buffer(500)  # 500 meter buffer around each polygon
# Returns a GeoSeries of buffered geometries

# Buffer with different distances per row
neighborhoods_utm["buffer_dist"] = [100, 200, 300, 500, 150]
buffered_custom = neighborhoods_utm.geometry.buffer(neighborhoods_utm["buffer_dist"])

# Centroid: center point of each geometry
centroids = neighborhoods.centroid  # returns GeoSeries of Points
neighborhoods["centroid"] = centroids

# Convex hull: smallest convex polygon enclosing each geometry
hulls = neighborhoods.convex_hull

# Envelope: bounding rectangle for each geometry
bboxes = neighborhoods.envelope

# Simplify: reduce number of vertices (for display/performance)
simplified = neighborhoods.simplify(tolerance=0.001, preserve_topology=True)

# Unary union: merge all geometries into one
merged = neighborhoods.union_all()  # single geometry containing all neighborhoods
# Older API: neighborhoods.unary_union

# Intersection of two GeoSeries (element-wise)
result = gdf1.intersection(gdf2)

# Difference: subtract one geometry from another (element-wise)
result = gdf1.difference(gdf2)

# Symmetric difference: area in either but not both
result = gdf1.symmetric_difference(gdf2)

# Boundary: the boundary of each polygon (returns linestrings)
borders = neighborhoods.boundary

# Exterior coordinates of polygons
for idx, row in neighborhoods.iterrows():
    coords = list(row.geometry.exterior.coords)
    print(f"{row['name']}: {len(coords)} vertices")
```

---

## Spatial Joins

Combine GeoDataFrames based on spatial relationships.

```python
import geopandas as gpd

# Load data
points = gpd.read_file("data/restaurants.geojson")      # point data
polygons = gpd.read_file("data/neighborhoods.geojson")   # polygon data

# sjoin: spatial join based on geometric relationship
# Find which neighborhood each restaurant is in
joined = gpd.sjoin(
    points,           # left GeoDataFrame (the points)
    polygons,         # right GeoDataFrame (the polygons)
    how="inner",      # inner, left, right (like pandas merge)
    predicate="within"  # spatial relationship to test
)
# Result has columns from both DataFrames
# Plus "index_right" showing which polygon matched
print(joined[["restaurant_name", "neighborhood_name"]].head())

# Spatial predicates for sjoin:
# "intersects" - geometries share any space (most permissive)
# "within"     - left geometry is entirely inside right geometry
# "contains"   - left geometry entirely contains right geometry
# "crosses"    - geometries cross each other

# Left join: keep all restaurants, even those not in any neighborhood
joined_left = gpd.sjoin(points, polygons, how="left", predicate="within")
# Restaurants not in any neighborhood will have NaN for polygon columns

# Count points in polygons
# "How many restaurants per neighborhood?"
count_by_neighborhood = (
    gpd.sjoin(points, polygons, predicate="within")
    .groupby("neighborhood_name")
    .size()
    .reset_index(name="restaurant_count")
)
print(count_by_neighborhood)

# sjoin_nearest: join based on proximity (nearest neighbor)
# Find the nearest park to each restaurant
nearest = gpd.sjoin_nearest(
    points,                # left: restaurants
    parks,                 # right: parks
    how="left",
    max_distance=1000,     # maximum distance in CRS units
    distance_col="dist"    # column name for the distance
)
print(nearest[["restaurant_name", "park_name", "dist"]].head())
```

---

## Spatial Queries

Filter GeoDataFrames based on spatial criteria.

```python
import geopandas as gpd
from shapely.geometry import box, Point

# Load data
buildings = gpd.read_file("data/buildings.geojson")

# cx indexer: filter by bounding box (coordinate-based indexing)
# Select buildings within a bounding box
subset = buildings.cx[-122.45:-122.40, 37.75:37.80]
# cx[xmin:xmax, ymin:ymax] - note: x=longitude, y=latitude
print(f"Buildings in bbox: {len(subset)}")

# clip: cut geometries to a region
# Like a cookie cutter - geometries are clipped to the mask boundary
clip_region = gpd.GeoDataFrame(
    geometry=[box(-122.43, 37.77, -122.41, 37.79)],
    crs="EPSG:4326"
)
clipped = gpd.clip(buildings, clip_region)
# Polygons crossing the boundary are cut; points outside are removed

# Boolean spatial filtering with geometry methods
search_area = Point(-122.42, 37.78).buffer(0.01)  # ~1km radius

# Filter using Shapely predicates
mask = buildings.geometry.within(search_area)  # boolean Series
nearby_buildings = buildings[mask]

mask_intersects = buildings.geometry.intersects(search_area)
intersecting = buildings[mask_intersects]

# Filter by distance
reference_point = Point(-122.42, 37.78)
buildings_utm = buildings.to_crs("EPSG:32610")
ref_utm = gpd.GeoSeries([reference_point], crs="EPSG:4326").to_crs("EPSG:32610")[0]

distances = buildings_utm.geometry.distance(ref_utm)
within_500m = buildings_utm[distances < 500]  # buildings within 500 meters
print(f"Buildings within 500m: {len(within_500m)}")

# Sindex: spatial index for fast queries
# GeoPandas builds an R-tree index automatically when needed
# Manual spatial index query:
sindex = buildings.sindex
possible_matches_idx = list(sindex.intersection(search_area.bounds))
possible_matches = buildings.iloc[possible_matches_idx]
# Then do precise filtering on the candidates
precise_matches = possible_matches[possible_matches.intersects(search_area)]
```

---

## Plotting

GeoPandas provides built-in matplotlib-based plotting.

```python
import geopandas as gpd
import matplotlib.pyplot as plt

# Load data
neighborhoods = gpd.read_file("data/neighborhoods.geojson")

# Basic plot
neighborhoods.plot()
plt.title("Neighborhoods")
plt.show()

# Column-based coloring (choropleth)
neighborhoods.plot(
    column="population",      # color by this column
    cmap="YlOrRd",            # color map (yellow-orange-red)
    legend=True,              # show color bar legend
    legend_kwds={"label": "Population"},
    edgecolor="black",        # polygon border color
    linewidth=0.5,            # border line width
    figsize=(12, 8)
)
plt.title("Neighborhood Population")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.tight_layout()
plt.show()

# Classification schemes for choropleth maps (requires mapclassify)
neighborhoods.plot(
    column="median_income",
    scheme="quantiles",       # equal count bins
    k=5,                      # number of classes
    cmap="Blues",
    legend=True,
    legend_kwds={"title": "Income Quantiles"},
    figsize=(12, 8)
)
plt.show()

# Other schemes: "equal_interval", "natural_breaks", "fisher_jenks"

# Plot multiple layers
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
neighborhoods.plot(ax=ax, color="lightgray", edgecolor="black")  # base layer
parks.plot(ax=ax, color="green", alpha=0.5)                       # parks overlay
schools.plot(ax=ax, color="red", markersize=10, label="Schools")  # point layer
ax.legend()
ax.set_title("Neighborhoods, Parks, and Schools")
plt.show()

# Add a basemap with contextily
import contextily as cx

# Must be in Web Mercator (EPSG:3857) for contextily basemaps
gdf_3857 = neighborhoods.to_crs("EPSG:3857")
ax = gdf_3857.plot(
    column="population",
    cmap="viridis",
    alpha=0.6,
    legend=True,
    figsize=(12, 8)
)
cx.add_basemap(ax, source=cx.providers.OpenStreetMap.Mapnik)
ax.set_title("Neighborhoods on Basemap")
plt.show()

# Side-by-side comparison plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
neighborhoods.plot(ax=ax1, column="population", cmap="Reds", legend=True)
ax1.set_title("Population")
neighborhoods.plot(ax=ax2, column="median_income", cmap="Greens", legend=True)
ax2.set_title("Median Income")
plt.tight_layout()
plt.show()
```

---

## Dissolve and Aggregate

Combine geometries and aggregate data based on attributes.

```python
import geopandas as gpd

# Load county-level data
counties = gpd.read_file("data/counties.geojson")
print(counties.head())
# Columns: name, state, population, area_sqmi, geometry

# Dissolve: merge geometries by a grouping column
# Similar to pandas groupby, but also merges geometries
states = counties.dissolve(
    by="state",          # group by this column
    aggfunc={            # aggregation for non-geometry columns
        "population": "sum",
        "area_sqmi": "sum",
        "name": "count"  # count counties per state
    }
)
states = states.rename(columns={"name": "county_count"})
print(states.head())
# Each row is a state with merged geometry and summed population

# Dissolve without aggregation (just merge all geometries)
all_merged = counties.dissolve()  # single row with one merged geometry

# Dissolve with multiple aggregation functions
states_detailed = counties.dissolve(
    by="state",
    aggfunc={
        "population": ["sum", "mean", "max"],
        "area_sqmi": "sum"
    }
)

# Explode: opposite of dissolve - split multi-part geometries
# MultiPolygon -> individual Polygons
exploded = states.explode(index_parts=True)
print(f"Before explode: {len(states)} rows")
print(f"After explode: {len(exploded)} rows")  # more rows (islands, etc.)
```

---

## Overlay Operations

Combine two GeoDataFrames using set-like operations.

```python
import geopandas as gpd

# Load two polygon layers
land_use = gpd.read_file("data/land_use.geojson")
flood_zones = gpd.read_file("data/flood_zones.geojson")

# Intersection: area common to both layers
# "Where does land use overlap with flood zones?"
intersected = gpd.overlay(land_use, flood_zones, how="intersection")
# Result contains only the overlapping areas
# with attributes from both input layers

# Union: combined area from both layers (all areas)
combined = gpd.overlay(land_use, flood_zones, how="union")
# Result includes: areas in both, areas only in left, areas only in right

# Difference: area in first layer but NOT in second
# "What land use areas are outside flood zones?"
safe_areas = gpd.overlay(land_use, flood_zones, how="difference")

# Symmetric difference: areas in either but not both
# "Areas that are in one layer or the other, but not overlapping"
sym_diff = gpd.overlay(land_use, flood_zones, how="symmetric_difference")

# Identity: keeps all of first layer, splits where second layer overlaps
identity = gpd.overlay(land_use, flood_zones, how="identity")
# Like intersection, but keeps the non-overlapping parts of the first layer too

# Practical example: calculate flood risk by land use type
intersection = gpd.overlay(land_use, flood_zones, how="intersection")
intersection["overlap_area"] = intersection.to_crs("EPSG:6933").area  # sq meters
flood_risk_summary = (
    intersection.groupby("land_use_type")["overlap_area"]
    .sum()
    .sort_values(ascending=False)
)
print(flood_risk_summary)
```

---

## Distance and Area Calculations

Accurate measurements require appropriate projections.

```python
import geopandas as gpd
from shapely.geometry import Point

# Load data
cities = gpd.read_file("data/cities.geojson")  # EPSG:4326

# IMPORTANT: calculations in EPSG:4326 give results in degrees (not useful)
# Always project to a metric CRS first

# Project to UTM for accurate measurements
cities_utm = cities.to_crs("EPSG:32610")  # UTM Zone 10N (meters)

# Distance between all cities and a reference point
ref_point = gpd.GeoSeries([Point(-122.4194, 37.7749)], crs="EPSG:4326")
ref_utm = ref_point.to_crs("EPSG:32610")[0]

cities_utm["dist_to_sf_m"] = cities_utm.geometry.distance(ref_utm)
cities_utm["dist_to_sf_km"] = cities_utm["dist_to_sf_m"] / 1000
print(cities_utm[["name", "dist_to_sf_km"]].sort_values("dist_to_sf_km"))

# Distance matrix: distance between every pair of cities
import numpy as np

n = len(cities_utm)
dist_matrix = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        dist_matrix[i][j] = cities_utm.geometry.iloc[i].distance(
            cities_utm.geometry.iloc[j]
        )

# Convert to DataFrame for readability
import pandas as pd
dist_df = pd.DataFrame(
    dist_matrix / 1000,  # convert to km
    index=cities_utm["name"],
    columns=cities_utm["name"]
)
print(dist_df.round(1))

# Area calculations for polygons
neighborhoods = gpd.read_file("data/neighborhoods.geojson")
neighborhoods_proj = neighborhoods.to_crs("EPSG:32610")  # project to meters

neighborhoods_proj["area_sqm"] = neighborhoods_proj.area
neighborhoods_proj["area_sqkm"] = neighborhoods_proj.area / 1_000_000
neighborhoods_proj["area_acres"] = neighborhoods_proj.area * 0.000247105

print(neighborhoods_proj[["name", "area_sqkm", "area_acres"]].head())

# Perimeter / length calculations
neighborhoods_proj["perimeter_m"] = neighborhoods_proj.length
roads_proj = roads.to_crs("EPSG:32610")
roads_proj["length_km"] = roads_proj.length / 1000
```

---

## Geocoding

Convert addresses to coordinates and vice versa.

```python
import geopandas as gpd

# Forward geocoding: address to coordinates
# Requires a geocoding provider (Nominatim is free but rate-limited)
from geopandas.tools import geocode

# Geocode a list of addresses
addresses = [
    "1600 Pennsylvania Ave NW, Washington, DC",
    "350 Fifth Avenue, New York, NY",
    "600 Navarro St, San Antonio, TX"
]

# Using Nominatim (free, OpenStreetMap-based)
geocoded = geocode(
    addresses,
    provider="nominatim",
    user_agent="my_geocoding_app"  # required by Nominatim
)
print(geocoded)
# Returns a GeoDataFrame with Point geometries and address info

# Reverse geocoding: coordinates to addresses
from geopandas.tools import reverse_geocode
from shapely.geometry import Point

points = [
    Point(-77.0365, 38.8977),    # White House
    Point(-73.9857, 40.7484),    # Empire State Building
]

reverse = reverse_geocode(
    points,
    provider="nominatim",
    user_agent="my_geocoding_app"
)
print(reverse["address"])

# Using a different provider (e.g., Google, requires API key)
# geocoded = geocode(addresses, provider="google", api_key="YOUR_KEY")

# Geocoding a DataFrame column
import pandas as pd

df = pd.DataFrame({
    "name": ["White House", "Empire State", "Space Needle"],
    "address": [
        "1600 Pennsylvania Ave NW, Washington, DC",
        "350 Fifth Avenue, New York, NY",
        "400 Broad St, Seattle, WA"
    ]
})

geocoded = geocode(df["address"], provider="nominatim", user_agent="my_app")
gdf = gpd.GeoDataFrame(df, geometry=geocoded.geometry, crs="EPSG:4326")
print(gdf)
```

---

## Writing Spatial Data

Export GeoDataFrames to various spatial file formats.

```python
import geopandas as gpd

gdf = gpd.read_file("data/neighborhoods.geojson")

# Write to GeoJSON
gdf.to_file("output/neighborhoods.geojson", driver="GeoJSON")

# Write to shapefile
gdf.to_file("output/neighborhoods.shp")  # shapefile is the default driver
# Creates: .shp, .shx, .dbf, .prj files

# Write to GeoPackage (recommended modern format)
gdf.to_file("output/data.gpkg", layer="neighborhoods", driver="GPKG")
# Can write multiple layers to the same .gpkg file
parks.to_file("output/data.gpkg", layer="parks", driver="GPKG")

# Write to CSV with WKT geometry
gdf["wkt"] = gdf.geometry.to_wkt()  # convert geometry to WKT strings
gdf.drop(columns=["geometry"]).to_csv("output/data.csv", index=False)

# Write to Parquet (fast, columnar format, good for large datasets)
gdf.to_parquet("output/neighborhoods.parquet")

# Read Parquet back
gdf_from_parquet = gpd.read_parquet("output/neighborhoods.parquet")

# Write to PostGIS
from sqlalchemy import create_engine

engine = create_engine("postgresql://user:password@localhost/mydb")
gdf.to_postgis("neighborhoods", engine, if_exists="replace", index=True)

# Read from PostGIS
gdf_from_db = gpd.read_postgis(
    "SELECT * FROM neighborhoods WHERE population > 10000",
    engine,
    geom_col="geometry"
)
```

---

## Integration with Folium

Create interactive web maps from GeoPandas data.

```python
import geopandas as gpd
import folium

# Load data
neighborhoods = gpd.read_file("data/neighborhoods.geojson")
restaurants = gpd.read_file("data/restaurants.geojson")

# Create a base map centered on the data
center = [neighborhoods.geometry.centroid.y.mean(),
          neighborhoods.geometry.centroid.x.mean()]
m = folium.Map(location=center, zoom_start=12)

# Add GeoDataFrame as a GeoJSON layer
folium.GeoJson(
    neighborhoods,
    name="Neighborhoods",
    style_function=lambda feature: {
        "fillColor": "lightblue",
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.4
    },
    tooltip=folium.GeoJsonTooltip(fields=["name", "population"])
).add_to(m)

# Add points as markers
for _, row in restaurants.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=f"{row['name']}<br>Cuisine: {row['cuisine']}",
        tooltip=row["name"],
        icon=folium.Icon(color="red", icon="cutlery", prefix="fa")
    ).add_to(m)

# Choropleth map from GeoDataFrame
folium.Choropleth(
    geo_data=neighborhoods,
    data=neighborhoods,
    columns=["name", "median_income"],
    key_on="feature.properties.name",
    fill_color="YlGn",
    fill_opacity=0.7,
    legend_name="Median Income"
).add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# Save the interactive map
m.save("output/interactive_map.html")
```

```python
# Using the explore() method (built-in GeoPandas + Folium integration)
# This is the quickest way to get an interactive map

# Simple interactive map
m = neighborhoods.explore(
    column="population",       # color by this column
    cmap="YlOrRd",             # color map
    legend=True,
    tooltip=["name", "population"],
    popup=True,                # show all columns on click
    tiles="CartoDB positron",  # basemap tiles
    style_kwds={"weight": 1, "fillOpacity": 0.6}
)

# Add another layer to the same map
restaurants.explore(
    m=m,                       # add to existing map
    color="red",
    marker_kwds={"radius": 5},
    tooltip=["name", "cuisine"]
)

m.save("output/explore_map.html")
```

---

## Practice Exercises

1. **Load and explore**: Read a GeoJSON or shapefile into a GeoDataFrame. Print its CRS, geometry types, number of features, and total bounds. Plot it with column-based coloring.

2. **Create from coordinates**: Build a GeoDataFrame from a CSV file with latitude and longitude columns. Set the CRS to EPSG:4326 and plot the points.

3. **Spatial join**: Load a points layer (e.g., schools) and a polygons layer (e.g., districts). Use sjoin to find which district each school belongs to. Count schools per district.

4. **Buffer analysis**: Buffer all school points by 500 meters (project to UTM first). Find which buildings fall within any school buffer using spatial join.

5. **Overlay**: Perform an intersection overlay between land use zones and flood risk zones. Calculate the area of each intersection and summarize by land use type.

6. **Distance matrix**: Calculate the distance in kilometers between 5 cities. Display as a formatted DataFrame.

7. **Interactive map**: Create a Folium map showing neighborhoods as a choropleth (colored by population) with school locations as markers. Save as HTML.

---

## Summary

GeoPandas brings spatial data capabilities to the Pandas ecosystem. Key takeaways:

- **GeoDataFrame**: extends DataFrame with a geometry column and spatial methods
- **Reading data**: supports shapefiles, GeoJSON, GeoPackage, and many other formats via read_file
- **CRS management**: set_crs declares, to_crs transforms; always project to metric CRS for measurements
- **Geometric operations**: buffer, intersection, union, difference, centroid, simplify via Shapely
- **Spatial joins**: sjoin combines DataFrames based on spatial relationships (within, intersects, contains)
- **Plotting**: built-in matplotlib plots with column-based coloring, basemaps via contextily
- **Dissolve**: merge geometries by attribute with aggregation (like spatial groupby)
- **Overlay**: intersection, union, difference between polygon layers
- **Measurements**: project to metric CRS, then use .area, .length, .distance()
- **Integration**: works with Folium for interactive maps, PostGIS for databases

---

## Next Steps

- Learn Folium for rich interactive web maps
- Explore PostGIS for server-side spatial queries on large datasets
- Study raster data with rasterio and xarray
- Practice spatial analysis workflows combining GeoPandas with scikit-learn
- Build spatial data pipelines with GeoPandas and Airflow
- Learn about spatial statistics with PySAL

---

## Additional Resources

- [GeoPandas Official Documentation](https://geopandas.org/en/stable/)
- [GeoPandas User Guide](https://geopandas.org/en/stable/docs/user_guide.html)
- [Shapely Documentation](https://shapely.readthedocs.io/)
- [contextily Documentation](https://contextily.readthedocs.io/)
- [mapclassify Documentation](https://pysal.org/mapclassify/)
- [Fiona Documentation](https://fiona.readthedocs.io/)
- [CRS Explorer (epsg.io)](https://epsg.io/)
- [Automating GIS Processes Course](https://autogis-site.readthedocs.io/)
