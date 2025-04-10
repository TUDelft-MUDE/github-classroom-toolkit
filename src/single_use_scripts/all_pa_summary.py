import pandas as pd
import glob

# Step 1: Specify the path to your CSV files
csv_files = glob.glob('cli/backup_grades_5_11/PA_grades/*.csv')  # Adjust the path accordingly

# Step 2: Load CSV files into a list of DataFrames
dataframes = [pd.read_csv(file, usecols=[0, 1]) for file in csv_files]

# Step 3: Merge all DataFrames on the specified key
# Replace 'your_key' with the column name you want to merge on
merged_df = dataframes[0]  # Start with the first DataFrame

for df in dataframes[1:]:
    merged_df = merged_df.merge(df, on='OrgDefinedId', how='left')  # Use 'outer', 'inner', etc. as needed

# Now merged_df contains all the data merged on 'your_key'
slice_df = merged_df.iloc[:, 1:]
# print(slice_df)
passing_students = (slice_df == 10).all(axis=1)
count = passing_students.sum()

merged_df[passing_students].to_csv('data/passing_students', index=False)
merged_df[~merged_df.index.isin(passing_students[passing_students].index)].to_csv('data/failing_students', index=False)

# didnt pass PA 1.5

non_PA15_students = merged_df[(merged_df.iloc[:, [1, 2, 4, 5, 6]] == 10).all(axis=1)]
non_PA15_students = non_PA15_students[(merged_df.iloc[:, [3]] == 0).all(axis=1)]
print(non_PA15_students)
non_PA15_students.to_csv('data/non_PA15_students', index=False)