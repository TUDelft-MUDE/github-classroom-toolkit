import pandas as pd

# Load CSV into a DataFrame
df = pd.read_csv("final_grade_output/MUDE AP Grading - Sheet1 (3).csv")

# Create a new DataFrame with a subset of columns
df = df[['OrgDefinedId', 'New Percentage when GA 2.6 removed', ]]


def complex_logic(row):
    column_name = 'New Percentage when GA 2.6 removed'
    if row[column_name] < 0.10:
        return 0.0
    elif row[column_name] < 0.20:
        return 1.0
    elif row[column_name] < 0.30:
        return 2.0
    elif row[column_name] < 0.40:
        return 3.0
    elif row[column_name] < 0.50:
        return 4.0
    elif row[column_name] < 0.62:
        return 5.0
    elif row[column_name] < 0.70:
        return 5.5
    elif row[column_name] < 0.73:
        return 6.0
    elif row[column_name] < 0.77:
        return 6.5
    elif row[column_name] < 0.81:
        return 7.0
    elif row[column_name] < 0.85:
        return 7.5
    elif row[column_name] < 0.90:
        return 8.0
    elif row[column_name] < 0.94:
        return 8.5
    elif row[column_name] < 0.99:
        return 9.0
    elif row[column_name] < 1.00:
        return 9.5
    else:
        return 10.0


df['New Percentage when GA 2.6 removed'] = df['New Percentage when GA 2.6 removed'].str.replace(",", ".").astype(float)
df['Grade'] = df.apply(complex_logic, axis=1)
df = df[['OrgDefinedId', 'Grade', ]]
df['End-of-Line Indicator'] = '#'

file_name = f'final_grade_output/final_grades_brightspace.csv'
df.to_csv(file_name, index=False)
