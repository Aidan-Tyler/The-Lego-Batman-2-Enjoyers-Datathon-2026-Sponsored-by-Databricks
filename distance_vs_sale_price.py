import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 1. Load your new dataset (the one with the distances)
df = pd.read_csv('/Users/aidantyler/Desktop/Datathon2026/The-Lego-Batman-2-Enjoyers-Datathon-2026-Sponsored-by-Databricks/nyc_housing_with_distances.csv')

# 2. Setup the figure (Two charts side-by-side)
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# --- Chart 1: Taco Bell (Purple) ---
# Check your CSV column names! I am assuming the price column is named 'rent' or 'price'.
# If it's different (e.g., 'monthly_rent'), change y='rent' below.
sns.regplot(x='dist_to_tacobell', y='sale_price', data=df, ax=axes[0], 
            color='#6A0DAD', line_kws={"color": "black"}, scatter_kws={'alpha': 0.3})
axes[0].set_title('Does Taco Bell Affect Rent?')
axes[0].set_xlabel('Miles to Nearest Taco Bell')
axes[0].set_ylabel('Rent Price ($)')

# --- Chart 2: Chipotle (Dark Red) ---
sns.regplot(x='dist_to_chipotle', y='sale_price', data=df, ax=axes[1], 
            color='#A81612', line_kws={"color": "black"}, scatter_kws={'alpha': 0.3})
axes[1].set_title('Does Chipotle Affect Rent?')
axes[1].set_xlabel('Miles to Nearest Chipotle')
axes[1].set_ylabel('Rent Price ($)')

# 3. Show the plot
plt.tight_layout()
plt.show()