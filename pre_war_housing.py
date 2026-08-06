import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load Data
df = pd.read_csv('nyc_housing_base.csv')

# 2. Filter Data (Remove tiny/free buildings and extreme outliers)
df = df[(df['sale_price'] > 100000) & (df['bldgarea'] > 200)]
df = df[df['yearbuilt'] > 1850] # Focus on the last ~170 years

# 3. Create "Decade" Column (e.g., 1923 -> 1920)
df['decade'] = (df['yearbuilt'] // 10) * 10

# 4. Calculate Price Per Square Foot (The great equalizer!)
df['price_per_sqft'] = df['sale_price'] / df['bldgarea']

# 5. Group by Borough and Decade
# We use 'median' because averages can be skewed by one billion-dollar penthouse
timeline = df.groupby(['borough_y', 'decade'])['price_per_sqft'].median().reset_index()

# 6. Plot the "Vintage Value Curve"
plt.figure(figsize=(14, 7))
sns.lineplot(data=timeline, x='decade', y='price_per_sqft', hue='borough_y', 
             linewidth=3, marker='o', palette='bright')

plt.title('The "Vintage Value" Curve: Price per SqFt by Decade Built', fontsize=16)
plt.xlabel('Decade Built', fontsize=12)
plt.ylabel('Median Price per Sq Ft ($)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title='Borough')
plt.show()