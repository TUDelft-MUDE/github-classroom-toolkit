import json

import pandas as pd


def find_accepted_students(assignment: str, classlist_filename: str, accepted_assignments_filename: str):
    assert accepted_assignments_filename.endswith('.json'), 'accepted assignments filename must end with .json'
    # get accepted assignments file
    with open(accepted_assignments_filename, 'r') as file:
        # Load the data from the file
        accepted_assignments_data = json.load(file)

    classlist = pd.read_csv(classlist_filename)
    # get classlist
    df = classlist[['OrgDefinedId', 'GithubUsername', 'Email', ]].copy()

    result_column_name = f'{assignment}_status'
    df[result_column_name] = "Not found in Accepted Assignments file"
    df[f'{assignment}_passed'] = False

    for assignment_data in accepted_assignments_data:
        # df.loc[df['Name'] == 'Jane', 'Score'] = 2
        github_username = str(assignment_data['students'][0]['login']).lower()
        has_passed = assignment_data['passing']
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


find_accepted_students(
    'PA 2.1',
    'cli/classlists/V3_Q2_CLASSLIST.csv',
    'data/dump_PA_2_1_accepted_assignments_20250226_143308.json'
)
find_accepted_students(
    'PA 2.2',
    'cli/classlists/V3_Q2_CLASSLIST.csv',
    'data/dump_PA_2_2_accepted_assignments_20250226_143538.json'
)
find_accepted_students(
    'PA 2.3',
    'cli/classlists/V3_Q2_CLASSLIST.csv',
    'data/dump_PA_2_3_accepted_assignments_20250226_145027.json'
)
find_accepted_students(
    'PA 2.4',
    'cli/classlists/V3_Q2_CLASSLIST.csv',
    'data/dump_PA_2_4_accepted_assignments_20250226_154818.json'
)
find_accepted_students(
    'PA 2.5',
    'cli/classlists/V3_Q2_CLASSLIST.csv',
    'data/dump_PA_2_5_accepted_assignments_20250226_155116.json'
)
find_accepted_students(
    'PA 2.6',
    'cli/classlists/V3_Q2_CLASSLIST.csv',
    'data/dump_PA_2_6_accepted_assignments_20250226_155832.json'
)
find_accepted_students(
    'PA 2.7',
    'cli/classlists/V3_Q2_CLASSLIST.csv',
    'data/dump_PA_2_7_accepted_assignments_20250226_160151.json'
)
