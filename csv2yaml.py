import yaml as yml
import pandas as pd


class csv2yaml:
    yml.Dumper.ignore_aliases = lambda *args: True

    snomed_data = None

    def __init__(self, df):
        self.snomed_data = pd.read_csv(df,
                                       dtype=str,
                                       encoding='ISO-8859-1',
                                       sep=";")
        print(self.snomed_data)
        SCTID_Columns = self.snomed_data.filter(regex=f"SCTID.*").columns.to_list()
        Semantic_Tag_Columns = self.snomed_data.filter(regex=f"Semantic_Tag.*").columns.to_list()
        FSN_Columns = self.snomed_data.filter(regex=f"FSN.*").columns.to_list()
        all_list = SCTID_Columns + Semantic_Tag_Columns + FSN_Columns
        self.snomed_data.drop(self.snomed_data.columns.difference(all_list), 1, inplace=True)
        dataframes = []
        for tag in FSN_Columns:
            index = tag.split("_")[1]
            df = self.snomed_data[[f"SCTID_{index}", f"FSN_{index}", f"Semantic_Tag_{index}"]]
            df = df.dropna()
            df.columns = ["SCTID", "FSN", "Semantic_Tag"]
            dataframes.append(df)

        print(dataframes)
        df = pd.concat(dataframes)
        print(df)
        self.snomed_data = df.drop_duplicates()
        self.write_yaml()

    def fill_terms(self, df):
        terms_list = []
        for x in range(df.shape[0]):
            terms = {
                "name": df.iloc[x]["SCTID"].strip(),
                "title": {
                    "en": df.iloc[x]["FSN"].strip()
                },
                "description": {},
                "attributes": {},
                "keywords": {},
                "terms": []
            }
            terms_list.append(terms)
        return terms_list

    def fill_vocabularies(self):
        vocabularies_list = []
        print(self.snomed_data.Semantic_Tag.unique())
        for tag in self.snomed_data.Semantic_Tag.unique():
            df = self.snomed_data.query(f'Semantic_Tag == "{tag}"')

            name = df["Semantic_Tag"].iloc[0]
            if len(name.strip().split(" ")) > 1:
                name = name.replace(" ", "_").strip()
            vocabularies = {
                "name": name.strip(),
                "title": {
                    "en": df["Semantic_Tag"].iloc[0].title().strip(),
                },
                "description": {
                    "en": "CHANGE TEXT",
                },
                "attributes": {},
                "keywords": {},
                "terms": self.fill_terms(df)
            }
            vocabularies_list.append(vocabularies)
        return vocabularies_list

    def write_yaml(self):
        data = {
            "name": "SNOMED",
            "title": {
                "en": "SNOMED Ontology"
            },
            "description": {
                "en": "Search for SNOMED CT concept or SCTID"
            },
            "attributes": {},
            "author": "SNOMED International",
            "keywords": {},
            "license": "Member",
            "vocabularies": self.fill_vocabularies()
        }
        with open("Output/Output_YAML.yaml", 'w') as yamlfile:
            yml.dump(data,
                     yamlfile,
                     default_flow_style=False,
                     explicit_start=False,
                     default_style='"',
                     sort_keys=False)
            print("Write successful")
