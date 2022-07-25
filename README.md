# anDREa_squid

## Required modules
- pandas, tqdm, os, sys, validators

Intall via:
> conda install -c conda-forge [module]

or

> pip install [module]

(pip might be pip3)





## Instructions:

- Correct any typos in config_template.txt using a plain text editor
- Use the dws_squid.xlsx as template/example.  To process:

> python .\workspace_whitelist.py [filename].xlsx

*E.g.:*
> python .\workspace_whitelist.py dws_squid.xlsx
    
    
- all output files will be put in a subfolder .\output
- upload all the files
- delete the subfolder


## Error logging
The following text files are used to display errors encountered:
- MISSING_WORKSPACES.txt  (workspaces not in the hash table)
- WRONG_DOMAINS.txt       (domains not meeting URL validator)