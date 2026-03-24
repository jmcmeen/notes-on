# Introduction to PostGIS

## Table of Contents

- [What is PostGIS](#what-is-postgis)
- [Installation](#installation)
- [Spatial Data Types](#spatial-data-types)
- [Creating Spatial Tables](#creating-spatial-tables)
- [Loading Spatial Data](#loading-spatial-data)
- [Spatial Queries](#spatial-queries)
- [Spatial Joins](#spatial-joins)
- [Coordinate Reference Systems](#coordinate-reference-systems)
- [Spatial Indexing](#spatial-indexing)
- [Measurement Functions](#measurement-functions)
- [Geometry Operations](#geometry-operations)
- [Importing and Exporting](#importing-and-exporting)
- [Python Integration](#python-integration)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is PostGIS

PostGIS is a spatial extension for PostgreSQL that adds support for geographic objects, allowing location-based queries to be run in SQL. It transforms PostgreSQL into a spatial database capable of storing, indexing, and querying geospatial data.

Key capabilities:

- Store points, lines, polygons, and complex geometries
- Perform spatial queries (containment, intersection, proximity)
- Calculate distances, areas, and lengths
- Transform between coordinate reference systems
- Support for both planar (geometry) and geodetic (geography) calculations
- Full SQL integration with spatial operators and functions

```sql
-- A taste of what PostGIS can do
-- Find all restaurants within 1km of a given point
SELECT name, ST_Distance(
    location::geography,
    ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326)::geography
) AS distance_meters
FROM restaurants
WHERE ST_DWithin(
    location::geography,
    ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326)::geography,
    1000  -- 1000 meters = 1 kilometer
)
ORDER BY distance_meters;
```

---

## Installation

PostGIS is installed as a PostgreSQL extension.

```sql
-- Connect to your PostgreSQL database and enable PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;

-- Verify the installation
SELECT PostGIS_Version();
-- Returns something like: "3.4 USE_GEOS=1 USE_PROJ=1 USE_STATS=1"

-- Check full version details
SELECT PostGIS_Full_Version();

-- Additional useful extensions
CREATE EXTENSION IF NOT EXISTS postgis_topology;      -- topological data
CREATE EXTENSION IF NOT EXISTS postgis_raster;         -- raster data support
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;          -- needed for Tiger geocoder
CREATE EXTENSION IF NOT EXISTS postgis_tiger_geocoder; -- US address geocoding
```

Installing PostGIS on the system level:

```bash
# Ubuntu/Debian
sudo apt-get install postgresql-16-postgis-3

# macOS with Homebrew
brew install postgis

# Docker (PostGIS-enabled PostgreSQL image)
docker run -d \
  --name postgis \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  postgis/postgis:16-3.4
```

---

## Spatial Data Types

PostGIS provides two main spatial types: geometry (planar) and geography (spheroidal).

```sql
-- GEOMETRY: uses a flat, Cartesian coordinate system
-- Fast calculations, but distances/areas are in the coordinate system's units
-- Best for: projected data, small areas, most GIS operations

-- GEOGRAPHY: uses a spherical/ellipsoidal model of the earth
-- Slower but accurate distance/area calculations in meters
-- Best for: global data, distance queries, when you need real-world units

-- Point: a single location (longitude, latitude)
SELECT ST_GeomFromText('POINT(-122.4194 37.7749)', 4326);

-- LineString: a path defined by two or more points
SELECT ST_GeomFromText('LINESTRING(-122.42 37.78, -122.41 37.77, -122.40 37.78)', 4326);

-- Polygon: a closed shape (first and last points must match)
SELECT ST_GeomFromText(
    'POLYGON((-122.43 37.77, -122.41 37.77, -122.41 37.79, -122.43 37.79, -122.43 37.77))',
    4326
);

-- MultiPoint: a collection of points
SELECT ST_GeomFromText('MULTIPOINT((-122.42 37.78), (-122.41 37.77))', 4326);

-- MultiLineString: a collection of linestrings
SELECT ST_GeomFromText(
    'MULTILINESTRING((-122.42 37.78, -122.41 37.77), (-122.40 37.78, -122.39 37.77))',
    4326
);

-- MultiPolygon: a collection of polygons (e.g., a state with islands)
SELECT ST_GeomFromText(
    'MULTIPOLYGON(((-122.43 37.77, -122.41 37.77, -122.41 37.79, -122.43 37.79, -122.43 37.77)))',
    4326
);
```

Geometry vs geography comparison:

```sql
-- Geometry: distance in coordinate units (degrees for EPSG:4326)
SELECT ST_Distance(
    ST_GeomFromText('POINT(-122.4194 37.7749)', 4326),
    ST_GeomFromText('POINT(-73.9857 40.7484)', 4326)
);
-- Returns: ~48.87 (degrees, not very useful!)

-- Geography: distance in meters (accurate on the sphere)
SELECT ST_Distance(
    ST_GeogFromText('POINT(-122.4194 37.7749)'),
    ST_GeogFromText('POINT(-73.9857 40.7484)')
);
-- Returns: ~4,129,086 meters (San Francisco to New York)

-- Rule of thumb:
-- Use geometry for most spatial operations (faster, more functions)
-- Use geography when you need accurate distance/area in meters
-- Cast between them: geom::geography or geog::geometry
```

---

## Creating Spatial Tables

```sql
-- Create a table with a geometry column
CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    population INTEGER,
    location GEOMETRY(Point, 4326)  -- Point type with SRID 4326 (WGS84)
);

-- Create a table with different geometry types
CREATE TABLE parks (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    park_type VARCHAR(50),
    boundary GEOMETRY(Polygon, 4326),    -- park boundary as polygon
    entrance GEOMETRY(Point, 4326),       -- main entrance as point
    trails GEOMETRY(MultiLineString, 4326) -- trail network
);

-- Create a table with geography type (for accurate distance queries)
CREATE TABLE airports (
    id SERIAL PRIMARY KEY,
    code CHAR(3) NOT NULL,
    name VARCHAR(200),
    location GEOGRAPHY(Point, 4326)  -- geography for accurate distance
);

-- Add a geometry column to an existing table
ALTER TABLE buildings
ADD COLUMN footprint GEOMETRY(Polygon, 4326);

-- Register the geometry column (older PostGIS style, rarely needed now)
-- SELECT AddGeometryColumn('public', 'buildings', 'footprint', 4326, 'POLYGON', 2);
```

---

## Loading Spatial Data

Multiple ways to insert spatial data into PostGIS.

```sql
-- Using Well-Known Text (WKT) - human-readable format
INSERT INTO cities (name, population, location) VALUES
    ('San Francisco', 874961, ST_GeomFromText('POINT(-122.4194 37.7749)', 4326)),
    ('New York', 8336817, ST_GeomFromText('POINT(-73.9857 40.7484)', 4326)),
    ('Chicago', 2693976, ST_GeomFromText('POINT(-87.6298 41.8781)', 4326)),
    ('Los Angeles', 3979576, ST_GeomFromText('POINT(-118.2437 34.0522)', 4326));

-- Using ST_MakePoint (simpler for points)
INSERT INTO cities (name, population, location) VALUES
    ('Seattle', 737015, ST_SetSRID(ST_MakePoint(-122.3321, 47.6062), 4326)),
    ('Portland', 652503, ST_SetSRID(ST_MakePoint(-122.6765, 45.5152), 4326));

-- Using GeoJSON (common in web applications)
INSERT INTO cities (name, population, location) VALUES
    ('Denver', 715522, ST_GeomFromGeoJSON(
        '{"type": "Point", "coordinates": [-104.9903, 39.7392]}'
    ));

-- Using Well-Known Binary (WKB) - binary format, common in data transfers
-- WKB is typically used programmatically, not typed by hand
INSERT INTO cities (name, population, location) VALUES
    ('Austin', 978908, ST_GeomFromWKB(E'\\x0101...', 4326));

-- Loading a polygon
INSERT INTO parks (name, park_type, boundary) VALUES
    ('Central Park', 'urban',
     ST_GeomFromText(
         'POLYGON((-73.9813 40.7681, -73.9580 40.7681,
                   -73.9580 40.8006, -73.9813 40.8006, -73.9813 40.7681))',
         4326
     ));

-- Generate a point from latitude/longitude columns in an existing table
UPDATE locations SET
    geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)
WHERE geom IS NULL;
```

---

## Spatial Queries

Core spatial query functions for testing relationships between geometries.

```sql
-- ST_Contains: does geometry A contain geometry B?
-- "Find all points inside a polygon"
SELECT c.name
FROM cities c, neighborhoods n
WHERE n.name = 'Downtown'
AND ST_Contains(n.boundary, c.location);  -- neighborhood contains city point

-- ST_Intersects: do two geometries share any space?
-- "Find all roads that cross through a park"
SELECT r.name AS road_name, p.name AS park_name
FROM roads r, parks p
WHERE ST_Intersects(r.geom, p.boundary);

-- ST_Within: is geometry A inside geometry B?
-- Opposite of ST_Contains
SELECT s.name AS school_name
FROM schools s, districts d
WHERE d.name = 'District 5'
AND ST_Within(s.location, d.boundary);  -- school is within district

-- ST_DWithin: are two geometries within a given distance?
-- "Find all restaurants within 500 meters" (uses geography for meters)
SELECT name, cuisine,
    ST_Distance(
        location::geography,
        ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326)::geography
    ) AS distance_m
FROM restaurants
WHERE ST_DWithin(
    location::geography,
    ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326)::geography,
    500  -- 500 meters
)
ORDER BY distance_m;

-- ST_Distance: compute the distance between two geometries
-- With geography type, returns meters
SELECT a.name AS city_a, b.name AS city_b,
    ST_Distance(a.location::geography, b.location::geography) / 1000 AS distance_km
FROM cities a, cities b
WHERE a.name < b.name  -- avoid duplicates
ORDER BY distance_km;

-- ST_Crosses: does a linestring cross through a polygon?
SELECT r.name
FROM rivers r, counties c
WHERE c.name = 'Marin County'
AND ST_Crosses(r.geom, c.boundary);

-- ST_Touches: do geometries share a boundary but not interiors?
SELECT a.name, b.name
FROM parcels a, parcels b
WHERE a.id < b.id
AND ST_Touches(a.boundary, b.boundary);

-- ST_Overlaps: do geometries share some but not all space?
SELECT a.name AS zone_a, b.name AS zone_b
FROM flood_zones a, building_zones b
WHERE ST_Overlaps(a.boundary, b.boundary);
```

---

## Spatial Joins

Combining tables based on spatial relationships.

```sql
-- Basic spatial join: find which neighborhood each restaurant is in
SELECT r.name AS restaurant, n.name AS neighborhood
FROM restaurants r
JOIN neighborhoods n ON ST_Contains(n.boundary, r.location);

-- Count points in polygons: how many schools per district?
SELECT d.name AS district,
    COUNT(s.id) AS school_count
FROM districts d
LEFT JOIN schools s ON ST_Contains(d.boundary, s.location)
GROUP BY d.name
ORDER BY school_count DESC;

-- Nearest neighbor join: find the closest hospital to each fire station
SELECT DISTINCT ON (fs.name)
    fs.name AS fire_station,
    h.name AS nearest_hospital,
    ST_Distance(fs.location::geography, h.location::geography) AS distance_m
FROM fire_stations fs
CROSS JOIN LATERAL (
    SELECT name, location
    FROM hospitals
    ORDER BY fs.location <-> location  -- <-> is the distance operator
    LIMIT 1
) h;

-- Aggregate spatial data: dissolve polygons by attribute
SELECT state_name,
    ST_Union(county_boundary) AS state_boundary,  -- merge all county polygons
    SUM(population) AS total_population
FROM counties
GROUP BY state_name;

-- Spatial join with area calculation
SELECT p.name AS parcel_name,
    z.zone_type,
    ST_Area(ST_Intersection(p.boundary, z.boundary)::geography) AS overlap_area_sqm
FROM parcels p
JOIN zoning_areas z ON ST_Intersects(p.boundary, z.boundary);
```

---

## Coordinate Reference Systems

Understanding and transforming between coordinate systems.

```sql
-- SRID (Spatial Reference Identifier) defines the coordinate system
-- EPSG:4326 (WGS84) is the most common: longitude/latitude in degrees
-- Used by GPS, most web mapping, GeoJSON

-- Check the SRID of a geometry
SELECT ST_SRID(location) FROM cities LIMIT 1;
-- Returns: 4326

-- Set the SRID on a geometry (declares, does not transform)
SELECT ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326);

-- ST_Transform: convert between coordinate systems
-- Transform from WGS84 (4326) to UTM Zone 10N (32610) for accurate measurements
SELECT name,
    ST_Transform(location, 32610) AS location_utm,  -- project to UTM
    ST_X(ST_Transform(location, 32610)) AS easting,
    ST_Y(ST_Transform(location, 32610)) AS northing
FROM cities
WHERE name = 'San Francisco';

-- Common coordinate systems:
-- EPSG:4326  - WGS84 (lat/lon degrees) - GPS, global mapping
-- EPSG:3857  - Web Mercator (meters) - Google Maps, OpenStreetMap tiles
-- EPSG:32610 - UTM Zone 10N (meters) - western US (accurate measurements)
-- EPSG:2163  - US National Atlas (meters) - equal area for US
-- EPSG:27700 - British National Grid (meters) - UK mapping

-- Calculate area accurately by transforming to an equal-area projection
SELECT name,
    ST_Area(boundary) AS area_degrees,                     -- meaningless number
    ST_Area(boundary::geography) AS area_sqm_geography,    -- accurate via geography
    ST_Area(ST_Transform(boundary, 2163)) AS area_sqm_utm  -- accurate via projection
FROM states
WHERE name = 'California';

-- Find what SRID to use for a given location
SELECT srid, proj4text
FROM spatial_ref_sys
WHERE proj4text LIKE '%utm%zone=10%'
LIMIT 5;
```

---

## Spatial Indexing

Spatial indexes dramatically speed up spatial queries.

```sql
-- GiST index: the standard spatial index for PostGIS
-- Uses bounding box approximations for fast filtering
CREATE INDEX idx_cities_location ON cities USING GIST (location);
CREATE INDEX idx_parks_boundary ON parks USING GIST (boundary);
CREATE INDEX idx_roads_geom ON roads USING GIST (geom);

-- GiST indexes support these operators:
-- && : bounding box overlap (used internally by ST_Intersects, etc.)
-- <-> : distance ordering (used with ORDER BY for nearest neighbor)
-- @  : bounding box containment

-- BRIN index: for large, naturally ordered datasets
-- Much smaller than GiST, good when data is spatially clustered
CREATE INDEX idx_parcels_boundary_brin ON parcels USING BRIN (boundary);

-- Verify that your queries use the spatial index
EXPLAIN ANALYZE
SELECT name FROM cities
WHERE ST_DWithin(
    location::geography,
    ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326)::geography,
    1000
);
-- Look for "Index Scan using idx_cities_location" in the output

-- Index on geography columns
CREATE INDEX idx_airports_location ON airports USING GIST (location);
-- Geography columns use GiST indexes the same way

-- Rebuild indexes after large data loads
REINDEX INDEX idx_cities_location;

-- Analyze table statistics for the query planner
ANALYZE cities;

-- K-nearest neighbor (KNN) query using the index
-- The <-> operator uses the GiST index for efficient sorting
SELECT name,
    location <-> ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326) AS distance
FROM cities
ORDER BY location <-> ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326)
LIMIT 10;
```

---

## Measurement Functions

Functions for calculating distances, areas, and lengths.

```sql
-- ST_Distance: distance between two geometries
-- With geography type, returns meters
SELECT ST_Distance(
    'SRID=4326;POINT(-122.4194 37.7749)'::geography,  -- San Francisco
    'SRID=4326;POINT(-73.9857 40.7484)'::geography     -- New York
) / 1000 AS distance_km;
-- Returns: ~4129 km

-- ST_Area: area of a polygon
-- Geography returns square meters, geometry returns square units of CRS
SELECT name,
    ST_Area(boundary::geography) AS area_sqm,
    ST_Area(boundary::geography) / 1000000 AS area_sqkm,
    ST_Area(boundary::geography) * 0.000247105 AS area_acres
FROM parks;

-- ST_Length: length of a linestring
SELECT name,
    ST_Length(route::geography) / 1000 AS length_km
FROM trails
ORDER BY length_km DESC;

-- ST_Perimeter: perimeter of a polygon
SELECT name,
    ST_Perimeter(boundary::geography) / 1000 AS perimeter_km
FROM lakes;

-- ST_Azimuth: bearing from one point to another (in radians)
SELECT degrees(ST_Azimuth(
    ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326),  -- from: SF
    ST_SetSRID(ST_MakePoint(-73.9857, 40.7484), 4326)    -- to: NYC
)) AS bearing_degrees;
-- Returns: ~66 degrees (roughly ENE)

-- Centroid and bounding box
SELECT name,
    ST_AsText(ST_Centroid(boundary)) AS centroid,        -- center point
    ST_AsText(ST_Envelope(boundary)) AS bounding_box,    -- bounding rectangle
    ST_XMin(boundary) AS min_lon,
    ST_YMin(boundary) AS min_lat,
    ST_XMax(boundary) AS max_lon,
    ST_YMax(boundary) AS max_lat
FROM parks;

-- Number of points in a geometry
SELECT name, ST_NPoints(boundary) AS num_vertices
FROM countries
ORDER BY num_vertices DESC
LIMIT 10;
```

---

## Geometry Operations

Functions that create new geometries from existing ones.

```sql
-- ST_Buffer: create a buffer zone around a geometry
-- Buffer a point by 1000 meters (must use geography or projected CRS)
SELECT name,
    ST_Buffer(location::geography, 1000)::geometry AS buffer_1km
FROM fire_stations;

-- Buffer a road by 50 meters for a noise impact zone
SELECT name,
    ST_Buffer(
        ST_Transform(route, 32610),  -- transform to UTM for meters
        50                           -- 50 meter buffer
    ) AS noise_zone
FROM highways;

-- ST_Union: merge multiple geometries into one
-- Combine all county polygons into state boundaries
SELECT state_name,
    ST_Union(county_geom) AS state_geom
FROM counties
GROUP BY state_name;

-- Union of two specific geometries
SELECT ST_Union(
    ST_GeomFromText('POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))', 4326),
    ST_GeomFromText('POLYGON((1 1, 3 1, 3 3, 1 3, 1 1))', 4326)
) AS merged;

-- ST_Intersection: get the overlapping area of two geometries
SELECT
    a.name AS zone_a,
    b.name AS zone_b,
    ST_Intersection(a.boundary, b.boundary) AS overlap_area,
    ST_Area(ST_Intersection(a.boundary, b.boundary)::geography) AS overlap_sqm
FROM flood_zones a, building_zones b
WHERE ST_Intersects(a.boundary, b.boundary);

-- ST_Difference: subtract one geometry from another
-- "What part of the park is NOT in the flood zone?"
SELECT p.name,
    ST_Difference(p.boundary, f.boundary) AS safe_area
FROM parks p, flood_zones f
WHERE ST_Intersects(p.boundary, f.boundary);

-- ST_ConvexHull: smallest convex polygon containing all points
SELECT ST_ConvexHull(ST_Collect(location)) AS hull
FROM observation_points
WHERE survey_id = 42;

-- ST_SimplifyPreserveTopology: reduce vertex count for display
SELECT name,
    ST_NPoints(boundary) AS original_vertices,
    ST_NPoints(ST_SimplifyPreserveTopology(boundary, 0.001)) AS simplified_vertices,
    ST_SimplifyPreserveTopology(boundary, 0.001) AS simplified_geom
FROM countries;

-- ST_VoronoiPolygons: create Voronoi diagram from points
SELECT ST_VoronoiPolygons(ST_Collect(location)) AS voronoi
FROM weather_stations;

-- ST_Subdivide: split large polygons into smaller pieces (for indexing)
SELECT name, ST_Subdivide(boundary, 256) AS sub_polygon  -- max 256 vertices per piece
FROM large_regions;
```

---

## Importing and Exporting

Tools for getting data in and out of PostGIS.

```bash
# shp2pgsql: import shapefiles into PostGIS
# -s: specify SRID
# -I: create spatial index
# -D: use dump format (faster for large files)
shp2pgsql -s 4326 -I -D neighborhoods.shp public.neighborhoods | psql -d mydb

# Import with encoding specification
shp2pgsql -s 4326 -W "UTF-8" data.shp public.data | psql -d mydb

# ogr2ogr: versatile spatial data converter (GDAL/OGR)
# Import GeoJSON into PostGIS
ogr2ogr -f "PostgreSQL" PG:"host=localhost dbname=mydb user=postgres" \
    data.geojson -nln my_table -lco GEOMETRY_NAME=geom

# Import shapefile with reprojection
ogr2ogr -f "PostgreSQL" PG:"host=localhost dbname=mydb" \
    buildings.shp -t_srs EPSG:4326 -nln buildings

# Import GeoPackage
ogr2ogr -f "PostgreSQL" PG:"host=localhost dbname=mydb" \
    data.gpkg -nln my_layer

# Export PostGIS table to GeoJSON
ogr2ogr -f "GeoJSON" output.geojson \
    PG:"host=localhost dbname=mydb" -sql "SELECT * FROM cities"

# Export to shapefile
ogr2ogr -f "ESRI Shapefile" output_dir/ \
    PG:"host=localhost dbname=mydb" -sql "SELECT * FROM parks"

# Export to GeoPackage
ogr2ogr -f "GPKG" output.gpkg \
    PG:"host=localhost dbname=mydb" cities parks  # multiple tables
```

Exporting as GeoJSON directly from SQL:

```sql
-- Convert a single geometry to GeoJSON
SELECT ST_AsGeoJSON(location) FROM cities WHERE name = 'San Francisco';
-- Returns: {"type":"Point","coordinates":[-122.4194,37.7749]}

-- Build a full GeoJSON FeatureCollection from a table
SELECT json_build_object(
    'type', 'FeatureCollection',
    'features', json_agg(
        json_build_object(
            'type', 'Feature',
            'geometry', ST_AsGeoJSON(location)::json,
            'properties', json_build_object(
                'name', name,
                'population', population
            )
        )
    )
) AS geojson
FROM cities;

-- Export other formats
SELECT ST_AsText(location) AS wkt FROM cities;          -- WKT
SELECT ST_AsKML(location) AS kml FROM cities;           -- KML
SELECT ST_AsSVG(location) AS svg FROM cities;           -- SVG path
SELECT ST_AsGML(location) AS gml FROM cities;           -- GML
SELECT encode(ST_AsBinary(location), 'hex') FROM cities; -- WKB hex
```

---

## Python Integration

Using PostGIS with Python through psycopg2 and Shapely.

```python
# Basic PostGIS queries with psycopg2
import psycopg2
import json

# Connect to the PostGIS database
conn = psycopg2.connect(
    host="localhost",
    dbname="mydb",
    user="postgres",
    password="password"
)
cur = conn.cursor()

# Query points as GeoJSON
cur.execute("""
    SELECT name, population, ST_AsGeoJSON(location) AS geojson
    FROM cities
    WHERE population > 500000
    ORDER BY population DESC
""")

for row in cur.fetchall():
    name, population, geojson = row
    coords = json.loads(geojson)["coordinates"]
    print(f"{name}: pop={population}, lon={coords[0]}, lat={coords[1]}")
```

```python
# Using Shapely for geometry manipulation in Python
from shapely.geometry import Point, Polygon, mapping, shape
from shapely import wkt, wkb
import psycopg2

conn = psycopg2.connect(dbname="mydb", user="postgres")
cur = conn.cursor()

# Create geometries with Shapely and insert into PostGIS
point = Point(-122.4194, 37.7749)
polygon = Polygon([
    (-122.43, 37.77), (-122.41, 37.77),
    (-122.41, 37.79), (-122.43, 37.79),
    (-122.43, 37.77)
])

# Insert using WKT
cur.execute(
    "INSERT INTO cities (name, location) VALUES (%s, ST_GeomFromText(%s, 4326))",
    ("Test City", point.wkt)  # Shapely .wkt property generates WKT
)

# Insert using GeoJSON
cur.execute(
    "INSERT INTO parks (name, boundary) VALUES (%s, ST_GeomFromGeoJSON(%s))",
    ("Test Park", json.dumps(mapping(polygon)))  # mapping() converts to GeoJSON dict
)
conn.commit()
```

```python
# Spatial queries from Python
import psycopg2
from shapely.geometry import shape
import json

conn = psycopg2.connect(dbname="mydb", user="postgres")
cur = conn.cursor()

# Find nearest neighbors from Python
search_point = (-122.4194, 37.7749)  # San Francisco
radius_meters = 5000  # 5km

cur.execute("""
    SELECT name, population,
           ST_AsGeoJSON(location) AS geojson,
           ST_Distance(location::geography,
                       ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography) AS dist_m
    FROM cities
    WHERE ST_DWithin(
        location::geography,
        ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography,
        %s
    )
    ORDER BY dist_m
""", (search_point[0], search_point[1],
      search_point[0], search_point[1],
      radius_meters))

for row in cur.fetchall():
    name, pop, geojson, distance = row
    geom = shape(json.loads(geojson))  # convert GeoJSON to Shapely geometry
    print(f"{name} ({pop:,}): {distance:.0f}m away at {geom.x:.4f}, {geom.y:.4f}")

cur.close()
conn.close()
```

```python
# Using SQLAlchemy with GeoAlchemy2 for ORM-based access
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape, from_shape
from shapely.geometry import Point

Base = declarative_base()

class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    population = Column(Integer)
    location = Column(Geometry("POINT", srid=4326))  # GeoAlchemy2 type

engine = create_engine("postgresql://postgres:password@localhost/mydb")

with Session(engine) as session:
    # Insert a city
    new_city = City(
        name="Portland",
        population=652503,
        location=from_shape(Point(-122.6765, 45.5152), srid=4326)
    )
    session.add(new_city)
    session.commit()

    # Query cities and convert to Shapely geometries
    cities = session.query(City).all()
    for city in cities:
        point = to_shape(city.location)  # convert to Shapely Point
        print(f"{city.name}: ({point.x}, {point.y})")
```

---

## Practice Exercises

1. **Create a spatial database**: Set up a PostGIS database with tables for cities (points), roads (linestrings), and neighborhoods (polygons). Insert at least 5 records in each table.

2. **Spatial queries**: Write queries to find (a) all cities within a neighborhood, (b) all roads that intersect a neighborhood, (c) the 3 nearest cities to a given point.

3. **Distance calculations**: Calculate the distance in kilometers between every pair of cities in your table. Use geography type for accurate results.

4. **Buffer analysis**: Create 1km buffer zones around each city point and find which neighborhoods overlap with these buffers.

5. **Spatial joins**: Join cities to neighborhoods based on containment. Then count the number of cities per neighborhood.

6. **Import/Export**: Import a GeoJSON file using ogr2ogr, query the data with spatial functions, and export the results as a new GeoJSON file.

7. **Python integration**: Write a Python script that connects to your PostGIS database, performs a nearest-neighbor query, and displays the results using Shapely.

---

## Summary

PostGIS extends PostgreSQL into a powerful spatial database. Key takeaways:

- **Data types**: geometry for fast planar operations, geography for accurate spheroidal calculations in meters
- **Common types**: Point, LineString, Polygon, and their Multi- variants
- **Spatial queries**: ST_Contains, ST_Intersects, ST_Within, ST_DWithin for relationship testing
- **Distance and area**: use geography type or project to an appropriate CRS for real-world units
- **Spatial indexing**: GiST indexes are essential for performance; always create them on geometry columns
- **Geometry operations**: ST_Buffer, ST_Union, ST_Intersection, ST_Difference for spatial analysis
- **CRS management**: ST_Transform converts between coordinate systems; EPSG:4326 is the standard for lat/lon
- **Import/Export**: shp2pgsql and ogr2ogr handle common formats; ST_AsGeoJSON exports from SQL
- **Python**: psycopg2 + Shapely or GeoAlchemy2 for programmatic access

---

## Next Steps

- Learn GeoPandas for Python-based spatial analysis that complements PostGIS
- Explore raster data handling with PostGIS Raster
- Study spatial indexing strategies for large datasets
- Build a web mapping application using PostGIS as the backend
- Learn about spatial topology for data quality enforcement
- Investigate pg_tileserv and pg_featureserv for serving spatial data via APIs

---

## Additional Resources

- [PostGIS Official Documentation](https://postgis.net/documentation/)
- [PostGIS Reference](https://postgis.net/docs/reference.html)
- [Introduction to PostGIS Workshop](https://postgis.net/workshops/postgis-intro/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [GeoAlchemy2 Documentation](https://geoalchemy-2.readthedocs.io/)
- [Shapely Documentation](https://shapely.readthedocs.io/)
- [EPSG Registry](https://epsg.io/)
- [OGR2OGR Documentation](https://gdal.org/programs/ogr2ogr.html)
