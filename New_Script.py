import pandas as pd
from styleframe import StyleFrame, Styler
from csv2yaml import csv2yaml
import numpy as np
from pathlib import Path
from os import walk

Path("Output").mkdir(parents=True, exist_ok=True)

# Value 1 = Excel File | Value 2 = CSV + YAML
mode = 2

Semantic_Tag_Columns = None
FSN_Columns = None

def edit_excel(name):
    global FSN_Columns
    global Semantic_Tag_Columns
    excel_file = pd.read_excel(name,
                               dtype=str)
    print(name)
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

    return excel_file

if mode == 1:
    _, _, files = next(walk("Files"))
    excel_file = None
    name = None
    for x in files:
        name = x
        file = pd.read_excel(f"Files/{x}", sheet_name=None)
        excel_file = edit_excel(f"Files/{x}")
        # Write to Excel file
        SCTID_Columns = excel_file.filter(regex=f"SCTID.*").columns
        all_list = SCTID_Columns.to_list() + Semantic_Tag_Columns + FSN_Columns.to_list()
        excel_file = excel_file.drop(columns=all_list)

        col_list = excel_file.columns.tolist()
        excel_writer = StyleFrame.ExcelWriter(f"Output/{name}")
        sf = StyleFrame(excel_file)
        sf.apply_headers_style(Styler(bold=False, horizontal_alignment='left'))
        sf.to_excel(excel_writer=excel_writer, index=False, best_fit=col_list, sheet_name="Variables")
        file.pop("Variables")
        for x in file:
            sf = StyleFrame(file[x])
            col_list = file[x].columns.tolist()
            sf.apply_headers_style(Styler(bold=False, horizontal_alignment='left'))
            sf.to_excel(excel_writer=excel_writer, index=False, best_fit=col_list, sheet_name=x)
        excel_writer.save()
elif mode == 2:
    _, _, files = next(walk("Files"))
    excel_dfs = []
    for x in files:
        excel_df = edit_excel(f"Files/{x}")
        for tag in FSN_Columns:
            index = tag.split("_")[1]
            df = excel_df[[f"SCTID_{index}", f"FSN_{index}", f"Semantic_Tag_{index}"]]
            df = df.dropna()
            excel_dfs.append(df)

    excel_file = pd.concat(excel_dfs)

    # Write to CSV file
    excel_file.to_csv("output.csv",
                      sep=";",
                      index=False)
    # Convert to YAML
    csv2 = csv2yaml("output.csv")
