import pandas as pd

old_classlist_with_usernames_df = pd.read_csv('classlist_export_2024-10-07-15-47-49.csv')
df_selected = old_classlist_with_usernames_df[['OrgDefinedId', 'GithubUsername',]].copy()
new_class_df = pd.read_csv('classlisto_new - Blad1.csv')

combined_df = new_class_df.merge(df_selected, how='left', on='OrgDefinedId')
combined_df['OrgDefinedId'] = combined_df['OrgDefinedId'].astype('Int64')

file_name = 'COMPLETE_CLASSLIST.csv'
combined_df.to_csv(file_name, index=False)




