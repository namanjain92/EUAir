import pandas as pd
import os
import matplotlib.pyplot as plt


# Load TSV
df = pd.read_csv("data/estat_ttr00012.tsv", sep="\t")

# Split the first column into separate columns
df[['freq', 'unit', 'tra_meas', 'tra_cov', 'schedule', 'geo']] = df.iloc[:, 0].str.split(',', expand=True)

# Drop the original combined column
df = df.drop(df.columns[0], axis=1)

# Convert to long format from wide format
df_long = df.melt(id_vars=['freq', 'unit', 'tra_meas', 'tra_cov', 'schedule', 'geo'],
                  var_name='year', value_name='passengers')

# Convert passengers to numeric
df_long['passengers'] = pd.to_numeric(df_long['passengers'], errors='coerce')

# Convert year to int
df_long['year'] = df_long['year'].astype(int)

# Check cleaned data
print(df_long.head(10))


if not os.path.exists("outputs"):
    os.makedirs("outputs")

# Plot total EU passengers over time ---
eu_total = df_long.groupby('year')['passengers'].sum()

plt.figure(figsize=(8,5))
eu_total.plot(marker='o')
plt.title("Total Air Passengers in EU (2013–2021)")
plt.ylabel("Passengers")
plt.xlabel("Year")
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/total_passengers_eu.png")
plt.show()

#  Top 10 countries in 2019 and 2021 ---
for yr in [2019, 2021]:
    top10 = df_long[df_long['year'] == yr].sort_values('passengers', ascending=False).head(10)
    plt.figure(figsize=(8,5))
    plt.bar(top10['geo'], top10['passengers'], color='skyblue')
    plt.title(f"Top 10 EU Countries by Air Passengers ({yr})")
    plt.ylabel("Passengers")
    plt.xlabel("Country")
    plt.tight_layout()
    plt.savefig(f"outputs/top10_{yr}.png")
    plt.show()

# Percent change 2019 → 2021 (COVID impact) ---
pivot = df_long.pivot(index='geo', columns='year', values='passengers')
pivot['change_%'] = ((pivot[2021] - pivot[2019]) / pivot[2019]) * 100
pivot = pivot.sort_values('change_%')

plt.figure(figsize=(8,10))
pivot['change_%'].plot(kind='barh', color='orange')
plt.title("Percent Change in Air Passengers (2019 → 2021)")
plt.xlabel("Percent Change")
plt.ylabel("Country")
plt.tight_layout()
plt.savefig("outputs/covid_impact_change.png")
plt.show()
