from datetime import datetime
from pathlib import Path

import pandas as pd

import excel_utils


def create_feedback_excel_file(json_data, assignment_name, columns, path):
    """ needs accepted assignments json """
    # importing group data
    data = []

    for data_point in json_data:
        entry = {}
        # not a perfect way to get the group names but it seems to work
        # (group name = repository name - assignment name)
        assignment_slug = str(data_point['assignment']['slug'])
        group_repository_name = str(data_point['repository']['name'])
        group_name = group_repository_name.split(assignment_slug)[1][1:]
        # get url as well
        url = str(data_point['repository']['html_url'])
        data.append({
            'group_name': group_name,
            # excelified url
            'github_url': f'=HYPERLINK("{url}","LINK TO REPO")',
            })
    df = pd.DataFrame(data)
    # generate pre columns
    # for column_name in pre_columns:
    #     df[column_name] = None
    # generate columns for questions
    for question_name in columns:
        df[question_name] = None
        # df[f'{question_name}_feedback'] = None
    # generate post columns
    # for column_name in post_columns:
    #     df[column_name] = None
    # generate excel file
    now = datetime.now()
    now_formatted = now.strftime("%Y%m%d_%H%M%S")
    file_path = Path(f'{assignment_name}_feedback_{now_formatted}.xlsx')
    full_path = path / file_path
    excel_utils.save_dataframe_to_excel_table(df, full_path)


# assignment_name = 'GA_1_5'
# # column names for questions (feedback columns will be inserted after each of these)
# questions = ['notebook', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8',]
# # column names for questions (feedback columns will NOT be inserted)
# pre_columns = ['grade',]
# post_columns = ['general_comment',]
#
# create_feedback_excel_file(
#     accepted_assignments_file_name=accepted_assignments_file_name,
#     assignment_name=assignment_name,
#     questions=questions,
#     pre_columns=pre_columns,
#     post_columns=post_columns,
# )
