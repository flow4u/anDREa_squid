# import all the libraries
import pandas as pd
import os
import sys
from tqdm import tqdm
import validators
import configparser

# number of repeating characters for printing
n=80

# define config
# CONFIG_INI = sys.argv[0][0:-3]+'.ini'
CONFIG_INI = ((sys.argv[0][0:-3]+'.ini').split('\\'))[-1]

# verify config_ini exists
try: os.path.exists(CONFIG_INI)
except:
    error_message(f'{CONFIG_INI} is missing')
    exit(0)
    
# Read workspace_whitelist.ini
config = configparser.ConfigParser()
config.sections()
config.read(CONFIG_INI)


# define default filenames and folders
FILE_NAME_WRONG_DOMAINS = config['OUTPUT']['FILE_NAME_WRONG_DOMAINS']
FILE_NAME_MISSING_WORKSPACES = config['OUTPUT']['FILE_NAME_MISSING_WORKSPACES']
FOLDER_OUTPUT = config['OUTPUT']['FOLDER_OUTPUT']

CONFIG_TEMPLATE = config['REQUIRED']['CONFIG_TEMPLATE']
WORKSPACES_CSV = config['REQUIRED']['WORKSPACES_CSV']

SEARCH_WORKSPACE = config['SEARCH_REPLACE']['SEARCH_WORKSPACE']
SEARCH_NETWORK = config['SEARCH_REPLACE']['SEARCH_NETWORK']

WORKSPACES_NETWORK = config['WORKSPACES']['WORKSPACES_NETWORK']
WORKSPACES_WORKSPACE = config['WORKSPACES']['WORKSPACES_WORKSPACE']

EXT_CONFIG = config['EXTENSIONS']['EXT_CONFIG']
EXT_ACL = config['EXTENSIONS']['EXT_ACL']


# error message
def error_message(message):
    print('\n\n'+'='*n)
    print(message)
    print('\n\nExample:\n')
    print('python .\workspace_whitelist.py dws_squid.xlsx')
    print('\n'+'='*n+'\n\n')


# check if Excel is given
try:
    excel = sys.argv[1]
    os.path.exists(excel)
    if excel[-5:] != '.xlsx': a = 1/0
except:
    error_message('Please provide a valid Excel file')
    exit(0)

# check if required files are present
try: os.path.exists(CONFIG_TEMPLATE)
except:
    error_message(f'{CONFIG_TEMPLATE} is missing')
    exit(0)
try: os.path.exists(WORKSPACES_CSV)
except:
    error_message(f'{WORKSPACES_CSV} is missing')
    exit(0)

    
    
# read hash file workspace-network
df_hashtable = pd.read_csv(WORKSPACES_CSV, index_col=WORKSPACES_WORKSPACE)

# read the excel
df_workspaces = pd.read_excel(excel, index_col=0, keep_default_na=False)

# read config.txt
with open(CONFIG_TEMPLATE) as f:
    config = f.read()


# functions to process the data

def ws_exist(workspace):
    try:
        network = df_hashtable.loc[workspace][WORKSPACES_NETWORK]
        return True
    except:
        return False
    

def create_conf(workspace):
    network = df_hashtable.loc[workspace][WORKSPACES_NETWORK]
    new_config = config
    new_config = new_config.replace(SEARCH_WORKSPACE, workspace)
    new_config = new_config.replace(SEARCH_NETWORK, network)
    return new_config
    

def create_acl(workspace):
    lst = []
    for value, domain in zip(df_workspaces.loc[workspace], df_workspaces.loc[workspace].index):
        if value.lower() == 'x' and validators.domain(domain):
            tmp = '.'.join((domain.split('.')[-2:]))
            lst.append('.'+tmp)
    return '\n'.join(set(lst))

def list_wrong_domains(domains):
    lst = []
    for i, item in enumerate(domains):
        if not validators.domain(item):
            excel_col = f'{chr(65+i//26-1) if i>25 else ""}{chr(65+i%26)}'
            lst.append(f'{excel_col}: {item}')
    return '\n'.join(lst)
                                                   
                                                      
def save_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)
        
        
# cleaning up and create output if it doesn't exist
try: os.remove(FILE_NAME_WRONG_DOMAINS)
except: pass

try: os.remove(FILE_NAME_MISSING_WORKSPACES)
except: pass

try: os.mkdir(FOLDER_OUTPUT)
except: pass
    

# process the excel
print('\n\n'+'='*n)
print(f'Processing: {excel}')
print('-'*n+'\n')


# list wrong domains
wrong_domains = ''
wrong_domains = list_wrong_domains(df_workspaces.columns)
if len(wrong_domains) != 0:
    save_file(FILE_NAME_WRONG_DOMAINS, wrong_domains)
    print('One or more domains were incorrect and are saved in:')
    print(FILE_NAME_WRONG_DOMAINS)
    print('\n' + '-'*n)


# list for workspaces missing in the hashtable
missing_workspaces = []

# created the output
print('\nCreating the .conf and .acl files for known workspaces and valid domains.\n')
for ws in tqdm(df_workspaces.index):
    if ws_exist(ws):
        save_file(FOLDER_OUTPUT + ws + EXT_CONFIG, create_conf(ws))
        save_file(FOLDER_OUTPUT + ws + EXT_ACL, create_acl(ws))
    else:
        missing_workspaces.append(ws)

# display and save any missing workspaces
if len(missing_workspaces) != 0:
    print('\n' + '-'*n)
    print('\nThe following Workspaces are missing in the hash table:\n\n')
    for item in missing_workspaces:
        print(item)
    save_file(FILE_NAME_MISSING_WORKSPACES, '\n'.join(missing_workspaces))    
    print(f'\n\nThe list is saved in {FILE_NAME_MISSING_WORKSPACES}') 
    
print('\n' + '-'*n)
print(f'Finished, files are created in {FOLDER_OUTPUT}')
print('='*n+'\n\n')
