import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

# Load percentage data (e.g. access to basic water services)
percentage_data = pd.read_csv("data/raw/who_WSH_WATER_BASIC.csv")

# Only keep necessary columns
columns_to_keep = [
    'SpatialDimType', 'SpatialDim', 'ParentLocationCode', 'Dim1', 'TimeDimensionValue', 'NumericValue'
]

percentage_data = percentage_data[
    (percentage_data['TimeDimensionValue'] >= 2010) &
    (percentage_data['TimeDimensionValue'] <= 2019)
]

percentage_clean = percentage_data[columns_to_keep]

# Filter for country-level data
percentage_country = percentage_clean[percentage_clean['SpatialDimType'] == 'COUNTRY']

# Optional: focus on a few countries for clarity
countries_to_plot = ['BLZ', 'AUS', 'SLV', 'JOR', 'MEX', 'TUR', 'DOM']
percentage_plot = percentage_country[percentage_country['SpatialDim'].isin(countries_to_plot)]

# Print only values for Belize (BLZ) in 2013
print(percentage_plot[(percentage_plot['SpatialDim'] == 'BLZ') & (percentage_plot['TimeDimensionValue'] == 2013)])

# Use only total population values
percentage_total = percentage_country[percentage_country['Dim1'] == 'RESIDENCEAREATYPE_TOTL']

# Pivot for year-wise time series per country
percentage_pivot = percentage_total.pivot_table(
    index='SpatialDim',
    columns='TimeDimensionValue',
    values='NumericValue'
)

# Visualize missing values
plt.figure(figsize=(12, 8))
sns.heatmap(percentage_pivot.isnull(), cbar=False, cmap="magma")
plt.title("Missing Data by Country and Year")
plt.xlabel("Year")
plt.ylabel("Country")
plt.tight_layout()
plt.show()

# Interpolate missing values across years
percentage_pivot = percentage_pivot.interpolate(axis=1, limit_direction='both')

# Scale using Min-Max (0–1), since it's percentage data
scaler = MinMaxScaler()
percentage_scaled = scaler.fit_transform(percentage_pivot)

# Convert back to DataFrame
percentage_scaled_df = pd.DataFrame(
    percentage_scaled, 
    index=percentage_pivot.index, 
    columns=percentage_pivot.columns
)

# Save both versions for future use
percentage_pivot.to_csv("data/clean/water_percentage_unscaled.csv")
percentage_scaled_df.to_csv("data/clean/water_percentage_scaled.csv")
