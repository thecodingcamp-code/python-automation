import pandas as pd

df = pd.read_csv("orders_raw.csv")

df = df.drop_duplicates()
df = df.dropna(subset=["customer_name"])

df["customer_name"] = df["customer_name"].str.strip()
df["city"] = df["city"].str.strip().str.title()

df["price"] = df["price"].replace(r"[$,]", "", regex=True)
df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["price"] = df["price"].fillna(df["price"].median())

df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce", format="mixed")

print(df)
print(df.isna().sum())