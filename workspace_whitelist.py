# import all the libraries
import pandas as pd
import os
import sys

# number of repeating characters for printing
n=60

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


# functions to process the data

def ws_exist(workspace):
    try:
        network = df_hashtable.loc[workspace]['network']
        return True
    except:
        return False
    

def create_conf(workspace):
    network = df_hashtable.loc[workspace]['network']
    return '''# /etc/squid/extra.d is the share
# whitelist.conf is the file on the share
acl domains_''' + workspace +''' dstdomain "/etc/squid/extra.d/''' + workspace + '''.domains.acl"

# Sets the source networking subnet for the workspace rule
acl workspace_''' + workspace + ''' src ''' + network + '''

# Allow the workspace network to access domains from workspacelist
http_access allow workspace_''' + workspace + ''' domains_''' + workspace

def create_acl(workspace):
    lst = []
    for value, domain in zip(df_workspaces.loc[workspace], df_workspaces.loc[workspace].index):
        if value.lower() == 'x':
            lst.append(domain)
    return '\n'.join(lst)

def save_file(filename, content):
    with open('./output/' + filename, 'w') as f:
        f.write(content)
        
        
# create output if it doesn't exist
try:
    os.mkdir('./output')
except:
    pass
    

# process the excel
n=50
print('\n\n'+'='*n)
print(f'Processing: {excel}')
print('-'*n+'\n')
for ws in df_workspaces.index:
    if ws_exist(ws):
        save_file(ws+'.conf', create_conf(ws))
        save_file(ws+'.domains.acl', create_acl(ws))
    else:
        print(f'{ws} does not exist in the hash table')
print('\n' + '-'*n)
print(f'Finished, files are created in .\output')
print('='*n+'\n\n')
