import csv

group_names = []
group_names.extend([f"hind{x}" for x in range(1, 17)])
group_names.extend([f"ming{x}" for x in range(1, 17)])
group_names.extend([f"riba{x}" for x in range(1, 12)])
group_names.extend([f"soga{x}" for x in range(1, 11)])

from github import Github

# Replace with your GitHub personal access token
TOKEN = None
assert TOKEN is not None, "Please fill in a Github Token. Remember not to commit and/or push this token."
output = []

g = Github(TOKEN)
for group_name in group_names:
    repo = g.get_repo(f"MUDE-2024/ga-2-8-{group_name}")
    file_content = repo.get_contents("ticket.md", ref="main")  # Adjust the path if needed
    data = file_content.decoded_content.decode("utf-8").split("Group:")[1]
    data = [x for x in data.split("\n") if x]
    group = data[0].strip().lower()
    if group != group_name:
        print(f'WARNING: {group} != {group_name}')
    output.append({
        'group_name': group_name,
        'month': data[1].strip(),
        'day': data[2].strip(),
        'hour': data[3].strip(),
        'minute': data[4].strip(),
        'justification': "".join(data[5:]).split("Justification:")[1].strip(),
    })

with open("final_grade_output/tickets.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=output[0].keys())
    writer.writeheader()
    writer.writerows(output)
