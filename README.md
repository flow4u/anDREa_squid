# anDREa_squid

## Required modules
- pandas, tqdm, os, sys, validators, configparser

Intall via:
> conda install -c conda-forge [module]

or

> pip install [module]

(pip might be pip3)


## Notes
- All variables used are in workspace_whitelist.ini
- workspace_whitelist.py can be renamed, but the ini must have the same name with .py replaced with .ini

## Instructions:
- Correct any typos in config_template.txt using a plain text editor
- Make changes in the .ini if needed using a plain text editor
- Use the dws_squid.xlsx as template/example.  To process:

> python .\workspace_whitelist.py [filename].xlsx

*E.g.:*
> python .\workspace_whitelist.py dws_squid.xlsx
    
    
- If present, the MISSING_WORKSPACES.txt will be deleted
- If present, the WRONG_DOMAINS.txt will be deleted
- If applicable, the MISSING_WORKSPACES.txt will be created in main folder
- If applicable, the WRONG_DOMAINS.txt will be created in main folder
- all output files will be put in a subfolder .\output
- upload all the files
- delete the subfolder


## Error logging
The following text files are used to display errors encountered:
- MISSING_WORKSPACES.txt  (workspaces not in the hash table)
- WRONG_DOMAINS.txt       (domains not meeting URL validator)