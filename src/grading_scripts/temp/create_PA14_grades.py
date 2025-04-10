import pandas as pd



def create_grades(assignment_name):
    accepted_assignment_df = pd.read_csv(f'PA_results/{assignment_name}_results.csv')
    accepted_assignment_df = accepted_assignment_df[['OrgDefinedId', f'{assignment_name}_passed']]

    # Turn True/False Pass/Fail into a 0 or 10 grade for Brightspace
    accepted_assignment_df[f'{assignment_name} Points Grade'] = 0
    accepted_assignment_df.loc[
        accepted_assignment_df[f'{assignment_name}_passed'], f'{assignment_name} Points Grade'] = 10
    # Turn the results into a grades file
    accepted_assignment_df = accepted_assignment_df[['OrgDefinedId', f'{assignment_name} Points Grade']]
    accepted_assignment_df['End-of-Line Indicator'] = '#'

    file_name = f'PA_grades/{assignment_name}_grades.csv'
    accepted_assignment_df.to_csv(file_name, index=False)


create_grades(assignment_name='PA 2.1')
create_grades(assignment_name='PA 2.2')
create_grades(assignment_name='PA 2.3')
create_grades(assignment_name='PA 2.4')
create_grades(assignment_name='PA 2.5')
create_grades(assignment_name='PA 2.6')
create_grades(assignment_name='PA 2.7')
