# import all the libraries
import pandas as pd
import os
import sys
from tqdm import tqdm
import validators
import configparser
from datetime import datetime
import shutil


# number of repeating characters for printing
n=80
VERSION='1.7'
print(f'{VERSION=}')

# define config
# CONFIG_INI = sys.argv[0][0:-3]+'.ini'
CONFIG_INI = ((sys.argv[0][0:-3]+'.ini').split('\\'))[-1]
print(CONFIG_INI)
# verify config_ini exists
try: os.path.exists(CONFIG_INI)
except:
    error_message(f'{CONFIG_INI} is missing')
    exit(0)
    
# Read workspace_whitelist.ini
config = configparser.ConfigParser()
config.sections()
config.read(CONFIG_INI)


# define default folder for excels
FOLDER_INPUT = config['INPUT']['FOLDER_INPUT']

# define default filenames and folders
FOLDER_OUTPUT = config['OUTPUT']['FOLDER_OUTPUT']
FOLDER_ACL = 'squid_files/'
FILE_NAME_WRONG_DOMAINS = config['OUTPUT']['FILE_NAME_WRONG_DOMAINS']
FILE_NAME_MISSING_WORKSPACES = config['OUTPUT']['FILE_NAME_MISSING_WORKSPACES']

CONFIG_TEMPLATE = config['REQUIRED']['CONFIG_TEMPLATE']

SEARCH_WORKSPACE = config['SEARCH_REPLACE']['SEARCH_WORKSPACE']
SEARCH_NETWORK = config['SEARCH_REPLACE']['SEARCH_NETWORK']

WORKSPACES_NETWORK = config['WORKSPACES']['WORKSPACES_NETWORK']
WORKSPACES_WORKSPACE = config['WORKSPACES']['WORKSPACES_WORKSPACE']
WORKSPACES_PROCESS = config['WORKSPACES']['WORKSPACES_PROCESS']

EXT_CONFIG = config['EXTENSIONS']['EXT_CONFIG']
EXT_ACL = config['EXTENSIONS']['EXT_ACL']


# error message
def error_message(message):
    print('\n\n'+'='*n)
    print(message)
    print('\n\nExample:\n')
    print('python .\workspace_whitelist.py')
    print('\n'+'='*n+'\n\n')


# check if Excel if one or more Excels to be processed are present
## just to make sure the required directory exists
try: os.mkdir(FOLDER_INPUT)
except: pass

## list to store files
excels = []
## Iterate directory
for file in os.listdir(FOLDER_INPUT):
    # check only text files
    if file.endswith('.xlsx'):
        excels.append(file)
if not excels:
    error_message('Please add one or more excels in the folder '+FOLDER_INPUT)
    exit(0)
print(excels)



# check if required files are present
try: os.path.exists(CONFIG_TEMPLATE)
except:
    error_message(f'{CONFIG_TEMPLATE} is missing')
    exit(0)

# function to create the config files
def create_conf(workspace):
    network = df_workspaces.loc[workspace][WORKSPACES_NETWORK]
    new_config = config
    new_config = new_config.replace(SEARCH_WORKSPACE, workspace)
    new_config = new_config.replace(SEARCH_NETWORK, network)
    return new_config
    
# function to create the acl files
def create_acl(workspace):
    lst = []
    for value, domain in zip(df_workspaces.loc[workspace], df_workspaces.loc[workspace].index):
        domain='.'.join(filter(None, domain.split('.'))).replace(' ','').lower()
        if (
            value.lower() == 'x' and
            validators.domain(domain)
        ):
            lst.append('.'+'.'.join(domain.split('.')))
    return '\n'.join(set(lst))


# function to check existance of sub and main domains
def subdomain_exist(domain, domains):
    domains_list = list(domains.to_series())
    # domains_lst = tmp.squeeze()
    temp_list = domains_list.copy()
    # print(f'{domain=}')
    temp_list.remove(domain)
    for item in temp_list:
        if item[-len(domain):].replace(' ','').lower() == domain.replace(' ','').lower(): return True
    return False


# function to list all the wrong domains
def list_wrong_domains(domains):
    lst_wrong = []
    lst_wright = []
    for i, item in enumerate(domains):
        item_original = item
        item='.'.join(filter(None, item.split('.'))).replace(' ','').lower()
        sub_exists = subdomain_exist(item_original, domains)
        if (
            not validators.domain(item) or
            item.lower().split('.').count('www') or
            sub_exists
        ):
            add_msg=""
            if sub_exists: add_msg = "(subdomain exists)"
            excel_col = f'{chr(64+(i+3)//26) if i>22 else ""}{chr(65+(i+3)%26)}'
            lst_wrong.append(f'{excel_col}: {item} {add_msg}')
            df_workspaces.drop(item_original, axis=1, inplace=True)
    return '\n'.join(lst_wrong)
    
# read config.txt
with open(CONFIG_TEMPLATE) as f:
    config = f.read()
    
    
# generic function to save a file
def save_file(filename, content):
    print(f'{filename=}')
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
            

# create timestamp string
now = datetime.now() # current date and time
timestamp = now.strftime("%Y%m%d-%H%M%S")
            
            
# create the output folder
timestamped_folder = './' + timestamp + '_' + FOLDER_OUTPUT
os.mkdir(timestamped_folder)
os.mkdir(timestamped_folder + FOLDER_ACL)
            
    
# process all the excels    
for excel in tqdm(excels):    
    # read the excel
    df_workspaces = pd.read_excel(FOLDER_INPUT + '/' + excel, index_col=0, keep_default_na=False)    

    # process the excel
    print('\n\n'+'='*n)
    print(f'Processing: {excel}')
    print('-'*n+'\n')

    # ensure no dahses in the workspace names
    df_workspaces.index = df_workspaces.index.str.replace('-','')
    print(f'{df_workspaces.shape=}')
    
    # list wrong domains
    wrong_domains = ''
    wrong_domains = list_wrong_domains(df_workspaces.columns[2:])
    print(f'{df_workspaces.shape=}')
    if len(wrong_domains) != 0:
        wrong_domains_excel = timestamped_folder + excel[:-5] + '_' + FILE_NAME_WRONG_DOMAINS
        save_file(wrong_domains_excel, wrong_domains)
        print('One or more domains were incorrect and are saved in:')
        print(wrong_domains_excel)
        print('\n' + '-'*n)


    # created the output
    print('\nCreating the .conf and .acl files for known workspaces and valid domains.\n')

    for ws in tqdm(df_workspaces.index):
        if ws and df_workspaces.loc[ws][WORKSPACES_PROCESS].lower() == 'x':
            ws2 = ws.replace('-', '')
            save_file(timestamped_folder + FOLDER_ACL + ws2 + EXT_CONFIG, create_conf(ws2))
            save_file(timestamped_folder + FOLDER_ACL + ws2 + EXT_ACL, create_acl(ws2))
    shutil.make_archive(timestamped_folder + FOLDER_ACL, format='zip', root_dir=timestamped_folder + FOLDER_ACL)
    os.rename(FOLDER_INPUT + '/' + excel, timestamped_folder + excel)
    
print('\n' + '-'*n)
print(f'Finished, files are created in {timestamped_folder}')
print('='*n+'\n\n')
