import pandas as pd

classlist_df = pd.read_csv('cli/classlists/V3_Q2_CLASSLIST.csv')
questionnaire_df = pd.read_excel('data/PA 2.82024-2025(1-272).xlsx')
student_number_col = 'What is your student number?\n\n\nOnly used to check that you completed the survey.\n'
questionnaire_df['OrgDefinedId'] = questionnaire_df[student_number_col]

# todo wladimir kattentidt filled in the wrong student number
questionnaire_df.loc[questionnaire_df['What is your name?\n\nOnly used to check that you completed the survey.'] == 'Wladimir Kattentidt', 'OrgDefinedId'] = 5610001
questionnaire_df['PA 2.8 Points Grade'] = 10
df = classlist_df.merge(questionnaire_df[['OrgDefinedId', 'PA 2.8 Points Grade']], on="OrgDefinedId", how='left')
df.fillna({'PA 2.8 Points Grade': 0}, inplace=True)
df = df[['OrgDefinedId', 'PA 2.8 Points Grade']]
df['End-of-Line Indicator'] = '#'
df.drop_duplicates(subset=['OrgDefinedId', 'PA 2.8 Points Grade'], inplace=True)
file_name = f'PA_grades/PA 2.8.csv'
df.to_csv(file_name, index=False)