# important settings
import pandas as pd

class_df = pd.read_csv('COMBINED_Q2_CLASSLIST.csv')  # classlist

# fix the group name
class_df['FixedName'] = class_df['GroupCategory'] + class_df['GroupName'].str[1:]

print(f'test={class_df['FixedName'].value_counts()}')

class_df.to_csv('V3_Q2_CLASSLIST.csv', index=False)