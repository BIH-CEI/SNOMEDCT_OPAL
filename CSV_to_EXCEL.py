import pandas as pd
from os import listdir
from os.path import isfile, join

# Script für Nina
path = "Variables"
csvfiles = [f for f in listdir(path) if isfile(join(path, f))]

for csv in csvfiles:
    new_name = csv.split(".")[0]
    csv = pd.read_csv(f"{path}/{csv}")
    csv.to_excel(f"{path}/{new_name}.xlsx", index=False)
