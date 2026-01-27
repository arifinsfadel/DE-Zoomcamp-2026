import pandas as pd

# Load data Green Taxi (November 2025)
file_parquet = "green_tripdata_2025-11.parquet"
df_green = pd.read_parquet(file_parquet)

# Load data Zone Lookup
file_csv = "taxi_zone_lookup.csv"
df_zones = pd.read_csv(file_csv)

print("Data Success Loaded!")


# Check first 5 line 
print(df_green.head())

# Check data type each colom
print(df_green.dtypes)

# Save to CSV without include index
df_green.to_csv("green_tripdata_2025-11.csv", index=False)
print("File CSV berhasil dibuat: green_tripdata_2025-11.csv")


