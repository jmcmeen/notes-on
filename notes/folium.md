# Introduction to Folium

## Table of Contents

- [What is Folium](#what-is-folium)
- [Installation](#installation)
- [Creating Maps](#creating-maps)
- [Markers](#markers)
- [Multiple Markers](#multiple-markers)
- [GeoJSON](#geojson)
- [Choropleth Maps](#choropleth-maps)
- [Circle and CircleMarker](#circle-and-circlemarker)
- [Polylines and Polygons](#polylines-and-polygons)
- [Layer Control](#layer-control)
- [Heatmaps](#heatmaps)
- [Drawing Tools](#drawing-tools)
- [Saving Maps](#saving-maps)
- [Integration with GeoPandas](#integration-with-geopandas)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is Folium

Folium is a Python library that creates interactive web maps using Leaflet.js. It lets you build rich, interactive maps entirely in Python and export them as standalone HTML files that can be viewed in any web browser.

Key features:

- Build interactive maps with pan, zoom, and click interactions
- Add markers, popups, tooltips, and custom icons
- Create choropleth maps with data-driven coloring
- Overlay GeoJSON data with custom styling
- Add heatmaps, marker clusters, and drawing tools
- Export as self-contained HTML files
- Integrates naturally with GeoPandas and Pandas

```python
import folium

# Create a simple interactive map in 3 lines
m = folium.Map(location=[37.7749, -122.4194], zoom_start=12)
folium.Marker([37.7749, -122.4194], popup="San Francisco").add_to(m)
m.save("map.html")  # open in any browser
```

---

## Installation

```python
# Install folium
# pip install folium

# Optional dependencies for additional features
# pip install geopandas      # spatial data integration
# pip install branca          # HTML/CSS rendering (installed with folium)

# Verify installation
import folium
print(folium.__version__)
```

---

## Creating Maps

The Map object is the foundation of every Folium visualization.

```python
import folium

# Basic map with location and zoom
m = folium.Map(
    location=[37.7749, -122.4194],  # [latitude, longitude] center point
    zoom_start=12                    # initial zoom level (1=world, 18=street)
)

# Map with different tile providers
# OpenStreetMap (default)
m = folium.Map(location=[37.7749, -122.4194], tiles="OpenStreetMap")

# CartoDB Positron (clean, light theme - good for data visualization)
m = folium.Map(location=[37.7749, -122.4194], tiles="CartoDB positron")

# CartoDB Dark Matter (dark theme)
m = folium.Map(location=[37.7749, -122.4194], tiles="CartoDB dark_matter")

# Esri satellite imagery
m = folium.Map(
    location=[37.7749, -122.4194],
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri"
)

# Map dimensions and control options
m = folium.Map(
    location=[37.7749, -122.4194],
    zoom_start=13,
    width="100%",             # map width (pixels or percentage)
    height="600px",           # map height
    min_zoom=5,               # minimum zoom level allowed
    max_zoom=18,              # maximum zoom level allowed
    control_scale=True,       # show scale bar
    zoom_control=True,        # show zoom +/- buttons
    prefer_canvas=True        # use canvas renderer (faster for many features)
)

# Fit map bounds to show a specific area
m = folium.Map()
m.fit_bounds([
    [37.70, -122.52],   # southwest corner [lat, lon]
    [37.82, -122.35]    # northeast corner [lat, lon]
])
```

---

## Markers

Add interactive markers to the map with popups and tooltips.

```python
import folium

m = folium.Map(location=[37.7749, -122.4194], zoom_start=13)

# Basic marker with popup and tooltip
folium.Marker(
    location=[37.7749, -122.4194],       # [lat, lon]
    popup="San Francisco City Center",    # shown on click
    tooltip="Click for details"           # shown on hover
).add_to(m)

# Marker with HTML popup content
html_popup = """
<div style="width: 200px;">
    <h4>Golden Gate Bridge</h4>
    <p>Opened: May 27, 1937</p>
    <p>Length: 2,737 meters</p>
    <img src="https://example.com/ggb.jpg" width="180">
</div>
"""
folium.Marker(
    location=[37.8199, -122.4783],
    popup=folium.Popup(html_popup, max_width=250),
    tooltip="Golden Gate Bridge"
).add_to(m)

# Marker with colored icon
folium.Marker(
    location=[37.7695, -122.4667],
    popup="Golden Gate Park",
    icon=folium.Icon(
        color="green",          # marker color: red, blue, green, purple, orange, etc.
        icon="tree-deciduous",  # Bootstrap glyphicon name
        prefix="glyphicon"      # icon set: "glyphicon" (default) or "fa" (Font Awesome)
    )
).add_to(m)

# Font Awesome icons (more variety)
folium.Marker(
    location=[37.7850, -122.4094],
    popup="Restaurant",
    icon=folium.Icon(
        color="red",
        icon="utensils",     # Font Awesome icon name
        prefix="fa"          # use Font Awesome
    )
).add_to(m)

# Custom icon from an image URL
custom_icon = folium.CustomIcon(
    icon_image="https://example.com/marker.png",
    icon_size=(30, 30),          # (width, height) in pixels
    icon_anchor=(15, 30),        # anchor point (center-bottom)
    popup_anchor=(0, -30)        # popup position relative to anchor
)
folium.Marker(
    location=[37.7600, -122.4350],
    popup="Custom Icon",
    icon=custom_icon
).add_to(m)

# DivIcon: custom HTML as marker icon
folium.Marker(
    location=[37.7900, -122.4000],
    icon=folium.DivIcon(
        html='<div style="font-size: 20px; color: red;">&#x2605;</div>',  # star emoji
        icon_size=(30, 30),
        icon_anchor=(15, 15)
    )
).add_to(m)
```

---

## Multiple Markers

Efficiently add many markers with clustering and grouping.

```python
import folium
from folium.plugins import MarkerCluster

m = folium.Map(location=[37.7749, -122.4194], zoom_start=12)

# Sample data: list of locations
locations = [
    {"name": "Place A", "lat": 37.7849, "lon": -122.4094, "type": "restaurant"},
    {"name": "Place B", "lat": 37.7750, "lon": -122.4180, "type": "cafe"},
    {"name": "Place C", "lat": 37.7650, "lon": -122.4280, "type": "bar"},
    {"name": "Place D", "lat": 37.7710, "lon": -122.4130, "type": "restaurant"},
    {"name": "Place E", "lat": 37.7800, "lon": -122.4050, "type": "cafe"},
]

# MarkerCluster: groups nearby markers at low zoom levels
# Essential for maps with hundreds or thousands of markers
marker_cluster = MarkerCluster(name="Restaurants & Cafes").add_to(m)

for loc in locations:
    folium.Marker(
        location=[loc["lat"], loc["lon"]],
        popup=f"{loc['name']} ({loc['type']})",
        tooltip=loc["name"],
        icon=folium.Icon(
            color="red" if loc["type"] == "restaurant" else "blue",
            icon="info-sign"
        )
    ).add_to(marker_cluster)  # add to cluster, not directly to map

# FeatureGroup: logical grouping of markers (for layer control)
restaurants = folium.FeatureGroup(name="Restaurants")
cafes = folium.FeatureGroup(name="Cafes")

for loc in locations:
    marker = folium.Marker(
        location=[loc["lat"], loc["lon"]],
        popup=loc["name"],
        tooltip=loc["name"]
    )
    if loc["type"] == "restaurant":
        marker.add_to(restaurants)
    else:
        marker.add_to(cafes)

restaurants.add_to(m)
cafes.add_to(m)
folium.LayerControl().add_to(m)  # toggle groups on/off

# Fast marker addition from a DataFrame
import pandas as pd

df = pd.DataFrame(locations)

# Using FastMarkerCluster for very large datasets (thousands of points)
from folium.plugins import FastMarkerCluster

callback = """
function (row) {
    var marker = L.marker(new L.LatLng(row[0], row[1]));
    marker.bindPopup(row[2]);
    return marker;
}
"""
FastMarkerCluster(
    data=df[["lat", "lon", "name"]].values.tolist(),
    callback=callback
).add_to(m)
```

---

## GeoJSON

Add GeoJSON data layers with custom styling and interactivity.

```python
import folium
import json

m = folium.Map(location=[37.7749, -122.4194], zoom_start=12)

# Load GeoJSON from a file
with open("data/neighborhoods.geojson") as f:
    geojson_data = json.load(f)

# Add GeoJSON layer with default styling
folium.GeoJson(
    geojson_data,
    name="Neighborhoods"
).add_to(m)

# Add GeoJSON with custom styling
folium.GeoJson(
    geojson_data,
    name="Styled Neighborhoods",
    style_function=lambda feature: {
        "fillColor": "lightblue",     # fill color
        "color": "navy",              # border color
        "weight": 2,                  # border width
        "fillOpacity": 0.4,           # fill transparency (0-1)
        "dashArray": "5, 5"           # dashed border
    }
).add_to(m)

# Dynamic styling based on feature properties
def style_by_population(feature):
    """Color neighborhoods by population."""
    pop = feature["properties"].get("population", 0)
    if pop > 100000:
        color = "#d73027"    # red for high population
    elif pop > 50000:
        color = "#fee08b"    # yellow for medium
    else:
        color = "#1a9850"    # green for low
    return {
        "fillColor": color,
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.6
    }

folium.GeoJson(
    geojson_data,
    name="Population",
    style_function=style_by_population,
    tooltip=folium.GeoJsonTooltip(
        fields=["name", "population"],               # properties to show
        aliases=["Neighborhood:", "Population:"],     # display labels
        style="font-size: 14px; padding: 5px;"
    ),
    popup=folium.GeoJsonPopup(
        fields=["name", "population", "area_sqmi"],
        aliases=["Name", "Population", "Area (sq mi)"]
    )
).add_to(m)

# Highlight on hover
folium.GeoJson(
    geojson_data,
    name="Interactive",
    style_function=lambda f: {"fillColor": "#3186cc", "fillOpacity": 0.3},
    highlight_function=lambda f: {
        "fillColor": "#ffff00",   # yellow highlight on hover
        "fillOpacity": 0.7,
        "weight": 3
    },
    tooltip=folium.GeoJsonTooltip(fields=["name"])
).add_to(m)

# Load GeoJSON directly from a URL
folium.GeoJson(
    "https://example.com/data/boundaries.geojson",
    name="Remote GeoJSON"
).add_to(m)
```

---

## Choropleth Maps

Data-driven colored maps for visualizing statistics across regions.

```python
import folium
import pandas as pd

m = folium.Map(location=[37.7749, -122.4194], zoom_start=11)

# Data to visualize (DataFrame with region identifiers and values)
data = pd.DataFrame({
    "neighborhood": ["Mission", "Castro", "Richmond", "Sunset", "SoMa"],
    "median_income": [65000, 85000, 72000, 78000, 95000]
})

# Create choropleth map
folium.Choropleth(
    geo_data="data/neighborhoods.geojson",    # GeoJSON with region boundaries
    data=data,                                 # DataFrame with values
    columns=["neighborhood", "median_income"], # [key_column, value_column]
    key_on="feature.properties.name",          # GeoJSON property to match key_column
    fill_color="YlOrRd",                       # color scale
    fill_opacity=0.7,
    line_opacity=0.3,
    legend_name="Median Income ($)",
    nan_fill_color="gray",                     # color for regions with no data
    nan_fill_opacity=0.4
).add_to(m)

# Available color scales (from branca.colormap):
# Sequential: "YlGn", "YlOrRd", "BuGn", "BuPu", "GnBu", "OrRd", "PuBu",
#             "PuRd", "RdPu", "YlGnBu", "Blues", "Greens", "Reds", "Purples"
# Diverging: "BrBG", "PiYG", "PRGn", "RdBu", "RdYlBu", "RdYlGn", "Spectral"

# Choropleth with custom bins
folium.Choropleth(
    geo_data="data/neighborhoods.geojson",
    data=data,
    columns=["neighborhood", "median_income"],
    key_on="feature.properties.name",
    fill_color="Blues",
    bins=[0, 50000, 65000, 80000, 100000, 150000],  # custom breakpoints
    legend_name="Median Income ($)"
).add_to(m)

# Add tooltips to a choropleth (requires adding GeoJson separately)
import json

with open("data/neighborhoods.geojson") as f:
    geo_data = json.load(f)

# Merge data into GeoJSON properties for tooltips
income_map = dict(zip(data["neighborhood"], data["median_income"]))
for feature in geo_data["features"]:
    name = feature["properties"]["name"]
    feature["properties"]["median_income"] = income_map.get(name, "N/A")

# Add the choropleth
choropleth = folium.Choropleth(
    geo_data=geo_data,
    data=data,
    columns=["neighborhood", "median_income"],
    key_on="feature.properties.name",
    fill_color="YlGn",
    legend_name="Median Income"
).add_to(m)

# Add tooltips on top of the choropleth
folium.GeoJsonTooltip(
    fields=["name", "median_income"],
    aliases=["Neighborhood:", "Median Income:"]
).add_to(choropleth.geojson)
```

---

## Circle and CircleMarker

Circle-based map elements for proportional symbol maps.

```python
import folium

m = folium.Map(location=[37.7749, -122.4194], zoom_start=12)

# CircleMarker: radius in pixels (stays same size regardless of zoom)
folium.CircleMarker(
    location=[37.7749, -122.4194],
    radius=10,                  # radius in pixels
    color="blue",               # border color
    fill=True,
    fill_color="lightblue",
    fill_opacity=0.7,
    popup="San Francisco",
    tooltip="SF"
).add_to(m)

# Circle: radius in meters (scales with zoom)
folium.Circle(
    location=[37.7749, -122.4194],
    radius=1000,                # radius in meters
    color="red",
    fill=True,
    fill_color="red",
    fill_opacity=0.2,
    popup="1km radius around SF",
    tooltip="1km zone"
).add_to(m)

# Proportional symbol map: size circles by a data value
cities = [
    {"name": "San Francisco", "lat": 37.7749, "lon": -122.4194, "pop": 874961},
    {"name": "Oakland", "lat": 37.8044, "lon": -122.2712, "pop": 433031},
    {"name": "San Jose", "lat": 37.3382, "lon": -121.8863, "pop": 1013240},
    {"name": "Berkeley", "lat": 37.8715, "lon": -122.2730, "pop": 124321},
]

for city in cities:
    # Scale radius proportionally to population
    radius = (city["pop"] / 1000000) * 30  # scale factor for visibility

    folium.CircleMarker(
        location=[city["lat"], city["lon"]],
        radius=radius,
        color="darkblue",
        fill=True,
        fill_color="cornflowerblue",
        fill_opacity=0.6,
        popup=f"{city['name']}: {city['pop']:,}",
        tooltip=city["name"]
    ).add_to(m)
```

---

## Polylines and Polygons

Draw lines and shapes on the map.

```python
import folium

m = folium.Map(location=[37.7749, -122.4194], zoom_start=13)

# Polyline: a line connecting multiple points
route = [
    [37.7749, -122.4194],   # start point
    [37.7850, -122.4094],   # waypoint
    [37.7900, -122.3950],   # waypoint
    [37.7800, -122.3900]    # end point
]

folium.PolyLine(
    locations=route,
    color="blue",
    weight=4,              # line width in pixels
    opacity=0.8,
    dash_array="10",       # dashed line: "10" or "5, 10"
    popup="Walking Route",
    tooltip="Route A"
).add_to(m)

# Multiple colored segments (e.g., colored by speed or elevation)
segment1 = [[37.7749, -122.4194], [37.7850, -122.4094]]
segment2 = [[37.7850, -122.4094], [37.7900, -122.3950]]
segment3 = [[37.7900, -122.3950], [37.7800, -122.3900]]

folium.PolyLine(segment1, color="green", weight=5, tooltip="Fast").add_to(m)
folium.PolyLine(segment2, color="orange", weight=5, tooltip="Medium").add_to(m)
folium.PolyLine(segment3, color="red", weight=5, tooltip="Slow").add_to(m)

# Polygon: a closed shape
park_boundary = [
    [37.7700, -122.4600],
    [37.7700, -122.4500],
    [37.7800, -122.4500],
    [37.7800, -122.4600]
    # automatically closes back to the first point
]

folium.Polygon(
    locations=park_boundary,
    color="green",
    weight=2,
    fill=True,
    fill_color="lightgreen",
    fill_opacity=0.4,
    popup="Golden Gate Park",
    tooltip="Park"
).add_to(m)

# Rectangle: defined by opposite corners
folium.Rectangle(
    bounds=[[37.77, -122.45], [37.79, -122.41]],  # [[sw_lat, sw_lon], [ne_lat, ne_lon]]
    color="purple",
    fill=True,
    fill_color="purple",
    fill_opacity=0.2,
    popup="Study Area"
).add_to(m)
```

---

## Layer Control

Toggle layers on and off for interactive exploration.

```python
import folium

m = folium.Map(location=[37.7749, -122.4194], zoom_start=12)

# Create named feature groups (each becomes a toggleable layer)
parks_layer = folium.FeatureGroup(name="Parks", show=True)       # visible by default
schools_layer = folium.FeatureGroup(name="Schools", show=True)
transit_layer = folium.FeatureGroup(name="Transit", show=False)  # hidden by default

# Add markers to each layer
folium.Marker([37.7694, -122.4862], popup="Golden Gate Park",
              icon=folium.Icon(color="green")).add_to(parks_layer)
folium.Marker([37.7700, -122.4500], popup="Buena Vista Park",
              icon=folium.Icon(color="green")).add_to(parks_layer)

folium.Marker([37.7650, -122.4300], popup="Mission High School",
              icon=folium.Icon(color="blue")).add_to(schools_layer)
folium.Marker([37.7780, -122.4160], popup="Lowell High School",
              icon=folium.Icon(color="blue")).add_to(schools_layer)

folium.Marker([37.7850, -122.4094], popup="Montgomery Station",
              icon=folium.Icon(color="orange")).add_to(transit_layer)

# Add all layers to the map
parks_layer.add_to(m)
schools_layer.add_to(m)
transit_layer.add_to(m)

# Add layer control widget (appears in top-right corner)
folium.LayerControl(
    collapsed=False  # show expanded by default (True = collapsed)
).add_to(m)

# Multiple tile layers with control
m = folium.Map(location=[37.7749, -122.4194], zoom_start=12)
folium.TileLayer("OpenStreetMap", name="Street Map").add_to(m)
folium.TileLayer("CartoDB positron", name="Light Theme").add_to(m)
folium.TileLayer("CartoDB dark_matter", name="Dark Theme").add_to(m)
folium.LayerControl().add_to(m)
# Users can switch between base map styles
```

---

## Heatmaps

Visualize density patterns with heat maps.

```python
import folium
from folium.plugins import HeatMap

m = folium.Map(location=[37.7749, -122.4194], zoom_start=12)

# Heatmap data: list of [lat, lon] or [lat, lon, weight]
heat_data = [
    [37.7749, -122.4194],     # equal weight (default 1.0)
    [37.7750, -122.4180],
    [37.7748, -122.4200],
    [37.7800, -122.4094],
    [37.7690, -122.4350],
    [37.7700, -122.4300, 5],  # weighted point (5x intensity)
    [37.7850, -122.4000, 3],  # weighted point (3x intensity)
]

HeatMap(
    data=heat_data,
    min_opacity=0.3,       # minimum opacity
    max_zoom=15,           # zoom level where points appear as individual dots
    radius=15,             # radius of each point's influence in pixels
    blur=10,               # amount of blur
    gradient={             # custom color gradient
        0.2: "blue",
        0.4: "lime",
        0.6: "yellow",
        0.8: "orange",
        1.0: "red"
    }
).add_to(m)

# Heatmap from a DataFrame
import pandas as pd

df = pd.DataFrame({
    "lat": [37.77, 37.78, 37.76, 37.79, 37.77, 37.78, 37.75],
    "lon": [-122.42, -122.41, -122.43, -122.40, -122.41, -122.42, -122.44],
    "weight": [1, 2, 1, 3, 2, 1, 4]  # optional weights
})

# Create heat data from DataFrame
heat_data = df[["lat", "lon", "weight"]].values.tolist()
HeatMap(heat_data, radius=20).add_to(m)

# Time-based heatmap (animated)
from folium.plugins import HeatMapWithTime

# Data format: list of lists, one per time step
# Each time step is a list of [lat, lon, weight] points
time_data = [
    # Hour 0
    [[37.77, -122.42, 1], [37.78, -122.41, 2]],
    # Hour 1
    [[37.77, -122.42, 3], [37.78, -122.41, 1], [37.76, -122.43, 2]],
    # Hour 2
    [[37.78, -122.41, 4], [37.76, -122.43, 3]],
]

HeatMapWithTime(
    data=time_data,
    index=["00:00", "01:00", "02:00"],  # time labels
    auto_play=True,
    speed_step=1
).add_to(m)
```

---

## Drawing Tools

Let users draw shapes directly on the map.

```python
import folium
from folium.plugins import Draw

m = folium.Map(location=[37.7749, -122.4194], zoom_start=13)

# Add drawing toolbar
Draw(
    draw_options={
        "polyline": True,      # allow drawing lines
        "polygon": True,       # allow drawing polygons
        "rectangle": True,     # allow drawing rectangles
        "circle": True,        # allow drawing circles
        "marker": True,        # allow placing markers
        "circlemarker": False  # disable circle markers
    },
    edit_options={
        "edit": True,          # allow editing drawn shapes
        "remove": True         # allow deleting drawn shapes
    },
    export=True                # show export button for drawn shapes
).add_to(m)

# The export button lets users download their drawn shapes as GeoJSON

# MeasureControl: add distance/area measurement tool
from folium.plugins import MeasureControl

MeasureControl(
    primary_length_unit="meters",
    secondary_length_unit="kilometers",
    primary_area_unit="sqmeters",
    secondary_area_unit="hectares"
).add_to(m)

# LocateControl: add a "find my location" button
from folium.plugins import LocateControl

LocateControl(auto_start=False).add_to(m)

# Fullscreen control
from folium.plugins import Fullscreen

Fullscreen(
    position="topleft",
    title="Fullscreen",
    title_cancel="Exit Fullscreen"
).add_to(m)

# Minimap: small overview map in the corner
from folium.plugins import MiniMap

MiniMap(toggle_display=True).add_to(m)
```

---

## Saving Maps

Export maps as HTML files or display in notebooks.

```python
import folium

m = folium.Map(location=[37.7749, -122.4194], zoom_start=12)
folium.Marker([37.7749, -122.4194], popup="SF").add_to(m)

# Save as a standalone HTML file
m.save("output/my_map.html")
# The HTML file is self-contained and can be opened in any browser
# It includes all the JavaScript, CSS, and data inline

# Get the HTML as a string (for embedding in web applications)
html_string = m._repr_html_()
# or
html_string = m.get_root().render()

# Display in Jupyter Notebook (just output the map object)
# m  # displays inline in the notebook cell

# Save with custom page title
m.get_root().html.add_child(
    folium.Element("<title>My Custom Map</title>")
)
m.save("output/titled_map.html")

# Embedding in a Flask/Django web application
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")
def index():
    m = folium.Map(location=[37.7749, -122.4194], zoom_start=12)
    map_html = m._repr_html_()
    return render_template_string("""
    <html>
    <body>
        <h1>My Map Application</h1>
        {{ map_html | safe }}
    </body>
    </html>
    """, map_html=map_html)
```

---

## Integration with GeoPandas

Use GeoPandas GeoDataFrames as data sources for Folium maps.

```python
import geopandas as gpd
import folium
import json

# Load spatial data with GeoPandas
neighborhoods = gpd.read_file("data/neighborhoods.geojson")
restaurants = gpd.read_file("data/restaurants.geojson")

# Method 1: Use GeoDataFrame.explore() (simplest approach)
# explore() creates a Folium map directly from a GeoDataFrame
m = neighborhoods.explore(
    column="population",          # color by this column
    cmap="YlOrRd",                # color map
    legend=True,
    tooltip=["name", "population"],
    popup=True,                   # show all columns on click
    tiles="CartoDB positron",
    style_kwds={"weight": 1, "fillOpacity": 0.5},
    name="Neighborhoods"          # layer name for layer control
)

# Add a second GeoDataFrame to the same map
restaurants.explore(
    m=m,                          # existing map object
    color="red",
    marker_kwds={"radius": 5},
    tooltip=["name", "cuisine"],
    name="Restaurants"
)

# Add layer control
folium.LayerControl().add_to(m)
m.save("output/explore_map.html")

# Method 2: Manual construction with folium.GeoJson
m = folium.Map(location=[37.7749, -122.4194], zoom_start=12)

# GeoDataFrame can be passed directly to GeoJson
folium.GeoJson(
    neighborhoods,                 # pass GeoDataFrame directly
    name="Neighborhoods",
    style_function=lambda f: {
        "fillColor": "lightblue",
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.4
    },
    tooltip=folium.GeoJsonTooltip(fields=["name", "population"])
).add_to(m)

# Method 3: Choropleth from GeoDataFrame
m = folium.Map(location=[37.7749, -122.4194], zoom_start=12)

folium.Choropleth(
    geo_data=neighborhoods,               # GeoDataFrame as geo_data
    data=neighborhoods,                    # same or different DataFrame for values
    columns=["name", "median_income"],     # [key, value] columns
    key_on="feature.properties.name",      # match key in GeoJSON
    fill_color="YlGn",
    fill_opacity=0.7,
    legend_name="Median Income ($)"
).add_to(m)

# Add markers from a points GeoDataFrame
for _, row in restaurants.iterrows():
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],  # lat, lon from geometry
        radius=5,
        color="red",
        fill=True,
        popup=row["name"],
        tooltip=f"{row['name']} - {row['cuisine']}"
    ).add_to(m)

m.save("output/geopandas_map.html")
```

---

## Practice Exercises

1. **Basic map**: Create a Folium map centered on your city. Add 5 markers for notable locations with popups containing names and descriptions. Save as HTML.

2. **Marker clustering**: Create a map with at least 50 markers (generate random coordinates or use a real dataset). Use MarkerCluster to handle the density. Add tooltips.

3. **GeoJSON styling**: Load a GeoJSON file of neighborhoods/regions. Style polygons based on a property value using a custom style_function. Add tooltips and hover highlighting.

4. **Choropleth**: Create a choropleth map showing a statistic across regions (population, income, etc.). Add proper tooltips and a descriptive legend.

5. **Heatmap**: Create a heatmap from a dataset of point locations (crime data, taxi pickups, etc.). Experiment with radius, blur, and gradient parameters.

6. **Multi-layer map**: Build a map with at least 3 toggleable layers (e.g., parks, schools, transit stops). Use FeatureGroups and LayerControl. Include different tile layer options.

7. **GeoPandas integration**: Load two spatial datasets with GeoPandas (one polygon, one point). Create an interactive Folium map showing both layers with a choropleth for polygons and markers for points.

---

## Summary

Folium makes it easy to create interactive web maps from Python. Key takeaways:

- **Maps**: folium.Map with location, zoom, and tile provider options
- **Markers**: Marker, CircleMarker, and Circle with popups, tooltips, and custom icons
- **Clustering**: MarkerCluster handles large numbers of points efficiently
- **GeoJSON**: add polygon/line layers with custom styling and interactive tooltips
- **Choropleth**: data-driven coloring for statistical visualization across regions
- **Layers**: FeatureGroup and LayerControl for toggleable map layers
- **Heatmaps**: HeatMap plugin for density visualization
- **Drawing**: Draw plugin lets users create shapes interactively
- **Export**: save as standalone HTML files or embed in web applications
- **GeoPandas**: explore() method and GeoJson layer for seamless integration

---

## Next Steps

- Combine Folium with GeoPandas for spatial analysis and visualization workflows
- Explore additional Folium plugins (TimestampedGeoJson, AntPath, DualMap)
- Build web applications with Flask/Django that serve Folium maps dynamically
- Learn Leaflet.js for custom JavaScript extensions beyond Folium's built-in options
- Explore Plotly or Deck.gl for 3D and high-performance map visualizations

---

## Additional Resources

- [Folium Official Documentation](https://python-visualization.github.io/folium/)
- [Folium Plugins](https://python-visualization.github.io/folium/plugins.html)
- [Leaflet.js Documentation](https://leafletjs.com/)
- [GeoPandas explore() Guide](https://geopandas.org/en/stable/docs/user_guide/interactive_mapping.html)
- [Folium GitHub Examples](https://github.com/python-visualization/folium/tree/main/examples)
- [ColorBrewer (color scales)](https://colorbrewer2.org/)
