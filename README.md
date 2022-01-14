
# SNOMED OPAL  
  
  
## The Script.py got two modes:  
  
* Mode 1: Excel files  
With the use of mode 1, the user is able to map the FSN_X to SNOMED::X and SCTID_X to the value under the SNOMED::X column. At the end an Excel file gets generated. If you want to have a better looking Excel file you may use the StyleFrame package.    
  
  
* Mode 2: CSV + YAML
With the use of mode 2, the user will get a CSV file generated with the following header: 
SCTID_X;FSN_X;Semantic_Tag_X 
The CSV file is the imput for the csv2yaml.py file. This file filters all the semantic tags and sort all the respective SCTID's under it. At the end a yaml file gets generated.  
  
## Run the code  
Use the Script.py file and choose the mode using the mode variable (1|2)