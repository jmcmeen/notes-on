# Introduction to pyinaturalist

## Table of Contents

- [What is pyinaturalist](#what-is-pyinaturalist)
- [Installation](#installation)
- [Authentication](#authentication)
- [Searching Observations](#searching-observations)
- [Observation Details](#observation-details)
- [Searching Taxa](#searching-taxa)
- [Searching Places](#searching-places)
- [Creating and Updating Observations](#creating-and-updating-observations)
- [Working with Photos](#working-with-photos)
- [Pagination and Rate Limiting](#pagination-and-rate-limiting)
- [Data Analysis with Pandas](#data-analysis-with-pandas)
- [Integration with GeoPandas](#integration-with-geopandas)
- [Species Lists and Biodiversity Analysis](#species-lists-and-biodiversity-analysis)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is pyinaturalist

pyinaturalist is a Python client for the iNaturalist API. iNaturalist is a citizen science platform where users upload observations of organisms (plants, animals, fungi) with photos and location data. The API provides access to millions of biodiversity observations worldwide.

Key capabilities:

- Search and filter observations by species, location, date, and quality
- Access taxonomic information (species hierarchy, common names)
- Create, update, and manage your own observations
- Download photos and observation metadata
- Perform biodiversity analysis with rich spatial and temporal data

```python
from pyinaturalist import get_observations

# Fetch recent research-grade bird observations in California
response = get_observations(
    taxon_name="Aves",           # birds
    place_id=14,                  # California
    quality_grade="research",     # community-verified observations
    per_page=5                    # limit results
)

# Each observation includes species, location, photos, and more
for obs in response["results"]:
    taxon = obs["taxon"]
    print(f"{taxon['preferred_common_name']} ({taxon['name']})")
    print(f"  Location: {obs['place_guess']}")
    print(f"  Date: {obs['observed_on']}")
    print()
```

---

## Installation

```python
# Install pyinaturalist
# pip install pyinaturalist

# Install with optional dependencies for data analysis
# pip install pyinaturalist pandas geopandas folium

# Verify installation
import pyinaturalist
print(pyinaturalist.__version__)

# pyinaturalist features:
# - Type-annotated API wrapper for all iNaturalist endpoints
# - Built-in request caching to reduce API calls
# - Rate limiting to respect iNaturalist API guidelines
# - Response formatting and Pydantic model support
```

---

## Authentication

Authentication is required for creating/modifying observations. Read-only access (searching) works without authentication.

```python
from pyinaturalist import get_access_token

# Step 1: Register an application at https://www.inaturalist.org/oauth/applications
# You'll receive: app_id and app_secret

# Step 2: Get an access token using your credentials
token = get_access_token(
    username="your_inaturalist_username",
    password="your_password",
    app_id="your_app_id",
    app_secret="your_app_secret"
)
print(f"Token: {token[:20]}...")  # keep this secret

# Use environment variables for credentials (recommended)
import os

# Set these in your environment or .env file:
# export INAT_USERNAME="your_username"
# export INAT_PASSWORD="your_password"
# export INAT_APP_ID="your_app_id"
# export INAT_APP_SECRET="your_app_secret"

token = get_access_token(
    username=os.environ.get("INAT_USERNAME"),
    password=os.environ.get("INAT_PASSWORD"),
    app_id=os.environ.get("INAT_APP_ID"),
    app_secret=os.environ.get("INAT_APP_SECRET")
)

# The token is passed to write operations
# Read operations (get_observations, get_taxa) do NOT require authentication
```

---

## Searching Observations

The core function for retrieving observation data from iNaturalist.

```python
from pyinaturalist import get_observations

# Basic search: all observations of a species
response = get_observations(
    taxon_name="Danaus plexippus",  # monarch butterfly (scientific name)
    per_page=10
)
print(f"Total results: {response['total_results']}")

# Search by common name
response = get_observations(
    taxon_name="Monarch Butterfly",
    per_page=10
)

# Search by taxon ID (faster than name lookup)
response = get_observations(
    taxon_id=48662,       # monarch butterfly taxon ID
    per_page=10
)

# Filter by location (place ID or bounding box)
response = get_observations(
    taxon_name="Aves",          # birds
    place_id=14,                 # California (iNat place ID)
    per_page=20
)

# Filter by bounding box (nelat, nelng, swlat, swlng)
response = get_observations(
    taxon_name="Aves",
    nelat=38.0, nelng=-122.0,    # northeast corner
    swlat=37.5, swlng=-122.5,   # southwest corner
    per_page=20
)

# Filter by geographic coordinates and radius
response = get_observations(
    taxon_name="Plantae",       # plants
    lat=37.7749,                 # center latitude
    lng=-122.4194,               # center longitude
    radius=10,                   # radius in kilometers
    per_page=20
)

# Filter by date range
response = get_observations(
    taxon_name="Fungi",
    d1="2025-01-01",             # start date (YYYY-MM-DD)
    d2="2025-03-31",             # end date
    per_page=20
)

# Filter by observation date fields
response = get_observations(
    taxon_name="Mammalia",
    year=2025,                   # specific year
    month=6,                     # specific month
    per_page=20
)

# Filter by quality grade
response = get_observations(
    taxon_name="Reptilia",
    quality_grade="research",    # "research", "needs_id", or "casual"
    per_page=20
)
# research: community-verified species ID
# needs_id: awaiting community verification
# casual: missing location, date, or media

# Filter by observation characteristics
response = get_observations(
    taxon_name="Aves",
    has=["photos", "geo"],       # must have photos and geolocation
    introduced=False,            # only native species
    threatened=True,             # only threatened species
    per_page=20
)

# Filter by user
response = get_observations(
    user_login="username123",    # specific user's observations
    per_page=20
)

# Combine multiple filters
response = get_observations(
    taxon_name="Amphibia",       # amphibians
    place_id=14,                  # California
    quality_grade="research",
    d1="2024-01-01",
    d2="2024-12-31",
    has=["photos", "geo"],
    order_by="observed_on",      # sort by observation date
    order="desc",                # newest first
    per_page=50
)
```

---

## Observation Details

Understanding the structure of observation data.

```python
from pyinaturalist import get_observations, get_observation

# Get a single observation by ID
obs = get_observation(12345678)  # returns a single observation dict

# Get observations with full details
response = get_observations(
    taxon_name="Strix occidentalis",  # spotted owl
    quality_grade="research",
    per_page=5
)

for obs in response["results"]:
    # Basic observation info
    print(f"ID: {obs['id']}")
    print(f"Observed on: {obs['observed_on']}")
    print(f"Created at: {obs['created_at']}")
    print(f"Place guess: {obs['place_guess']}")
    print(f"Quality: {obs['quality_grade']}")

    # Location data
    if obs.get("geojson"):
        coords = obs["geojson"]["coordinates"]  # [longitude, latitude]
        print(f"Coordinates: {coords[1]}, {coords[0]}")  # lat, lon
    print(f"Positional accuracy: {obs.get('positional_accuracy')} meters")
    print(f"Obscured: {obs.get('obscured')}")  # True if location obscured for privacy

    # Taxon (species) information
    taxon = obs.get("taxon", {})
    print(f"Species: {taxon.get('name')}")
    print(f"Common name: {taxon.get('preferred_common_name')}")
    print(f"Rank: {taxon.get('rank')}")
    print(f"Iconic taxon: {taxon.get('iconic_taxon_name')}")

    # Photos
    photos = obs.get("photos", [])
    print(f"Number of photos: {len(photos)}")
    for photo in photos:
        print(f"  Photo URL: {photo['url']}")
        # URL sizes: square, small, medium, large, original
        # Replace "square" in URL to get different sizes
        large_url = photo["url"].replace("square", "large")
        print(f"  Large URL: {large_url}")

    # Identifications (community IDs)
    identifications = obs.get("identifications", [])
    print(f"Number of IDs: {len(identifications)}")
    for ident in identifications:
        user = ident.get("user", {})
        taxon = ident.get("taxon", {})
        print(f"  {user.get('login')}: {taxon.get('name')} (agree: {ident.get('current')})")

    # Annotations (life stage, sex, etc.)
    annotations = obs.get("annotations", [])
    for ann in annotations:
        attr = ann.get("controlled_attribute", {})
        val = ann.get("controlled_value", {})
        print(f"  {attr.get('label')}: {val.get('label')}")

    print("---")
```

---

## Searching Taxa

Look up taxonomic information including species hierarchy.

```python
from pyinaturalist import get_taxa

# Search by name
response = get_taxa(q="monarch butterfly")
for taxon in response["results"]:
    print(f"{taxon['name']} ({taxon.get('preferred_common_name', 'N/A')})")
    print(f"  Rank: {taxon['rank']}")
    print(f"  ID: {taxon['id']}")
    print(f"  Observations: {taxon.get('observations_count', 0)}")

# Search by scientific name
response = get_taxa(q="Quercus", rank="genus")  # oak genus

# Get taxonomy hierarchy (ancestors)
response = get_taxa(taxon_id=48662)  # monarch butterfly
taxon = response["results"][0]

# Ancestors show the full taxonomic hierarchy
ancestors = taxon.get("ancestors", [])
for ancestor in ancestors:
    print(f"  {ancestor['rank']}: {ancestor['name']}")
# Output:
#   kingdom: Animalia
#   phylum: Arthropoda
#   class: Insecta
#   order: Lepidoptera
#   family: Nymphalidae
#   genus: Danaus

# Get children of a taxon (subtaxa)
response = get_taxa(parent_id=47126)  # children of Passeriformes (songbirds)
for taxon in response["results"][:10]:
    print(f"{taxon['rank']}: {taxon['name']} ({taxon.get('preferred_common_name', '')})")

# Filter by rank
response = get_taxa(
    q="oak",
    rank="species",          # only species-level results
    is_active=True           # only currently accepted names
)

# Autocomplete search (fast, for search boxes)
from pyinaturalist import get_taxa_autocomplete

results = get_taxa_autocomplete(q="red-tailed")
for taxon in results["results"]:
    print(f"{taxon['matched_term']}: {taxon['name']}")
```

---

## Searching Places

Look up iNaturalist place identifiers for location-based queries.

```python
from pyinaturalist import get_places_autocomplete, get_places_nearby

# Search for places by name
response = get_places_autocomplete(q="Yosemite")
for place in response["results"]:
    print(f"ID: {place['id']} | {place['display_name']}")
    print(f"  Type: {place.get('place_type_name')}")
    print(f"  Bounding box: {place.get('bounding_box_geojson', {}).get('coordinates')}")

# Common place IDs (useful for filtering observations):
# 1     - United States
# 14    - California
# 6903  - Yosemite National Park
# 7161  - San Francisco
# 97394 - Europe

# Search for places near coordinates
response = get_places_nearby(
    nelat=37.8, nelng=-122.3,    # northeast corner
    swlat=37.7, swlng=-122.5     # southwest corner
)

# Results include standard places (political) and community places
for place_type in ["standard", "community"]:
    places = response["results"].get(place_type, [])
    for place in places[:5]:
        print(f"[{place_type}] {place['display_name']} (ID: {place['id']})")
```

---

## Creating and Updating Observations

Submit and manage observations (requires authentication).

```python
from pyinaturalist import create_observation, update_observation, delete_observation

# Create a new observation
response = create_observation(
    taxon_id=48662,                     # monarch butterfly
    observed_on_string="2025-03-15",    # date observed
    latitude=37.7749,                    # location
    longitude=-122.4194,
    positional_accuracy=10,              # accuracy in meters
    description="Spotted on a milkweed plant in the garden.",
    tag_list=["garden", "migration"],    # tags for organization
    access_token=token                   # authentication token
)
observation_id = response[0]["id"]
print(f"Created observation: {observation_id}")

# Update an existing observation
update_observation(
    observation_id,
    description="Updated: Adult monarch spotted on milkweed. Wings intact.",
    access_token=token
)

# Delete an observation
delete_observation(observation_id, access_token=token)

# Add a photo to an observation
from pyinaturalist import add_photo_to_observation

add_photo_to_observation(
    observation_id,
    photo="path/to/butterfly_photo.jpg",  # local file path
    access_token=token
)
```

---

## Working with Photos

Access and download observation photos.

```python
from pyinaturalist import get_observations
import requests
import os

# Get observations with photos
response = get_observations(
    taxon_name="Calypte anna",     # Anna's hummingbird
    quality_grade="research",
    has=["photos"],
    per_page=5
)

# Extract photo URLs
for obs in response["results"]:
    photos = obs.get("photos", [])
    for photo in photos:
        # iNaturalist provides multiple sizes via URL manipulation
        base_url = photo["url"]

        # Available sizes by replacing the size keyword in the URL:
        sizes = {
            "square": base_url,                                    # 75x75
            "small": base_url.replace("square", "small"),          # 240px
            "medium": base_url.replace("square", "medium"),        # 500px
            "large": base_url.replace("square", "large"),          # 1024px
            "original": base_url.replace("square", "original")     # full resolution
        }

        print(f"Observation {obs['id']}:")
        for size, url in sizes.items():
            print(f"  {size}: {url}")

# Download photos
def download_photo(url: str, output_path: str):
    """Download a photo from iNaturalist."""
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded: {output_path}")

# Download medium-resolution photos
os.makedirs("photos", exist_ok=True)
for obs in response["results"]:
    for i, photo in enumerate(obs.get("photos", [])):
        url = photo["url"].replace("square", "medium")
        filename = f"photos/obs_{obs['id']}_photo_{i}.jpg"
        download_photo(url, filename)
```

---

## Pagination and Rate Limiting

Handle large result sets and respect API limits.

```python
from pyinaturalist import get_observations
import time

# iNaturalist API limits:
# - Max 200 results per page (per_page)
# - Max 10,000 results total per query
# - Rate limit: ~1 request per second recommended

# Basic pagination
def get_all_observations(per_page=200, max_results=1000, **kwargs):
    """Fetch multiple pages of observations."""
    all_results = []
    page = 1

    while len(all_results) < max_results:
        response = get_observations(
            per_page=per_page,
            page=page,
            **kwargs
        )

        results = response["results"]
        if not results:
            break  # no more results

        all_results.extend(results)
        total = response["total_results"]
        print(f"Page {page}: got {len(results)} results ({len(all_results)}/{total})")

        if len(all_results) >= total:
            break  # fetched everything

        page += 1
        time.sleep(1)  # respect rate limits

    return all_results[:max_results]  # trim to max

# Usage: get up to 500 research-grade bird observations in California
observations = get_all_observations(
    taxon_name="Aves",
    place_id=14,
    quality_grade="research",
    max_results=500
)
print(f"Total fetched: {len(observations)}")

# For very large queries (>10,000 results), use ID-based pagination
def get_observations_by_id(max_results=50000, **kwargs):
    """Use id_below pagination for large result sets."""
    all_results = []
    id_below = None  # start from the most recent

    while len(all_results) < max_results:
        params = {**kwargs, "per_page": 200, "order": "desc", "order_by": "id"}
        if id_below:
            params["id_below"] = id_below

        response = get_observations(**params)
        results = response["results"]

        if not results:
            break

        all_results.extend(results)
        id_below = results[-1]["id"]  # set cursor to last ID
        print(f"Fetched {len(all_results)} observations (last ID: {id_below})")

        time.sleep(1)  # rate limiting

    return all_results[:max_results]

# pyinaturalist has built-in caching to avoid redundant API calls
# Responses are cached locally and reused for identical requests
```

---

## Data Analysis with Pandas

Convert iNaturalist data to Pandas DataFrames for analysis.

```python
import pandas as pd
from pyinaturalist import get_observations

# Fetch observations
response = get_observations(
    taxon_name="Aves",
    place_id=14,              # California
    quality_grade="research",
    per_page=200
)

# Convert to DataFrame
def observations_to_dataframe(observations: list) -> pd.DataFrame:
    """Convert iNaturalist observations to a Pandas DataFrame."""
    records = []
    for obs in observations:
        taxon = obs.get("taxon", {})
        record = {
            "id": obs["id"],
            "observed_on": obs.get("observed_on"),
            "created_at": obs.get("created_at"),
            "species": taxon.get("name"),
            "common_name": taxon.get("preferred_common_name"),
            "taxon_id": taxon.get("id"),
            "iconic_taxon": taxon.get("iconic_taxon_name"),
            "rank": taxon.get("rank"),
            "latitude": obs.get("geojson", {}).get("coordinates", [None, None])[1],
            "longitude": obs.get("geojson", {}).get("coordinates", [None, None])[0],
            "place_guess": obs.get("place_guess"),
            "quality_grade": obs.get("quality_grade"),
            "num_identification_agreements": obs.get("num_identification_agreements"),
            "num_photos": len(obs.get("photos", [])),
            "user_login": obs.get("user", {}).get("login"),
            "positional_accuracy": obs.get("positional_accuracy"),
            "obscured": obs.get("obscured"),
        }
        records.append(record)

    df = pd.DataFrame(records)
    df["observed_on"] = pd.to_datetime(df["observed_on"])
    return df

df = observations_to_dataframe(response["results"])
print(df.shape)
print(df.head())

# Basic analysis
print("\n--- Species Summary ---")
print(f"Total observations: {len(df)}")
print(f"Unique species: {df['species'].nunique()}")
print(f"Date range: {df['observed_on'].min()} to {df['observed_on'].max()}")

# Most observed species
print("\nTop 10 species:")
print(df["common_name"].value_counts().head(10))

# Observations by month
df["month"] = df["observed_on"].dt.month
monthly = df.groupby("month").size()
print("\nObservations by month:")
print(monthly)

# Top observers
print("\nTop observers:")
print(df["user_login"].value_counts().head(5))

# Observation quality
print("\nQuality distribution:")
print(df["quality_grade"].value_counts())
```

---

## Integration with GeoPandas

Map iNaturalist observations using GeoPandas and Folium.

```python
import geopandas as gpd
import pandas as pd
import folium
from shapely.geometry import Point
from pyinaturalist import get_observations

# Fetch observations
response = get_observations(
    taxon_name="Calypte anna",     # Anna's hummingbird
    place_id=14,                    # California
    quality_grade="research",
    has=["geo"],                    # must have coordinates
    per_page=200
)

# Convert to GeoDataFrame
def observations_to_geodataframe(observations: list) -> gpd.GeoDataFrame:
    """Convert iNaturalist observations to a GeoDataFrame."""
    records = []
    geometries = []

    for obs in observations:
        coords = obs.get("geojson", {}).get("coordinates")
        if not coords or obs.get("obscured"):
            continue  # skip observations without precise coordinates

        taxon = obs.get("taxon", {})
        records.append({
            "id": obs["id"],
            "observed_on": obs.get("observed_on"),
            "species": taxon.get("name"),
            "common_name": taxon.get("preferred_common_name"),
            "place_guess": obs.get("place_guess"),
            "user": obs.get("user", {}).get("login"),
        })
        geometries.append(Point(coords[0], coords[1]))  # (lon, lat)

    gdf = gpd.GeoDataFrame(records, geometry=geometries, crs="EPSG:4326")
    gdf["observed_on"] = pd.to_datetime(gdf["observed_on"])
    return gdf

gdf = observations_to_geodataframe(response["results"])
print(f"Observations with coordinates: {len(gdf)}")
print(gdf.head())

# Plot observations on a static map
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 8))
gdf.plot(ax=ax, color="red", markersize=10, alpha=0.6)
ax.set_title("Anna's Hummingbird Observations in California")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
plt.show()

# Create an interactive Folium map
center_lat = gdf.geometry.y.mean()
center_lon = gdf.geometry.x.mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=7)

for _, row in gdf.iterrows():
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=4,
        color="red",
        fill=True,
        fill_opacity=0.7,
        popup=f"""
            <b>{row['common_name']}</b><br>
            {row['species']}<br>
            {row['observed_on']}<br>
            {row['place_guess']}<br>
            Observer: {row['user']}
        """,
        tooltip=row["common_name"]
    ).add_to(m)

m.save("hummingbird_map.html")

# Spatial analysis: observations per county
counties = gpd.read_file("data/ca_counties.geojson")
obs_per_county = gpd.sjoin(gdf, counties, predicate="within")
county_counts = obs_per_county.groupby("county_name").size().reset_index(name="obs_count")
print("\nObservations per county:")
print(county_counts.sort_values("obs_count", ascending=False).head(10))
```

---

## Species Lists and Biodiversity Analysis

Analyze biodiversity patterns from iNaturalist data.

```python
import pandas as pd
from pyinaturalist import get_observations
from collections import Counter

def get_species_list(place_id: int, taxon_name: str = None,
                     max_results: int = 1000) -> pd.DataFrame:
    """Build a species list for a location from iNaturalist observations."""
    import time

    all_observations = []
    page = 1

    while len(all_observations) < max_results:
        params = {
            "place_id": place_id,
            "quality_grade": "research",
            "per_page": 200,
            "page": page,
            "has": ["geo"],
        }
        if taxon_name:
            params["taxon_name"] = taxon_name

        response = get_observations(**params)
        results = response["results"]
        if not results:
            break

        all_observations.extend(results)
        page += 1
        time.sleep(1)  # rate limit

    # Build species list with counts
    species_counts = Counter()
    species_info = {}

    for obs in all_observations:
        taxon = obs.get("taxon", {})
        if taxon.get("rank") != "species":
            continue  # only count species-level IDs

        species_name = taxon.get("name")
        species_counts[species_name] += 1

        if species_name not in species_info:
            species_info[species_name] = {
                "scientific_name": species_name,
                "common_name": taxon.get("preferred_common_name", ""),
                "taxon_id": taxon.get("id"),
                "iconic_taxon": taxon.get("iconic_taxon_name", ""),
            }

    # Combine into DataFrame
    records = []
    for species, count in species_counts.most_common():
        info = species_info[species]
        info["observation_count"] = count
        records.append(info)

    return pd.DataFrame(records)

# Generate a bird species list for Yosemite
species_df = get_species_list(place_id=6903, taxon_name="Aves", max_results=2000)
print(f"Bird species observed: {len(species_df)}")
print(species_df.head(15))

# Biodiversity metrics
print(f"\nSpecies richness: {len(species_df)}")
print(f"Total observations: {species_df['observation_count'].sum()}")
print(f"Most common: {species_df.iloc[0]['common_name']} ({species_df.iloc[0]['observation_count']} obs)")

# Seasonal analysis
def seasonal_species_analysis(place_id: int, taxon_name: str):
    """Analyze which species appear in each season."""
    import time

    seasonal_species = {"spring": set(), "summer": set(), "fall": set(), "winter": set()}
    season_map = {3: "spring", 4: "spring", 5: "spring",
                  6: "summer", 7: "summer", 8: "summer",
                  9: "fall", 10: "fall", 11: "fall",
                  12: "winter", 1: "winter", 2: "winter"}

    for month in range(1, 13):
        response = get_observations(
            place_id=place_id,
            taxon_name=taxon_name,
            quality_grade="research",
            month=month,
            per_page=200
        )

        season = season_map[month]
        for obs in response["results"]:
            taxon = obs.get("taxon", {})
            if taxon.get("rank") == "species":
                species = taxon.get("preferred_common_name", taxon.get("name"))
                seasonal_species[season].add(species)

        time.sleep(1)

    # Analyze seasonal patterns
    for season, species in seasonal_species.items():
        print(f"\n{season.capitalize()}: {len(species)} species")

    # Species unique to each season
    all_species = set.union(*seasonal_species.values())
    for season, species in seasonal_species.items():
        unique = species - set.union(*(s for s_name, s in seasonal_species.items()
                                        if s_name != season))
        if unique:
            print(f"\nUnique to {season}: {', '.join(list(unique)[:5])}")

    return seasonal_species
```

---

## Practice Exercises

1. **Basic search**: Search for observations of a species in your area. Print the species name, date, location, and number of photos for each result.

2. **Species inventory**: Build a species list for a park or region using research-grade observations. Calculate species richness and identify the 10 most commonly observed species.

3. **Temporal analysis**: Fetch a year's worth of observations for a migratory species. Plot the number of observations by month to visualize migration patterns using Pandas.

4. **Spatial mapping**: Fetch observations of a species, convert to a GeoDataFrame, and create a Folium map with markers colored by observation month.

5. **Biodiversity comparison**: Compare species richness between two different locations (parks, counties, etc.) for the same taxonomic group. Identify species unique to each location.

6. **Photo gallery**: Fetch observations with photos for a taxon. Download the medium-resolution photos and organize them in folders by species name.

7. **Multi-taxon analysis**: Fetch observations for birds, mammals, and reptiles in a region. Create a summary table and a stacked bar chart showing observation counts by month and taxonomic group.

---

## Summary

pyinaturalist provides Python access to the iNaturalist biodiversity database. Key takeaways:

- **Searching**: get_observations with filters for taxon, location, date, quality grade, and more
- **Taxa**: get_taxa for taxonomic lookups, hierarchy, and common names
- **Places**: search for iNaturalist place IDs to use in observation queries
- **Authentication**: required only for creating/updating observations; reading is public
- **Pagination**: use page-based or ID-based pagination for large result sets; respect rate limits
- **Pandas**: convert observations to DataFrames for statistical analysis
- **GeoPandas**: create GeoDataFrames for spatial analysis and mapping
- **Folium**: build interactive maps of observation locations
- **Biodiversity**: generate species lists, calculate richness, analyze seasonal patterns

---

## Next Steps

- Build a local biodiversity dashboard combining pyinaturalist, GeoPandas, and Folium
- Explore the iNaturalist export tool for bulk data downloads
- Integrate with eBird API for complementary bird observation data
- Study GBIF (Global Biodiversity Information Facility) for broader biodiversity data
- Use scikit-learn with observation data for species distribution modeling
- Contribute observations to iNaturalist to support citizen science

---

## Additional Resources

- [pyinaturalist Documentation](https://pyinaturalist.readthedocs.io/)
- [iNaturalist API Documentation](https://api.inaturalist.org/v1/docs/)
- [iNaturalist Website](https://www.inaturalist.org/)
- [iNaturalist API Reference](https://www.inaturalist.org/pages/api+reference)
- [GBIF (Global Biodiversity Information Facility)](https://www.gbif.org/)
- [GeoPandas Documentation](https://geopandas.org/)
- [Folium Documentation](https://python-visualization.github.io/folium/)
