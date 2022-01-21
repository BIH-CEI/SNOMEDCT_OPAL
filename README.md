
# SNOMED OPAL

## Abstract

SNOMED CT fosters interoperability in healthcare and research. This use case implemented SNOMED CT for browsing COVID-19 questionnaires in open-software solutions OPAL/MICA. We implemented a test server requiring files in a given YAML format for implementation of taxonomies with only two levels of hierarchy. Within this current format, neither the implementation of SNOMED CT hierarchies and post-coordination nor the use of release files was possible. To solve this, Python scripts were written to integrate the required SNOMED CT concepts (Fully Specified Name, FSN and SNOMED CT Identifier, SCTID) into the YAML format (YAML Mode). Mappings of SNOMED CT to data items of the questionnaires had to be provided as Excel files for implementation into Opal/MICA and further Python scripts were established within the Excel Mode. Finally, a total of eight questionnaires containing 1.178 data items were mapped to SNOMED CT and implemented in OPAL/MICA. This use case showed that implementing SNOMED CT for browsing COVID-19 questionnaires is feasible despite software solutions not supporting SNOMED CT. However, limitations of not being able to implement SNOMED CT release files and its provided hierarchy and post-coordination still have to be conquered.  
  
## The Script.py got two modes:  
  
* Mode 1: Excel files  
With the use of mode 1, the user is able to map the FSN_X to SNOMED::X and SCTID_X to the value under the SNOMED::X column. At the end an Excel file gets generated. If you want to have a better looking Excel file you may use the StyleFrame package.    
  
  
* Mode 2: CSV + YAML
With the use of mode 2, the user will get a CSV file generated with the following header: 
SCTID_X;FSN_X;Semantic_Tag_X 
The CSV file is the imput for the csv2yaml.py file. This file filters all the semantic tags and sort all the respective SCTID's under it. At the end a yaml file gets generated.  
  
## Run the code  
Use the Script.py file and choose the mode using the mode variable (1|2)