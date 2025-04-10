import pandas as pd
import glob


def combine_all_grades(folder):
    # todo: split into func and func that just combined multiple input cvs
    # Step 1: Specify the path to your CSV files
    csv_files = glob.glob(f'{folder}/*_grades.csv')  # Adjust the path accordingly

    # Step 2: Load CSV files into a list of DataFrames
    dataframes = [pd.read_csv(file, usecols=[0, 1]) for file in csv_files]

    # Step 3: Merge all DataFrames on the specified key
    # Replace 'your_key' with the column name you want to merge on
    merged_df = dataframes[0]  # Start with the first DataFrame

    for df in dataframes[1:]:
        merged_df = merged_df.merge(df, on='OrgDefinedId', how='left')  # Use 'outer', 'inner', etc. as needed

    merged_df['End-of-Line Indicator'] = '#'

    merged_df.to_csv(f'{folder}/{folder}_combined.csv', index=False)


combine_all_grades(folder='PA_grades_uploaded_PA28_removed')
