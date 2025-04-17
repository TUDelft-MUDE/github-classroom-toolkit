from datetime import datetime
from pathlib import Path

import pandas as pd

from src.utils import excel_utils


def create_feedback_excel_file(json_data, assignment_code: str, columns: list[str], path: Path):
    """
    Creates an Excel file used for grading Group Assignments. The Excel file contains all groups,
    links to the group repository for that assignment and columns for points.

    Easier to use using the CLI than by hand, as it needs accepted assignments JSON data directly.

    :param json_data: Accepted assignments JSON data for the specific GA
    :param assignment_code: Code name for the assignment, e.g. `GA_1_5`
    :param columns: List of column names for question/point columns, e.g. `['question 1', 'question 2', 'bonus']`
    :param path: Path object to location where the created Excel file should be saved to
    """
    # importing group data
    data = []

    for data_point in json_data:
        # not a perfect way to get the group names, but it seems to work
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
    # generate columns for questions
    for question_name in columns:
        df[question_name] = None
    # generate excel file
    datum = datetime.now()
    datum_formatted = datum.strftime("%Y%m%d_%H%M%S")
    file_path = Path(f'{assignment_code}_feedback_{datum_formatted}.xlsx')
    full_path = path / file_path
    excel_utils.save_dataframe_to_excel_table(df, full_path)

