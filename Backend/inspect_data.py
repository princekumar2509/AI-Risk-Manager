import pandas as pd

# Load dataset
df = pd.read_csv("../data/orders.csv")

print("=" * 50)
print("AI RISK MANAGER - DATASET INSPECTION")
print("=" * 50)

# Basic information
print("\n1. DATASET SHAPE")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

# Column names
print("\n2. COLUMNS")
print(df.columns.tolist())

# First 5 rows
print("\n3. FIRST 5 ROWS")
print(df.head())

# Data types
print("\n4. DATA TYPES")
print(df.dtypes)

# Missing values
print("\n5. MISSING VALUES")
print(df.isnull().sum())

# Duplicate rows
print("\n6. DUPLICATE ROWS")
print(df.duplicated().sum())

# Target distribution
print("\n7. RETURN DISTRIBUTION")
print(df["returned"].value_counts())

print("\nRETURN PERCENTAGE")
print(df["returned"].value_counts(normalize=True) * 100)

# Numerical statistics
print("\n8. NUMERICAL STATISTICS")
print(df.describe())

print("\n" + "=" * 50)
print("INSPECTION COMPLETE")
print("=" * 50)