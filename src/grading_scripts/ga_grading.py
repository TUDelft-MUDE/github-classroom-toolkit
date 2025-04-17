import pandas as pd

"""
This script creates a Brightspace-compatible grades file based on group assignment (GA) scores.

It merges student data from a classlist CSV with group-level grades from an Excel file,
associating each student with their group's grade. The resulting file is in the appropriate Brightspace format.
"""


def create_ga_grades(assignment_name: str, classlist_path: str, grade_excel_path: str):
    """
    Creates a Brightspace-compatible CSV file containing individual grades for a group assignment.

    This function merges student data from the classlist with group-level grades from the provided
    Excel sheet. It matches students to their groups, applies the grades, and formats the result
    for Brightspace import.

    :param assignment_name: Assignment name used as a prefix for the Brightspace grade column (e.g., "GA 2.8")
    :param classlist_path: Path to the CSV file containing the Brightspace classlist
    :param grade_excel_path: Path to the Excel file with group-level grades
    """
    # classlist
    class_df = pd.read_csv(classlist_path)
    # GA grade excel
    grade_df = pd.read_excel(grade_excel_path)
    # TODO: fix this to be more general. probably add param for changed column name with =None default value
    # make all group names upper case, to make comparing easier
    grade_df['group_name'] = grade_df['group_name'].str.upper()
    print(grade_df.columns)
    grade_df['grade'] = grade_df['preliminary grade']
    # rename group_name column to align with the classlist style
    grade_df.rename(columns={'group_name': 'FixedGroupName'}, inplace=True)

    # combine the grades and the classlist
    combined_df = pd.merge(class_df, grade_df, on='FixedGroupName', how='left')

    # we only need the student number and the grade
    df_selected = combined_df[['OrgDefinedId', 'grade', ]].copy()
    # make sure student number is rendered as an integer, without a decimal
    df_selected['OrgDefinedId'] = df_selected['OrgDefinedId'].astype('Int64')
    # rename the grade column to the correct (predefined) column in Brightspace
    df_selected.rename(columns={'grade': f'{assignment_name} Points Grade'}, inplace=True)
    # add end of line indicator, needed by Brightspace for import to correctly work
    df_selected['End-of-Line Indicator'] = '#'

    ga_grades_path = '../../data/output/ga'
    file_name = f'{ga_grades_path}/{assignment_name}_grades.csv'
    df_selected.to_csv(file_name, index=False)


# example usage:
# create_ga_grades(
#     assignment_name='GA 2.8',
#     classlist_path='../../data/classlists/V3_Q2_CLASSLIST.csv',
#     grade_excel_path='../../data/input/ga_grade_excel_sheets/GA_2_8_feedback_20250117_153423(filled).xlsx',
# )
