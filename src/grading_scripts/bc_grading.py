import pandas as pd

"""
This script generates Brightspace-compatible grade files from Buddycheck exports.

It connects student emails found in the Buddycheck CSV to student numbers in a classlist CSV.
The script then creates two files:
1. An overview file showing all merged data.
2. A Brightspace-compatible grade file containing only student numbers and grade values.

Grades are assigned as follows:
- 10 points if the Buddycheck was submitted.
- 0 points if not submitted or if the student is missing from the Buddycheck file.
"""


def create_bc_grades(classlist_file: str, buddycheck_file: str, grade_name: str):
    """
    Function used to create a brightspace-compatible grades file and an overview file.

    We only get student emails from the buddycheck file, but we need to connect the grades to student numbers
    before we can produce a brightspace-compatible grade file. We do this by connecting the email to the student
    number field in the classlist.

    :param classlist_file: path to an up-to-date classlist
    :param buddycheck_file: path to a brightspace-exported buddycheck csv file
    :param grade_name: brightspace compatible grade name prefix, e.g. `BC 2.8`
    """
    # TODO: connect this to CLI?
    # will use bc for buddycheck
    bc_df = pd.read_csv(buddycheck_file, sep=';')
    # Brightspace compatible grade column name
    bc_column_name = f'{grade_name} Points Grade'
    # give full points if buddycheck was completed
    bc_df[bc_column_name] = 10
    # give zero points if not
    bc_df.loc[bc_df['Submitted'] == 'na', bc_column_name] = 0
    bc_df = bc_df[['Email', bc_column_name]]
    bc_df['Email'] = bc_df['Email'].str.lower()

    classlist_df = pd.read_csv(classlist_file)
    classlist_df['Email'] = classlist_df['Email'].str.lower()
    # merge buddycheck dataframe with classlist as we need student number for brightspace grades
    combined_df = pd.merge(classlist_df, bc_df, on='Email', how='left')
    # also give 0 points to any students included in the classlist but not in brightspace
    # (not sure if this actually is a problem in practice)
    combined_df[bc_column_name] = combined_df[bc_column_name].fillna(0)

    bc_grades_path = '../../data/output/bc'
    # overview file
    combined_df.to_csv(f'{bc_grades_path}/{grade_name}_overview.csv', index=False)
    # grades
    combined_df = combined_df[['OrgDefinedId', bc_column_name]]
    combined_df['End-of-Line Indicator'] = '#'
    combined_df.to_csv(f'{bc_grades_path}/{grade_name}_grades.csv', index=False)

# example usage:
# create_bc_grades(
#     classlist_file='../../data/classlists/q2_classlist.csv',
#     buddycheck_file='BuddyCheck/MUDE-Week-2-8 - Peer questions results - without self scores.csv',
#     grade_name='BC 2.8',
# )
