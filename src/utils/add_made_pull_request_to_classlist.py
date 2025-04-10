import pandas as pd

pull_request_df = pd.read_csv('pull_request_makers.csv')
pull_request_df['MadePullRequest'] = True

# load the classlist
class_df = pd.read_csv('cli/classlists/CLASSLIST_3RD.csv')

# combine the grades and the classlist
combined_df = pd.merge(class_df, pull_request_df, on='GithubUsername', how='left')
combined_df['MadePullRequest'] = combined_df['MadePullRequest'].fillna(False)

# save the file
file_name = 'data/classlist_including_prs.csv'
combined_df.to_csv(file_name, index=False)