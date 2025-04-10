import pandas as pd

"""
The goal of this script is combining...
"""

df_17 = pd.read_csv('cli/backup_grades_5_11/PA_results/PA 1.7_results.csv')
df_17 = df_17[['OrgDefinedId', 'PA 1.7_passed']]

df_17_2 = pd.read_csv('cli/backup_grades_5_11/PA_results/PA 1.7_2_results.csv')
df_17_2 = df_17_2[['OrgDefinedId', 'PA 1.7_2_passed']]


combined_df = pd.merge(df_17, df_17_2, on='OrgDefinedId', how='left')
combined_df['PassedBoth'] = combined_df['PA 1.7_passed'] | combined_df['PA 1.7_2_passed']

summary_file_name = f'cli/backup_grades_5_11/PA_results/PA 1.7_combined_summary.csv'
with open(summary_file_name, 'w') as file:
    file.write(str(combined_df['PassedBoth'].value_counts()))

# Turn True/False Pass/Fail into a 0 or 10 grade for Brightspace
combined_df['PA 1.7 Points Grade'] = 0
combined_df.loc[combined_df['PassedBoth'], 'PA 1.7 Points Grade'] = 10
# Turn the results into a grades file
combined_df = combined_df[['OrgDefinedId', 'PA 1.7 Points Grade']]
combined_df['End-of-Line Indicator'] = '#'


file_name = 'cli/backup_grades_5_11/PA_results/PA 1.7_combined_grades.csv'
combined_df.to_csv(file_name, index=False)
