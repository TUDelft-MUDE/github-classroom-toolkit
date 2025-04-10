import pandas as pd

pull_request_df = pd.read_csv('data/classlist_including_prs.csv')
pull_request_df = pull_request_df[['OrgDefinedId', 'MadePullRequest']]

accepted_assignment_df = pd.read_csv('cli/backup_grades_5_11/PA_results/PA 1.5_results.csv')
accepted_assignment_df = accepted_assignment_df[['OrgDefinedId', 'PA 1.5_passed']]

combined_df = pd.merge(pull_request_df, accepted_assignment_df, on='OrgDefinedId', how='left')
combined_df['PassedBoth'] = combined_df['MadePullRequest'] & combined_df['PA 1.5_passed']

summary_file_name = f'cli/backup_grades_5_11/PA_results/PA 1.5_combined_summary.csv'
with open(summary_file_name, 'w') as file:
    file.write(str(combined_df['PassedBoth'].value_counts()))

# Turn True/False Pass/Fail into a 0 or 10 grade for Brightspace
combined_df['PA 1.5 Points Grade'] = 0
combined_df.loc[combined_df['PassedBoth'], 'PA 1.5 Points Grade'] = 10
# Turn the results into a grades file
combined_df = combined_df[['OrgDefinedId', 'PA 1.5 Points Grade']]
combined_df['End-of-Line Indicator'] = '#'


file_name = 'cli/backup_grades_5_11/PA_results/PA 1.5_combined_grades.csv'
combined_df.to_csv(file_name, index=False)
