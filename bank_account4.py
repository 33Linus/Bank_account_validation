# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 12:57:48 2022

@author: Linus
"""
import pandas as pd
import copy

details_df = pd.read_csv('acc_details.csv')

df = details_df.set_index('Account_ID')
bank_dict = df.T.to_dict('list')

types = ['S','C','D']
# to find duplicate records in given dataframe
duplicate = details_df[details_df.duplicated()]
dup_dict = duplicate.set_index('Account_ID')
rej_dict = dup_dict.T.to_dict('list')             # rejected dict

for k,v in rej_dict.items():
    if k in bank_dict.keys():
        v.append('duplicate record')
        rej_dict.update({k:v})


ALPHA = ['A','B','C','D','E','F','G','H','I','J','K','L','M',\
         'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
alpha = [i.lower() for i in ALPHA]

for k,v in bank_dict.items():
    for a in k[1:]:
        if a in ALPHA or a in alpha:
            val = copy.deepcopy(v)
            val.append('not a valid account number')
            rej_dict.update({k:val})
            
    if len(k[1:]) < 7 or len(k[1:]) > 12:
        val = copy.deepcopy(v)  
        val.append('invalid length of account number')
        rej_dict.update({k:val})
    
    if k[0] not in types:
        val = copy.deepcopy(v)  
        val.append('invalid account type')
        rej_dict.update({k:val})
        
for k,v in rej_dict.items():
    if k in bank_dict.keys():
        bank_dict.pop(k)

rej_dict1 = {'BankID':[v[0] for k,v in rej_dict.items()],
             'AccountID':list(rej_dict.keys()),
             'Reason':[v[1] for k,v in rej_dict.items()]}

val_bank_id = [v[0] for k,v in bank_dict.items()]

# val_bank_id2 = []
# for i in val_bank_id:
#     val_bank_id2.append(i[0])

valid_dict = {'Bank_ID':val_bank_id,
              'Account_type':[k[0] for k,v in bank_dict.items()],
              'Account_number':[k[1:] for k,v in bank_dict.items()]}

valid = pd.DataFrame(valid_dict)
rej = pd.DataFrame(rej_dict1)
print(rej)
print(valid)
valid.to_csv('target_bank_accounts.csv')
rej.to_csv('rejected_accounts.csv')