import pandas as pd
import geopandas as gpd
from shapely import wkt
import folium
from folium.plugins import MarkerCluster

# ---------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------
# Load your housing and restaurant data
housing_df = pd.read_csv('nyc_housing_with_distances.csv')
restaurants_df = pd.read_csv('TacoBell vs Chipotle2.csv')

# Load the NEW Borough Boundaries CSV you downloaded
borough_df = pd.read_csv('Borough_Boundaries_20260207.csv')

# ---------------------------------------------------------
# 2. PROCESS THE BOROUGH SHAPES
# ---------------------------------------------------------
# The CSV has a text column 'the_geom' that looks like "MULTIPOLYGON..."
# We convert this text into actual geometry objects for the map.
borough_df['geometry'] = borough_df['the_geom'].apply(wkt.loads)

# Convert to a GeoDataFrame (a special dataframe for maps)
borough_gdf = gpd.GeoDataFrame(borough_df, geometry='geometry')

# Set the coordinate system to WGS84 (Standard Latitude/Longitude)
borough_gdf.set_crs(epsg=4326, inplace=True)

# ---------------------------------------------------------
# 3. SETUP THE MAP & COLORS
# ---------------------------------------------------------
# Define colors for each borough
borough_colors = {
    'Manhattan': '#1f77b4',     # Blue
    'Bronx': '#d62728',         # Red
    'Brooklyn': '#ff7f0e',      # Orange
    'Queens': '#2ca02c',        # Green
    'Staten Island': '#9467bd'  # Purple
}

nyc_map = folium.Map(location=[40.7128, -74.0060], zoom_start=11, tiles='CartoDB positron')

# ---------------------------------------------------------
# 4. ADD LAYERS
# ---------------------------------------------------------

# LAYER 1: The Borough Polygons
folium.GeoJson(
    borough_gdf,
    name="Borough Boundaries",
    style_function=lambda feature: {
        # Note: The column name in your CSV is 'BoroName' (Capitalized)
        'fillColor': borough_colors.get(feature['properties']['BoroName'], 'gray'),
        'color': 'black',       # Border color
        'weight': 2,            # Border thickness
        'fillOpacity': 0.4      # Transparency
    },
    tooltip=folium.GeoJsonTooltip(fields=['BoroName'], aliases=['Borough:'])
).add_to(nyc_map)

# LAYER 2: Housing Clusters
housing_cluster = MarkerCluster(name="Housing Listings").add_to(nyc_map)

# Add housing points (Limiting to 2000 for speed)
for index, row in housing_df.head(34440).iterrows():
    try:
        price_text = "${:,.0f}".format(row['sale_price'])
    except:
        price_text = "N/A"
        
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=5,
        popup=f"Price: {price_text}",
        color="white",
        weight=1,
        fill=True,
        fill_color="#333",
        fill_opacity=0.7
    ).add_to(housing_cluster)

# LAYER 3: Taco Bells (Purple Pins)
taco_bells = restaurants_df[restaurants_df['Restaurant'] == 'Taco Bell']
for index, row in taco_bells.iterrows():
    folium.Marker(
        location=[row['Zip Lat'], row['Zip Lon']],
        popup=row['Restaurant'],
        tooltip="Taco Bell",
        icon=folium.Icon(color='purple', icon='bell', prefix='fa')
    ).add_to(nyc_map)

# LAYER 4: Chipotles (Red Pins)
chipotles = restaurants_df[restaurants_df['Restaurant'] == 'Chipotle']
for index, row in chipotles.iterrows():
    folium.Marker(
        location=[row['Zip Lat'], row['Zip Lon']],
        popup=row['Restaurant'],
        tooltip="Chipotle",
        icon=folium.Icon(color='red', icon='fire', prefix='fa')
    ).add_to(nyc_map)

# ---------------------------------------------------------
# 5. SAVE
# ---------------------------------------------------------
folium.LayerControl().add_to(nyc_map)
nyc_map.save("nyc_borough_map_final.html")
print("Success! Map saved as 'nyc_borough_map_final.html'")