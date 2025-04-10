import glob

import pandas as pd


def create_bc_grades(classlist_file, buddycheck_file, grade_name):
    classlist = pd.read_csv(classlist_file)
    # lower emails for comparison
    classlist['Email'] = classlist['Email'].str.lower()

    # combined df starts off as classlist
    combined_df = classlist

    # will use bc for buddycheck
    # bc_csv_files = glob.glob('BuddyCheck/*.csv')
    grade_columns = []
    # print(f'Found {len(bc_csv_files)} BuddyCheck files')
    # for index, csv_file in enumerate(bc_csv_files):
    bc_df = pd.read_csv(buddycheck_file, sep=';')
    bc_df['Email'] = bc_df['Email'].str.lower()
    # print(.value_counts())
    bc_column_name = f'{grade_name} Points Grade'
    grade_columns.append(bc_column_name)
    bc_df[bc_column_name] = 10
    bc_df.loc[bc_df['Submitted'] == 'na', bc_column_name] = 0
    print(bc_df['Submitted'].value_counts())
    bc_df = bc_df[['Email', bc_column_name]]
    combined_df = pd.merge(combined_df, bc_df, on='Email', how='left')
    combined_df[bc_column_name] = combined_df[bc_column_name].fillna(0)
    # print(bc_df.columns)

    # overview file
    combined_df.to_csv(f'BC_grades/{grade_name}_overview.csv', index=False)
    # grades
    combined_df = combined_df[['OrgDefinedId'] + grade_columns]
    combined_df['End-of-Line Indicator'] = '#'
    combined_df.to_csv(f'BC_grades/{grade_name}_grades.csv', index=False)

    print(combined_df[f'{grade_name} Points Grade'].value_counts())


create_bc_grades(
    classlist_file='cli/classlists/V3_Q2_CLASSLIST.csv',
    buddycheck_file='BuddyCheck/MUDE-Week-2-8 - Peer questions results - without self scores.csv',
    grade_name='BC 2.8',
)
