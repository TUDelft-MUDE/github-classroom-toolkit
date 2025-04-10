import pandas as pd

classlist = pd.read_csv('data/classlist_including_prs.csv')

pa15_results = pd.read_csv('backup_grades_5_11/PA_results/PA 1.5_results.csv')
results = pa15_results[['OrgDefinedId', 'PA 1.5_passed']]

df = pd.merge(classlist, results, on='OrgDefinedId', how='left')

students_passed = df[df['MadePullRequest'] & df['PA 1.5_passed']]
students_failed_pr = df[~df['MadePullRequest'] & df['PA 1.5_passed']]
students_failed_coding = df[df['MadePullRequest'] & (~df['PA 1.5_passed'])]
students_failed_both = df[(~df['MadePullRequest']) & (~df['PA 1.5_passed'])]

students_passed.to_csv(f'PA1_5_data/passed', index=False)
students_failed_pr.to_csv(f'PA1_5_data/failed_pr', index=False)
students_failed_coding.to_csv(f'PA1_5_data/failed_coding', index=False)
students_failed_both.to_csv(f'PA1_5_data/failed_both', index=False)