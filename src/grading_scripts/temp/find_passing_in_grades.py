import json

import pandas as pd


def find_grades(assignment: str, classlist_filename: str, grades_file: str):
    assert grades_file.endswith('.csv'), 'accepted assignments filename must end with .csv'
    # get accepted assignments file
    grades = pd.read_csv(grades_file)

    classlist = pd.read_csv(classlist_filename)
    # get classlist
    df = classlist[['OrgDefinedId', 'GithubUsername', 'Email', ]].copy()

    result_column_name = f'{assignment}_status'
    df[result_column_name] = "Not found in Accepted Assignments file"
    df[f'{assignment}_passed'] = False

    for index, row in grades.iterrows():
        # df.loc[df['Name'] == 'Jane', 'Score'] = 2
        github_username = str(row['github_username']).lower()
        has_passed = int(row['points_awarded']) != 0
        if has_passed:
            df.loc[df['GithubUsername'] == github_username, result_column_name] = 'Passed'
            df.loc[df['GithubUsername'] == github_username, f'{assignment}_passed'] = True
        else:
            df.loc[df['GithubUsername'] == github_username, result_column_name] = 'Failed'

    result_file_name = f'PA_results/{assignment}_results.csv'
    df.to_csv(result_file_name, index=False)

    print(f'Student Accepted File made with filename {result_file_name}')
    print(f'{df[result_column_name].value_counts()}')

    # Adjust the display option to show all columns
    pd.set_option('display.max_columns', None)

    summary_file_name = f'{result_file_name[:-4]}_summary.csv'
    with open(summary_file_name, 'w') as file:
        file.write(str(df[result_column_name].value_counts()))
        file.write("\n\nNot found rows:\n")
        file.write(
            f'{df.loc[df[result_column_name] == "Not found in Accepted Assignments file"].to_string(index=False)}')
        file.write("\n\nFailed rows:\n")
        file.write(f'{df.loc[df[result_column_name] == "Failed"].to_string(index=False)}')


find_grades(
    'PA 2.5',
    'cli/classlists/V3_Q2_CLASSLIST.csv',
    'downloaded_grades_16_december/pa-2-5-grades-1734364831.csv'
)
