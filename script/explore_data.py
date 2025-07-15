import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

file_path = os.path.join("..","data","population_data.csv")
df = pd.read_csv(file_path,skiprows=4)

print(df.describe())
print(df.info())
print(df.columns.tolist())
print(df.head())
print(df.isnull().sum())
print(df.dtypes)

df.drop("Unnamed: 69", axis=1, inplace=True)

print(df.shape)

print(df["Indicator Name"].unique())


#OBJECTIVE 1
# Step 1: Select countries
selected_countries = ['India', 'China', 'United States', 'Indonesia', 'Brazil']
country_df = df[df["Country Name"].isin(selected_countries)]
# Step 2: Prepare year columns (1970–2024)
year_cols = [str(year) for year in range(1962, 2025)]
pop_data = country_df[["Country Name"] + year_cols].set_index("Country Name")
pop_data = pop_data.T
pop_data.index = pop_data.index.astype(int)
# Step 3: Convert to numeric and calculate growth
pop_data = pop_data.apply(pd.to_numeric, errors='coerce')
growth_data = pop_data.pct_change() * 100
# Step 4: Plot
plt.figure(figsize=(12, 6))
for country in selected_countries:
    plt.plot(growth_data.index, growth_data[country], label=country)
plt.title("Year-on-Year Population Growth Rate (1971–2024)")
plt.xlabel("Year")
plt.ylabel("Growth Rate (%)")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show();

#OBJECTIVE 2
#Horizontal Bar Plot - Top 20 most populous countries in 2024
exclusions = [
    'World', 'IDA & IBRD total', 'Low & middle income', 'Middle income', 'IBRD only','Early-demographic dividend', 'Lower middle income', 'Upper middle income','East Asia & Pacific', 'Late-demographic dividend', 'High income','East Asia & Pacific (excluding high income)', 'East Asia & Pacific (IDA & IBRD countries)','South Asia', 'South Asia (IDA & IBRD)', 'OECD members','Sub-Saharan Africa (IDA & IBRD countries)', 'IDA total','Sub-Saharan Africa', 'IDA only', 'Least developed countries: UN classification','Sub-Saharan Africa (excluding high income)', 'Post-demographic dividend','Pre-demographic dividend', 'Fragile and conflict affected situations','Heavily indebted poor countries (HIPC)', 'Europe & Central Asia','Middle East, North Africa, Afghanistan & Pakistan','Africa Eastern and Southern','Middle East, North Africa, Afghanistan & Pakistan (excluding high income)','Middle East, North Africa, Afghanistan & Pakistan (IDA & IBRD)','IDA blend', 'Latin America & Caribbean','Latin America & the Caribbean (IDA & IBRD countries)','Low income', 'Latin America & Caribbean (excluding high income)','Africa Western and Central', 'Arab World','Europe & Central Asia (IDA & IBRD countries)', 'European Union','North America', 'Euro area', 'Europe & Central Asia (excluding high income)','Central Europe and the Baltics','Egypt, Arab Rep.'
]

filtered_df = df[~df["Country Name"].isin(exclusions)].copy()
filtered_df["2024"] = filtered_df["2024"].astype(float)

top20_countries = (
    filtered_df[["Country Name", "2024"]]
    .dropna()
    .sort_values(by="2024", ascending=False)
    .head(20)
    .reset_index(drop=True)
)

plt.figure(figsize=(10, 8))
plt.barh(y=top20_countries["Country Name"], width=top20_countries["2024"], color='#A0522D')
plt.gca().invert_yaxis()
plt.title("Top 20 Most Populous Countries in 2024")
plt.xlabel("Population")
plt.ylabel("Country")
plt.tight_layout()
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.show()


#OBJECTIVE 3
# Step 1: Extract relevant rows
world_pop = df[df["Country Name"] == "World"]["2024"].values[0]
india_pop = df[df["Country Name"] == "India"]["2024"].values[0]
china_pop = df[df["Country Name"] == "China"]["2024"].values[0]

# Step 2: Calculate rest of the world
rest_pop = world_pop - (india_pop + china_pop)

# Step 3: Prepare data
labels = ['India', 'China', 'Rest of the World']
sizes = [india_pop, china_pop, rest_pop]
colors = ['#06065d', '#008080', '#4682B4']

# Step 4: Plot
plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, colors=colors, autopct='%.1f%%', startangle=140)
plt.title("India and China vs Rest of the World (2024 Population)")
plt.axis('equal')  # Equal aspect ratio ensures pie is a circle.
plt.tight_layout()
plt.show()

