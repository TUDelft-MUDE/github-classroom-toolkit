import pandas as pd

# Load both CSV files
df1 = pd.read_csv("PA_grades_uploaded_PA28_removed/PA_grades_uploaded_PA28_removed_all.csv")
df2 = pd.read_csv("PA_grades/PA_grades_all.csv")
classlist_df = pd.read_csv("cli/classlists/V3_Q2_CLASSLIST.csv")[['OrgDefinedId', 'FirstName', 'LastName']]

df1 = classlist_df.merge(df1, on='OrgDefinedId', how='left')

# List to hold output strings
output = []

# Iterate through rows and columns to compare values
for index, row in df1.iterrows():
    org_defined_id = row['OrgDefinedId']
    first_name = row['FirstName']
    last_name = row['LastName']
    row_diff = []

    # Compare the row in df1 and df2
    for column in df1.columns:
        if column not in ['OrgDefinedId', 'FirstName', 'LastName']:  # Skip 'OrgDefinedId' column
            old_value = row[column]
            new_value = df2.at[index, column]
            if old_value != new_value:  # Check if there's a difference
                row_diff.append(f"\t{str(column).split(" Points Grade")[0]}: old={old_value} new={new_value}\n")

    # If there are differences, add to output
    if row_diff:
        # output.append(f"({org_defined_id}):\n" + "".join(row_diff))
        output.append(f"{first_name} {str(last_name)} ({org_defined_id}):\n" + "".join(row_diff))

# Write the output to a new file
with open('PA_grades/output.csv', 'w', encoding='utf-8') as f:
    for line in output:
        f.write(line + '\n')

print("Comparison complete. Check the output.csv file.")
