import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Load Data
df = pd.read_csv('/Users/aidantyler/Desktop/Datathon2026/The-Lego-Batman-2-Enjoyers-Datathon-2026-Sponsored-by-Databricks/nyc_housing_with_distances.csv')

# 2. Filter for clean data (remove outliers)
df = df[(df['sale_price'] < 5000000) & (df['sale_price'] > 10000)]

# 3. Create "Zones" using pd.cut
# We cut the distance into 4 buckets: <0.2 miles, 0.2-0.5, 0.5-1, and 1+ miles
bins = [0, 0.2, 0.5, 1.0, 100]
labels = ['Next Door (<0.2m)', 'Walkable (0.2-0.5m)', 'Driveable (0.5-1m)', 'Far (>1m)']
df['Taco_Zone'] = pd.cut(df['dist_to_tacobell'], bins=bins, labels=labels)

# 4. Calculate Average Price per Zone
zone_stats = df.groupby('Taco_Zone')['sale_price'].mean().reset_index()

# 5. Plot the Bar Chart
plt.figure(figsize=(10, 6))
sns.barplot(x='Taco_Zone', y='sale_price', data=zone_stats, palette='Purples_r')

plt.title('Average Housing Price by Taco Bell Proximity')
plt.ylabel('Average Price ($)')
plt.xlabel('Distance Zone')
plt.show()