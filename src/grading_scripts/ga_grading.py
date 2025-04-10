import pandas as pd


# important settings
assignment_name = 'GA 2.8'
class_df = pd.read_csv('cli/classlists/V3_Q2_CLASSLIST.csv')  # classlist
grade_df = pd.read_excel('GA_filled_in/GA_2_8_feedback_20250117_153423(filled).xlsx')  # GA grade excel

# make all group names upper case, to make comparing easier
grade_df['group_name'] = grade_df['group_name'].str.upper()
print(grade_df.columns)
grade_df['grade'] = grade_df['preliminary grade']
# rename group_name column to align with the classlist style
grade_df.rename(columns={'group_name': 'FixedGroupName'}, inplace=True)

# combine the grades and the classlist
combined_df = pd.merge(class_df, grade_df, on='FixedGroupName', how='left')


# we only need the student number and the grade
df_selected = combined_df[['OrgDefinedId', 'grade',]].copy()
# make sure student number is rendered as an integer, without a decimal
df_selected['OrgDefinedId'] = df_selected['OrgDefinedId'].astype('Int64')
# rename the grade column to the correct (predefined) column in Brightspace
df_selected.rename(columns={'grade': f'{assignment_name} Points Grade'}, inplace=True)
# add end of line indicator, needed by Brightspace for import to correctly work
df_selected['End-of-Line Indicator'] = '#'

# save the file
file_name = f'GA_results/{assignment_name}_grades.csv'
df_selected.to_csv(file_name, index=False)

