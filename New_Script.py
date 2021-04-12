import pandas as pd
from styleframe import StyleFrame, Styler
from csv2yaml import csv2yaml

# Value 1 = Excel File | Value 2 = CSV File + YAML
mode = 2

# Excel File
excel_file = pd.read_excel("Probe_Python_SHIP.xlsx",
                           dtype=str)

# Copy the value in between the parenthesis to the column "Semantic_Tag"
excel_file["Semantic_Tag"] = excel_file["FSN"].str.replace(r'[^(]*\(|\)[^)]*', '', regex=True).str.strip()

# DROP
excel_file.dropna(subset=["Semantic_Tag"], inplace=True)
excel_file["Semantic_Tag"] = excel_file["Semantic_Tag"].apply(
    lambda x: x.replace(" ", "_").strip() if len(x.strip().split(" ")) > 1 else x.strip())

# Remove the parenthesis + value
excel_file["FSN"] = excel_file["FSN"].str.replace(r'\([^)]*\)', '', regex=True).str.strip()


# Drop duplicates from the column FSN
excel_file.drop_duplicates(subset=["FSN"], inplace=True)

# List all unique tags
semantic_tags = excel_file["Semantic_Tag"].unique()

# Create the SNOMED columns using this format: "SNOMED::{Semantic_Tag}" and map the SCTID
for tag in range(len(semantic_tags)):
    m = excel_file['Semantic_Tag'] == semantic_tags[tag]
    excel_file.loc[m, f'SNOMED::{semantic_tags[tag]}'] = excel_file.loc[m, 'SCTID']

if mode == 1:
    # Write to Excel file
    col_list = excel_file.columns.tolist()
    excel_writer = StyleFrame.ExcelWriter('output.xlsx')
    sf = StyleFrame(excel_file)
    sf.apply_headers_style(Styler(bold=False, horizontal_alignment='left'))
    sf.to_excel(excel_writer=excel_writer, index=False, best_fit=col_list)
    excel_writer.save()
elif mode == 2:
    # Write to CSV file
    excel_file.to_csv("output.csv",
                      sep=";",
                      index=False)
    # Convert to YAML
    csv2 = csv2yaml("output.csv")
