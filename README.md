# anDREa_squid

## Required modules
- pandas, tqdm, os, sys, validators, configparser

Intall via:
> conda install -c conda-forge [module]

or

> pip install [module]

(pip might be pip3)


## Notes
- All variables used are in workspace_whitelist3.ini
- workspace_whitelist3.py can be renamed, but the ini must have the same name with .py replaced with .ini

## Instructions:
- Correct any typos in config_template.txt using a plain text editor
- Make changes in the .ini if needed using a plain text editor
- All Excels to be processed must be stored in the subfolder as named in the .ini
   - run python workspace_whitelist3.py once to create the folder
- Use the dws_squid.xlsx as template/example.  To process:

> python .\workspace_whitelist3.py

- all output files will be put in a subfolder .\<yyyymmdd-hhmmss>_output
- If applicable, the <excel>_WRONG_DOMAINS.txt will be added there
- the processed Excels will be moved to there as well

## Error logging
The following text files are used to display errors encountered:
- <excel>_WRONG_DOMAINS.txt       (domains not meeting URL validator)