from find_accepted_students import find_accepted_students
from pathlib import Path


def find_files_with_prefix(directory, prefix):
    path = Path(directory)
    result = [f.name for f in path.iterdir() if f.is_file() and f.name.startswith(prefix)]
    assert len(result) == 1, f'Expected len to be 1 but got {result}'
    return result[0]


accepted_assignment_prefixes = [f'dump_PA_1_{n}' for n in [3, 4, 5, 6, '7_accepted', '7_v2', 8]]
accepted_assignment_dumps = ['data/' + find_files_with_prefix('data/', prefix) for prefix in accepted_assignment_prefixes]

assignments = [f'PA 1.{n}' for n in [3, 4, 5, 6, 7, '7_2', 8]]

classlist_filename = "cli/classlists/ROSA_ONLY.csv"

for assignment_name, accepted_assignment_dump in zip(assignments, accepted_assignment_dumps):
    print(f'Handling {assignment_name}..')
    find_accepted_students(
        assignment=assignment_name,
        classlist_filename=classlist_filename,
        accepted_assignments_filename=accepted_assignment_dump,
    )
print('Done..')

