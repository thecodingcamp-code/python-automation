import pandas as pd

df = pd.read_excel("inventory.xlsx", sheet_name="Stock")
print(df)

# Total quantity per warehouse
totals = df.groupby("Warehouse")["Quantity"].sum()
print(totals)

# Filter down to anything running low
low_stock = df[df["Quantity"] < 10]
print(low_stock)

df.to_excel("inventory_updated.xlsx", sheet_name="Stock", index=False)