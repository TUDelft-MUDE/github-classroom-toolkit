import pandas as pd

df1 = pd.read_csv('BC_grades/bc_2.1_grades.csv')
print(df1['BC 2.1 Points Grade'].value_counts())
df2 = pd.read_csv('BC_grades/bc_2.1_overview.csv')
print(df2['BC 2.1 Points Grade'].value_counts())

merged = pd.merge(df2, df1, on='OrgDefinedId', how='left')
merged['End-of-Line Indicator'].fillna('MISSING')
# print(merged[merged['End-of-Line Indicator'] == 0])
