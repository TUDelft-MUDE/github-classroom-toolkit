# get classlist
import pandas as pd

# classlist
classlist_filename = "cli/classlists/CLASSLIST_3RD.csv"
classlist = pd.read_csv(classlist_filename)

# excel form
df = pd.read_excel("data/PA1.3_2024-2025 (2).xlsx")

# these students made a mistake while filling in the form
df.iloc[df[df.iloc[:, 7] == 'koomen'].index, 7] = 5080983
df.iloc[df[df.iloc[:, 7] == '`4668782'].index, 7] = 4668782

# processing student numbers from form
student_numbers = pd.DataFrame(df.iloc[:, 7].astype(int))
student_numbers = student_numbers.drop_duplicates()
student_numbers.columns = ['OrgDefinedId']

# assigning form completed: True/False
student_numbers['CompletedForm'] = True
result_df = pd.merge(classlist, student_numbers, on='OrgDefinedId', how='left')
result_df.fillna(value=False, inplace=True)

# Make summary file
summary_file_name = f'cli/backup_grades_5_11/PA_results/SURVEY_summary.csv'
with open(summary_file_name, 'w') as file:
    file.write(str(result_df['CompletedForm'].value_counts()))
    student_numbers_classlist = set(classlist['OrgDefinedId'])
    student_numbers_form = set(student_numbers['OrgDefinedId'])
    in_form_not_in_classlist = student_numbers_form - student_numbers_classlist
    in_classlist_not_in_form = student_numbers_classlist - student_numbers_form
    file.write(f'\n\nIn form: YES\tIn classlist: NO')
    file.write(f'\nAmount of students: {len(in_form_not_in_classlist)}')
    file.write(f'\nStudent Numbers: \t{in_form_not_in_classlist}')
    file.write(f'\n\nIn form: NO \tIn classlist: YES')
    file.write(f'\nAmount of students: {len(in_classlist_not_in_form)}')
    file.write(f'\nStudent Numbers: \t{in_classlist_not_in_form}')



accepted_assignment_df = pd.read_csv('cli/backup_grades_5_11/PA_results/PA 1.3_results.csv')
accepted_assignment_df = accepted_assignment_df[['OrgDefinedId', 'PA 1.3_passed']]

combined_df = pd.merge(result_df, accepted_assignment_df, on='OrgDefinedId', how='left')
combined_df['PassedBoth'] = combined_df['CompletedForm'] & combined_df['PA 1.3_passed']

summary_file_name = f'cli/backup_grades_5_11/PA_results/PA 1.3_combined_summary.csv'
with open(summary_file_name, 'w') as file:
    file.write(str(combined_df['PassedBoth'].value_counts()))

# Turn True/False Pass/Fail into a 0 or 10 grade for Brightspace
combined_df['PA 1.3 Points Grade'] = 0
combined_df.loc[combined_df['PassedBoth'], 'PA 1.3 Points Grade'] = 10
# Turn the results into a grades file
combined_df = combined_df[['OrgDefinedId', 'PA 1.3 Points Grade']]
combined_df['End-of-Line Indicator'] = '#'


file_name = 'cli/backup_grades_5_11/PA_results/PA 1.3_combined_grades.csv'
combined_df.to_csv(file_name, index=False)
