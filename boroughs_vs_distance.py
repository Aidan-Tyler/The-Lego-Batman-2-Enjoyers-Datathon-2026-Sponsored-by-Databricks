import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 1. Load Data
# Make sure the path is correct!
df = pd.read_csv('/Users/aidantyler/Desktop/Datathon2026/The-Lego-Batman-2-Enjoyers-Datathon-2026-Sponsored-by-Databricks/nyc_housing_with_distances.csv')

# --- DATA PREP ---
#df = df[(df['sale_price'] < 5000000) & (df['sale_price'] > 10000)]
df = df[df['bldgarea'] > 100]
df['price_per_sqft'] = df['sale_price'] / df['bldgarea']

# --- CHART SET 1: Total Sale Price vs. Taco Bell Distance ---
# col='borough_y' creates the side-by-side columns
# col_wrap=3 means it will start a new row after 3 charts
print("Generating Price vs. Distance charts...")
sns.lmplot(
    data=df, 
    x='dist_to_tacobell',  # Ensure this matches your column name (e.g., dist_to_bell vs dist_to_tacobell)
    y='sale_price', 
    col='borough_y',       # <--- This splits it into individual graphs!
    hue='borough_y',       # Colors them differently too
    col_wrap=3,            # Keeps them from being one tiny wide row
    height=4,              # Height of each small graph
    aspect=1.2,            # Width of each small graph
    scatter_kws={'alpha':0.3, 's':10}, # Make dots smaller and see-through
    line_kws={'color': 'black'}
)
plt.subplots_adjust(top=0.9)
plt.suptitle('Trend: Sale Price vs. Distance to Taco Bell (By Borough)', fontsize=16)
plt.show()

# --- CHART SET 2: Price Per SqFt vs. Taco Bell Distance ---
# This is usually the more accurate metric
print("Generating Price/SqFt vs. Distance charts...")
sns.lmplot(
    data=df, 
    x='dist_to_tacobell', 
    y='price_per_sqft', 
    col='borough_y',       # <--- Splits by borough
    hue='borough_y',
    col_wrap=3,
    height=4, 
    aspect=1.2,
    scatter_kws={'alpha':0.3, 's':10},
    line_kws={'color': 'black'} # The trend line
)
plt.subplots_adjust(top=0.9)
plt.suptitle('Trend: Price Per SqFt vs. Distance to Taco Bell (By Borough)', fontsize=16)
plt.show()