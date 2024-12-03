import pandas as pd

# Read the Excel file
df = pd.read_excel('Sample-Sales-Data.xlsx')

# Display basic information
print("Excel File Analysis")
print("-" * 50)
print("\nColumns:")
for col in df.columns:
    print(f"- {col}")

print("\nData Types:")
print(df.dtypes)

print("\nSample Data (first 2 rows):")
print(df.head(2))

print("\nBasic Statistics:")
print(df.describe())
