import csv
from github import Github

"""
(Script specific to MUDE 24/25 edition, could be slightly rewritten and reused if necessary.
Will probably not work right out of the box.)

This script fetches and parses 'ticket.md' files from the GitHub repositories of all groups. It extracts group answers 
from the markdown content and stores the results in `output`.

Make sure to set the GitHub personal access token in the `TOKEN` variable before running.

Requirements:
- PyGithub (`pip install PyGithub`)
"""


expected_group_names = []
expected_group_names.extend([f"hind{x}" for x in range(1, 17)])
expected_group_names.extend([f"ming{x}" for x in range(1, 17)])
expected_group_names.extend([f"riba{x}" for x in range(1, 12)])
expected_group_names.extend([f"soga{x}" for x in range(1, 11)])


# Replace with your GitHub personal access token
TOKEN = None
assert TOKEN is not None, "Please fill in a Github Token. Remember not to commit and/or push this token."
output = []

g = Github(TOKEN)
for expected_group_name in expected_group_names:
    repo = g.get_repo(f"MUDE-2024/ga-2-8-{expected_group_name}")
    file_content = repo.get_contents("ticket.md", ref="main")
    data = file_content.decoded_content.decode("utf-8").split("Group:")[1]
    data = [x for x in data.split("\n") if x]
    self_reported_group_name = data[0].strip().lower()
    if self_reported_group_name != expected_group_name:
        print(f'WARNING: {self_reported_group_name} (self-reported) != {expected_group_name} (expected)')
    output.append({
        'group_name': expected_group_name,
        'month': data[1].strip(),
        'day': data[2].strip(),
        'hour': data[3].strip(),
        'minute': data[4].strip(),
        'justification': "".join(data[5:]).split("Justification:")[1].strip(),
    })

with open("../../data/output/tickets.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=output[0].keys())
    writer.writeheader()
    writer.writerows(output)
