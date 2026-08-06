import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load your housing data
df = pd.read_csv('nyc_housing_base.csv')

# 2. Calculate Average Price per Borough
# We group by 'borough_y' (MN, BK, BX, QN, SI)
avg_price = df.groupby('borough_y')['sale_price'].mean().reset_index()
avg_price.columns = ['Borough', 'Avg_Price']

# 3. Add Taco Bell Counts (Sourced from public location data)
# Note: If your Taco Bell CSV has a 'Borough' column, you could groupby/count that instead.
taco_counts = {
    'MN': 27,  # Manhattan (New York, NY addresses)
    'BX': 17,  # Bronx
    'BK': 16,  # Brooklyn
    'QN': 18,  # Queens (Sum of neighborhoods)
    'SI': 6    # Staten Island
}

# Convert counts to a DataFrame
taco_df = pd.DataFrame(list(taco_counts.items()), columns=['Borough', 'Taco_Count'])

# 4. Merge the data
merged_df = pd.merge(avg_price, taco_df, on='Borough')

# 5. Plotting (Dual Axis Chart)
fig, ax1 = plt.subplots(figsize=(10, 6))

# Bar Plot for Price (Left Axis)
sns.barplot(x='Borough', y='Avg_Price', data=merged_df, ax=ax1, color='skyblue', alpha=0.6)
ax1.set_ylabel('Average Home Price ($)', color='blue', fontsize=12)
ax1.tick_params(axis='y', labelcolor='blue')

# Line Plot for Taco Bell Count (Right Axis)
ax2 = ax1.twinx()
sns.lineplot(x='Borough', y='Taco_Count', data=merged_df, ax=ax2, color='red', marker='o', linewidth=3)
ax2.set_ylabel('Number of Taco Bells', color='red', fontsize=12)
ax2.tick_params(axis='y', labelcolor='red')

plt.title('Do Taco Bells Correlate with Home Prices?', fontsize=14)
plt.show()