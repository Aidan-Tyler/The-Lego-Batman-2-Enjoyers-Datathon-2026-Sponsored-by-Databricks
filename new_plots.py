import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv('/Users/aidantyler/Desktop/Datathon2026/The-Lego-Batman-2-Enjoyers-Datathon-2026-Sponsored-by-Databricks/nyc_housing_with_distances.csv')

df = df[(df['sale_price'] < 5000000) & (df['sale_price'] > 10000)]
df = df[df['bldgarea'] > 100] # Remove placeholders with 0 size

# Calculate Price Per SqFt
df['price_per_sqft'] = df['sale_price'] / df['bldgarea']

plt.figure(figsize=(12, 6))
sns.scatterplot(
    data=df, 
    x='dist_to_bell', 
    y='sale_price', 
    hue='borough_y',  
    alpha=0.4,
    palette='bright'
)
plt.title('Taco Bell Proximity vs. Price (Colored by Borough)')
plt.xlabel('Miles to Taco Bell')
plt.ylabel('Price ($)')
plt.legend(title='Borough')
plt.show()

plt.figure(figsize=(12, 6))
sns.regplot(
    data=df,
    x='dist_to_tacobell',
    y='price_per_sqft',
    scatter_kws={'alpha':0.3, 'color':'purple'},
    line_kws={'color':'black'}
)
plt.title('Does Taco Bell Proximity Affect Price per SqFt?')
plt.xlabel('Miles to Taco Bell')
plt.ylabel('Price per Square Foot ($)')
plt.show()