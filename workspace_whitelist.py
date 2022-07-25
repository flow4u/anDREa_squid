# import all the libraries
import pandas as pd
import os
import sys
from tqdm import tqdm
import validators

# number of repeating characters for printing
n=80

# define default filenames and folders
FILE_NAME_WRONG_DOMAINS = 'WRONG_DOMAINS.txt'
FILE_NAME_MISSING_WORKSPACES = 'MISSING_WORKSPACES.txt'
FOLDER_OUTPUT = './output/'

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

    
# read hash file workspace-network
df_hashtable = pd.read_csv('workspaces.csv', index_col=0)

# read the excel
df_workspaces = pd.read_excel(excel, index_col=0, keep_default_na=False)

# read config.txt
with open('config_template.txt') as f:
    config = f.read()


# functions to process the data

def ws_exist(workspace):
    try:
        network = df_hashtable.loc[workspace]['network']
        return True
    except:
        return False
    

def create_conf(workspace):
    network = df_hashtable.loc[workspace]['network']
    new_config = config
    new_config = new_config.replace('{WORKSPACE}', workspace)
    new_config = new_config.replace('{NETWORK}', network)
    return new_config
    

def create_acl(workspace):
    lst = []
    for value, domain in zip(df_workspaces.loc[workspace], df_workspaces.loc[workspace].index):
        if value.lower() == 'x' and validators.domain(domain):
            lst.append('.'+domain)
    return '\n'.join(lst)

def list_wrong_domains(domains):
    lst = []
    for i, item in enumerate(domains):
        if not validators.domain(item):
            lst.append(f'{chr(65+i+1)}: {item}')
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
        save_file(FOLDER_OUTPUT + ws+'.conf', create_conf(ws))
        save_file(FOLDER_OUTPUT + ws+'.domains.acl', create_acl(ws))
    else:
        missing_workspaces.append(ws)

# display and save any missing workspaces
if len(missing_workspaces) != 0:
    print('\n' + '-'*n)
    print('\nThe following Workspaces are missing in the hash table:\n\n')
    for item in missing_workspaces:
        print(item)
    save_file('MISSING_WORKSPACES.txt', '\n'.join(missing_workspaces))    
    print(f'\n\nThe list is saved in {FILE_NAME_MISSING_WORKSPACES}') 
    
print('\n' + '-'*n)
print(f'Finished, files are created in {FOLDER_OUTPUT}')
print('='*n+'\n\n')
