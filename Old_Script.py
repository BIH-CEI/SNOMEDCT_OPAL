import pandas as pd

excel_file_name = "50010_GECCO COVID-19 Research-Dataset_CV_11032021.xlsx"
excel_file = pd.read_excel(excel_file_name)

excel_file["Semantic_Tag"] = excel_file["SNOMED_FSN"].str.replace(r'[^(]*\(|\)[^)]*', '', regex=True).str.strip()
excel_file["SNOMED_FSN"] = excel_file["SNOMED_FSN"].str.replace(r'\([^)]*\)', '', regex=True).str.strip()

excel_file.to_csv('output.csv',
                  sep=";")
