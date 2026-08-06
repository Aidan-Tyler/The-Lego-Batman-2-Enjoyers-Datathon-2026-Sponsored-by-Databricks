import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree

# ---------------------------------------------------------
# 1. SETUP: Load the data
# ---------------------------------------------------------
housing_df = pd.read_csv('/Users/aidantyler/Desktop/Datathon2026/The-Lego-Batman-2-Enjoyers-Datathon-2026-Sponsored-by-Databricks/nyc_housing_base.csv')
restaurants_df = pd.read_csv('/Users/aidantyler/Desktop/Datathon2026/The-Lego-Batman-2-Enjoyers-Datathon-2026-Sponsored-by-Databricks/TacoBell vs Chipotle2.csv')

# ---------------------------------------------------------
# 2. PREPARATION (Do this once for the housing data)
# ---------------------------------------------------------
# Clean housing data
housing_df = housing_df.dropna(subset=['latitude', 'longitude'])

# Convert housing coordinates to radians (needed for the math)
housing_rad = np.deg2rad(housing_df[['latitude', 'longitude']].values)

# ---------------------------------------------------------
# 3. THE CALCULATION FUNCTION
# ---------------------------------------------------------
def get_nearest_distance(target_name, source_df, housing_radians):
    """
    Filters the restaurant list for a specific name (e.g., 'Taco Bell'),
    builds a tree, and calculates distance to the nearest one.
    """
    # A. Filter: Get only the rows for this specific restaurant
    # (Make sure 'Restaurant' matches the actual column name in your CSV!)
    subset_df = source_df[source_df['Restaurant'] == target_name].copy()
    
    # B. Clean: Remove rows with missing coordinates
    subset_df = subset_df.dropna(subset=['Zip Lat', 'Zip Lon'])
    
    # C. Convert to Radians
    subset_rad = np.deg2rad(subset_df[['Zip Lat', 'Zip Lon']].values)
    
    # D. Build Tree & Query
    tree = BallTree(subset_rad, metric='haversine')
    distances, _ = tree.query(housing_radians, k=1)
    
    # E. Return miles (Earth radius ~3963.2 miles)
    return distances * 3963.2

# ---------------------------------------------------------
# 4. RUN IT
# ---------------------------------------------------------

# Create the Taco Bell column
# Check your CSV: Is it "Taco Bell" or "taco bell"? Case matters!
housing_df['dist_to_tacobell'] = get_nearest_distance('Taco Bell', restaurants_df, housing_rad)

# Create the Chipotle column
housing_df['dist_to_chipotle'] = get_nearest_distance('Chipotle', restaurants_df, housing_rad)

# ---------------------------------------------------------
# 5. VIEW RESULTS
# ---------------------------------------------------------
output_filename = '/Users/aidantyler/Desktop/Datathon2026/The-Lego-Batman-2-Enjoyers-Datathon-2026-Sponsored-by-Databricks/nyc_housing_with_distances.csv'

# index=False prevents it from creating a weird extra column of row numbers
housing_df.to_csv(output_filename, index=False)
print(housing_df)