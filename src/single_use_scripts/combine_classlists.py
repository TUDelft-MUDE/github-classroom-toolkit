import pandas as pd

old_classlist = pd.read_csv('cli/classlists/CLASSLIST_3RD.csv')
old_classlist = old_classlist[['OrgDefinedId', 'GithubUsername']]

new_classlist = pd.read_csv('cli/classlists/Q2CLASSLIST.csv')

combined_classlist = pd.merge(new_classlist, old_classlist, on='OrgDefinedId', how='left')
combined_classlist['GithubUsername'] = combined_classlist['GithubUsername'].fillna('Missing')
print(combined_classlist['GithubUsername'].value_counts())

file_name = 'COMBINED_Q2_CLASSLIST.csv'
combined_classlist.to_csv(file_name, index=False)