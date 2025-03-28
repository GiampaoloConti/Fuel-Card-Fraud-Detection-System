import requests
import pandas as pd

overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = """
[out:json];
area["ISO3166-1"="IT"][admin_level=2];
node["amenity"="fuel"](area);
out body;
"""

response = requests.get(overpass_url, params={'data': overpass_query})
data = response.json()

fuel_stations = []
for element in data['elements']:
    if element['type'] == 'node':
        fuel_stations.append({
            'id': element['id'],
            'latitude': element['lat'],
            'longitude': element['lon'],
            'name': element['tags'].get('name', 'Unknown')
        })

fuel_stations_df = pd.DataFrame(fuel_stations)

fuel_stations_df.to_csv('fuel_stations_italy.csv', index=False)

print(f"Retrieved {len(fuel_stations_df)} fuel stations in Italy.")

import geopandas as gpd
from geopandas import GeoDataFrame


# Create geometry column from longitude and latitude
geometry = gpd.points_from_xy(fuel_stations_df["longitude"], fuel_stations_df["latitude"], crs="EPSG:4326")
gdf = GeoDataFrame(fuel_stations_df, geometry=geometry)

gdf.explore()