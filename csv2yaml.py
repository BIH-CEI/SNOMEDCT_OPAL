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
        with open("output.yaml", 'w') as yamlfile:
            yml.dump(data,
                     yamlfile,
                     default_flow_style=False,
                     explicit_start=False,
                     default_style='"',
                     sort_keys=False)
            print("Write successful")
