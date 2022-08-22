# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 14:40:20 2022

@author: Linus
"""
import pandas as pd

df = pd.read_csv('acc_details.csv')
target_df = pd.DataFrame()

dup_df = df[['Bank_ID','Account_ID']][df.duplicated()]
dup_df['Reason'] = 'Duplicate Record'

acc_type_df = df[['Bank_ID','Account_ID']][(df['Account_ID'].str[0]!='S') & (df['Account_ID'].str[0]!='C') & (df['Account_ID'].str[0]!='D')]
acc_type_df['Reason'] = 'Account type not valid'

acc_num_len_df = df[['Bank_ID','Account_ID']][~(((df['Account_ID'].str.len()-1)<=12) & ((df['Account_ID'].str.len()-1)>=7))]
acc_num_len_df['Reason'] = 'length of account number is not valid'

acc_num_df = df[['Bank_ID','Account_ID']][df['Account_ID'].str[1:].str.isnumeric() == False]
acc_num_df['Reason'] = 'not a valid account number'

error_df = pd.concat([dup_df,acc_type_df,acc_num_len_df,acc_num_df])

df2 = df.drop_duplicates()

df3 = df2[(df2['Account_ID'].str[0] == 'S') | (df2['Account_ID'].str[0] == 'C') | (df2['Account_ID'].str[0] == 'D')]

df4 = df3[(df3['Account_ID'].str[1:].str.len() < 13) & (df3['Account_ID'].str[1:].str.len() > 6)]

df5 = df4[df4['Account_ID'].str[1:].str.isnumeric() == True]

target_df['Bank_ID'] = df5['Bank_ID']
target_df['Account_Type'] = df5['Account_ID'].str[0]
target_df['Account_num'] = df5['Account_ID'].str[1:]