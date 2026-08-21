import pdfplumber
import pandas as pd

with pdfplumber.open("sales_report.pdf") as pdf:
    page1_table = pdf.pages[0].extract_table()
    page2_table = pdf.pages[1].extract_table()


combined_rows = page1_table[1:] + page2_table[1:]  # skip the header on every page after the first
headers = page1_table[0]

df = pd.DataFrame(combined_rows, columns=headers)

with pdfplumber.open("sales_report.pdf") as pdf:
    page2 = pdf.pages[1]
    tables = page2.extract_tables()


table_settings = {
    "vertical_strategy": "text",
    "horizontal_strategy": "text",
    "snap_tolerance": 10,
    "join_tolerance": 10,
    "text_x_tolerance": 5,
}

summary_region = page2.crop((0, 380, page2.width, 470))
summary_table = summary_region.extract_table(table_settings=table_settings)

with pdfplumber.open("sales_report.pdf") as pdf:
    page2 = pdf.pages[1]
    all_tables = page2.extract_tables()

print("Tables found:", len(all_tables))
for i, t in enumerate(all_tables):
    print(f"Table {i}:")
    print(t)