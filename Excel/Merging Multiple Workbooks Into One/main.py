import glob
import pandas as pd

all_files = glob.glob("regional_sales/*.xlsx")

column_map = {
    "Units Sold": "Units",
    "Revenue ($)": "Revenue"
}


frames = []
for filepath in all_files:
    df = pd.read_excel(filepath, sheet_name="Sales")
    df = df.rename(columns=column_map)  # apply the same fix to any file that needs it
    df["Region"] = filepath.split("_")[-1].replace(".xlsx", "").title()
    frames.append(df)

combined = pd.concat(frames, ignore_index=True)
combined.to_excel("regional_sales_combined.xlsx", sheet_name="Combined", index=False)