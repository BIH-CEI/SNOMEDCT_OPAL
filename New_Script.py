import pandas as pd
from styleframe import StyleFrame, Styler
from csv2yaml import csv2yaml
import numpy as np

# Value 1 = Excel File | Value 2 = CSV File + YAML
mode = 1

# Read Excel File
# excel_file = pd.read_excel("Probe_Python_SHIP.xlsx",
#                           dtype=str)

excel_file = pd.read_excel("asd.xlsx",
                           dtype=str)

# Variable for the columns that starts with FSN
FSN_Columns = excel_file.filter(regex=f"FSN.*").columns

# Copy the value in between the parenthesis to the column "Semantic_Tag_X"
for column in FSN_Columns:
    index = column.split("_")[1]
    # Copy the Semantic tag from the FSN to Semantic_Tag_X column
    excel_file[f"Semantic_Tag_{index}"] = excel_file[f"FSN_{index}"].str.replace(r'[^(]*\(|\)[^)]*', '',
                                                                                 regex=True).str.strip()
    # Replace empty spaces with _
    excel_file[f"Semantic_Tag_{index}"] = excel_file[f"Semantic_Tag_{index}"].str.replace(" ", "_").str.strip()
    # Remove the parenthesis + value from FSN_Columns
    excel_file[column] = excel_file[column].str.replace(r'\([^)]*\)', '', regex=True).str.strip()

# Variable for the columns that starts with FSN
Semantic_Tag_Columns = excel_file.filter(regex=f"Semantic_Tag.*").columns.to_list()

# List all unique tags
semantic_tags = pd.unique(excel_file[Semantic_Tag_Columns].values.ravel())

# Create the SNOMED columns using this format: "SNOMED::{Semantic_Tag}" and map the SCTID
for tag in range(len(semantic_tags)):
    for column in Semantic_Tag_Columns:
        m = excel_file[column] == semantic_tags[tag]
        if m.any():
            index = column.split("_")[2]
            excel_file.loc[m, f'SNOMED::{semantic_tags[tag]}'] = excel_file.loc[m, f'SCTID_{index}']

if mode == 1:
    # Write to Excel file
    SCTID_Columns = excel_file.filter(regex=f"SCTID.*").columns
    all_list = SCTID_Columns.to_list() + Semantic_Tag_Columns + FSN_Columns.to_list()
    excel_file = excel_file.drop(columns=all_list)
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
