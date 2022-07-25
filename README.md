# anDREa_squid

## Required modules
- pandas, tqdm, os, sys

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
    
    
- all output will be put in a subfolder .\output
- upload all the files
- delete the subfolder