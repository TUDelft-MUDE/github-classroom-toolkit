import pandas as pd

# 1. put old grades in df
raw_grade_df = pd.read_csv(
    'data/CEGM1000 Modelling, Uncertainty and Data for Engineers (202425 Q1)_GradesExport_2025-02-11-15-02.csv')
classlist_df = pd.read_csv('cli/classlists/V3_Q2_CLASSLIST.csv')
# keep only rows that are in the classlist
raw_grade_df = raw_grade_df[raw_grade_df["OrgDefinedId"].isin(classlist_df["OrgDefinedId"])]
# rename columns
rename_dict = {}
for col in raw_grade_df.columns:
    if "<" in col:  # If the column name contains a space
        # Replace spaces with underscores
        new_col_name = col.split(' Points Grade')[0]
        rename_dict[col] = new_col_name
    else:
        rename_dict[col] = col  # Leave it unchanged
raw_grade_df.rename(columns=rename_dict, inplace=True)
raw_grade_df.drop(columns=["End-of-Line Indicator"], inplace=True)
# 2. add new grades to df
ga_new_df = pd.read_csv('GA_results/GA_results_all.csv')
ga_new_df.drop(columns=["End-of-Line Indicator"], inplace=True)
ga_new_df.rename(columns={
    "GA 2.7 Points Grade": "GA 2.7",
    "GA 2.8 Points Grade": "GA 2.8"
}, inplace=True)

bc_new_df = pd.read_csv('BC_grades/BC_grades_all.csv')
bc_new_df.drop(columns=["End-of-Line Indicator"], inplace=True)
bc_new_df.rename(columns={
    "BC 2.6 Points Grade": "BC 2.6",
    "BC 2.7 Points Grade": "BC 2.7",
    "BC 2.8 Points Grade": "BC 2.8"
}, inplace=True)

pa_new_df = pd.read_csv('PA_grades/PA 2.8.csv')
pa_new_df.drop(columns=["End-of-Line Indicator"], inplace=True)
pa_new_df.rename(columns={
    "PA 2.8 Points Grade": "PA 2.8"
}, inplace=True)
# merge with raw grade df

# print(raw_grade_df.columns.duplicated().any())
# print(ga_new_df.columns.duplicated().any())
# print(bc_new_df.columns.duplicated().any())
# print(pa_new_df.columns.duplicated().any())

raw_grade_df = raw_grade_df.set_index("OrgDefinedId")
ga_new_df = ga_new_df.set_index("OrgDefinedId")
bc_new_df = bc_new_df.set_index("OrgDefinedId")
pa_new_df = pa_new_df.set_index("OrgDefinedId")

raw_grade_df["GA 2.7"] = ga_new_df["GA 2.7"]
raw_grade_df["GA 2.8"] = ga_new_df["GA 2.8"]

raw_grade_df["BC 2.6"] = bc_new_df["BC 2.6"]
raw_grade_df["BC 2.7"] = bc_new_df["BC 2.7"]
raw_grade_df["BC 2.8"] = bc_new_df["BC 2.8"]

raw_grade_df["PA 2.8"] = pa_new_df["PA 2.8"]

# 3. make sure df is a students x assignments matrix where each entry is the points
for col in raw_grade_df.columns:
    if "BC " in col:
        raw_grade_df[col] = raw_grade_df[col] * 0.2
    elif "PA " in col:
        raw_grade_df[col] = raw_grade_df[col] * 0.25

# TODO: Some students only did Q2
# 4. add a total points and a final grade column
cols_to_sum = raw_grade_df.columns.difference(["OrgDefinedId"])
raw_grade_df["Total Points"] = raw_grade_df[cols_to_sum].sum(axis=1)


def complex_logic(row):
    if row["Total Points"] < 21:
        return 0.0
    elif row["Total Points"] < 41:
        return 1.0
    elif row["Total Points"] < 61:
        return 2.0
    elif row["Total Points"] < 81:
        return 3.0
    elif row["Total Points"] < 102:
        return 4.0
    elif row["Total Points"] < 125:
        return 5.0
    elif row["Total Points"] < 142:
        return 5.5
    elif row["Total Points"] < 149:
        return 6.0
    elif row["Total Points"] < 156:
        return 6.5
    elif row["Total Points"] < 164:
        return 7.0
    elif row["Total Points"] < 173:
        return 7.5
    elif row["Total Points"] < 182:
        return 8.0
    elif row["Total Points"] < 191:
        return 8.5
    elif row["Total Points"] < 200:
        return 9.0
    elif row["Total Points"] < 203:
        return 9.5
    else:
        return 10.0


raw_grade_df["grade"] = raw_grade_df.apply(complex_logic, axis=1)
# 5. add name & group columns
raw_grade_df = classlist_df[['OrgDefinedId', 'Username', 'LastName', 'FirstName', 'FixedGroupName']].merge(
    raw_grade_df,
    on='OrgDefinedId',
    how='left'
)
raw_grade_df.rename(columns={
    "FixedGroupName": "GroupName",
    "Total Points": "Total Points No Bonus/Exceptions"
}, inplace=True)
# 6. save this "raw" grade matrix
file_name = f'final_grade_output/raw_grades.csv'
raw_grade_df.to_csv(file_name, index=False)
raw_grade_df.to_excel('final_grade_output/raw_grades.xlsx', index=False)
