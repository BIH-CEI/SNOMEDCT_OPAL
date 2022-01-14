# Imports
from styleframe import StyleFrame, Styler
from csv2yaml import csv2yaml
from pathlib import Path
from os import walk
import pandas as pd
import numpy as np

# Output directory gets created
Path("Output").mkdir(parents=True, exist_ok=True)

# Value 1 = Excel File | Value 2 = CSV + YAML
mode = 2

Semantic_Tag_Columns = None
FSN_Columns = None


def edit_excel(file_path):
    global FSN_Columns
    global Semantic_Tag_Columns
    print(file_path)
    excel_file = pd.read_excel(file_path,
                               dtype=str)
    # Variable for the columns that starts with FSN
    FSN_Columns = excel_file.filter(regex=f"FSN.*").columns

    # Copy the value in between the parenthesis to the column "Semantic_Tag_X"
    for column in FSN_Columns:
        FSN_index = column.split("_")[1]
        # Copy the Semantic tag from the FSN to Semantic_Tag_X column
        excel_file[f"Semantic_Tag_{FSN_index}"] = excel_file[f"FSN_{FSN_index}"].str.replace(r'[^(]*\(|\)[^)]*', '',
                                                                                     regex=True).str.strip()
        # Replace empty spaces with _
        excel_file[f"Semantic_Tag_{FSN_index}"] = excel_file[f"Semantic_Tag_{FSN_index}"].str.replace(" ", "_").str.strip()
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
                FSN_index = column.split("_")[2]
                excel_file.loc[m, f'SNOMED::{semantic_tags[tag]}'] = excel_file.loc[m, f'SCTID_{FSN_index}']

    return excel_file


# Excel file
if mode == 1:
    # Get all files
    _, _, files = next(walk("Files"))
    excel_file = None
    name = None
    # Loop over all the files
    for file_name in files:
        file_df = pd.read_excel(f"Files/{file_name}", sheet_name=None)
        excel_file = edit_excel(f"Files/{file_name}")
        # Write to Excel file
        SCTID_Columns = excel_file.filter(regex=f"SCTID.*").columns
        all_list = SCTID_Columns.to_list() + Semantic_Tag_Columns + FSN_Columns.to_list()
        excel_file = excel_file.drop(columns=all_list)

        col_list = excel_file.columns.tolist()
        excel_writer = pd.ExcelWriter(f"Output/{file_name}")
        # sf = StyleFrame(excel_file)
        # sf.apply_headers_style(Styler(bold=False, horizontal_alignment='left'))
        excel_file.to_excel(excel_writer=excel_writer, index=False, sheet_name="Variables")
        file_df.pop("Variables")
        for file_name in file_df:
            sf = StyleFrame(file_df[file_name])
            col_list = file_df[file_name].columns.tolist()
            # sf.apply_headers_style(Styler(bold=False, horizontal_alignment='left'))
            file_df[file_name].to_excel(excel_writer=excel_writer, index=False, sheet_name=file_name)
        excel_writer.save()
# CSV + YAML
elif mode == 2:
    _, _, files = next(walk("Files"))
    excel_dfs = []
    for file_name in files:
        excel_df = edit_excel(f"Files/{file_name}")
        for tag in FSN_Columns:
            index = tag.split("_")[1]
            df = excel_df[[f"SCTID_{index}", f"FSN_{index}", f"Semantic_Tag_{index}"]]
            df = df.dropna()
            excel_dfs.append(df)

    excel_file = pd.concat(excel_dfs)

    # Write to CSV file
    excel_file.to_csv("Output/Output_CSV.csv",
                      sep=";",
                      index=False)
    # Convert to YAML
    csv2 = csv2yaml("Output/Output_CSV.csv")
