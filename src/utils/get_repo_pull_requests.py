import csv
import json
from dataclasses import dataclass

import requests

from GithubClassroom import GithubClassroom


@dataclass
class PullRequestData:
    creator: str
    pull_id: int

    def __str__(self):
        return f'{self.creator} [{self.pull_id}]'


owner = 'iceclassic'
repo = 'mude-pa-1-5'
TOKEN = None
assert TOKEN is not None, "Please fill in a Github Token. Remember not to commit and/or push this token."

gc = GithubClassroom(token=TOKEN)
data: list = gc._request_all_pages(f'/repos/{owner}/{repo}/pulls', state='all')
print(f'There were {len(data)} Pull Requests found')
accounts = [
    PullRequestData(
        creator=str(pr['user']['login']).lower(),
        pull_id=int(str(pr['url']).split('/pulls/')[1])
    )
    for pr in data if pr['merged_at'] or (pr['merged_at'] is None and pr['closed_at'] is None)
]
# find which ids were closed
ids = set([acc.pull_id for acc in accounts])
missing_ids = [i for i in range(1, accounts[0].pull_id + 1) if i not in ids]
print(f'Of those, {len(missing_ids)} PRs were closed without merging. That leaves us with {len(accounts)} PRs.')

found_accounts = set()
unique_account = []
for account in accounts:
    if account.creator not in found_accounts:
        found_accounts.add(account.creator)
        unique_account.append(account)

print(f'There were {len(accounts) - len(found_accounts)} duplicate PRs found, that leaves us with {len(unique_account)} PRs.')
with open('data/pr_accounts.txt', 'w') as outfile:
    outfile.write('\n'.join([str(acc) for acc in unique_account]))
# with open("pull_request_makers.csv", "w", newline='') as csvfile:
#     # Define the custom field name for the CSV
#     fieldname = "GithubUsername"
#     writer = csv.DictWriter(csvfile, fieldnames=[fieldname])
#
#     # Write the header
#     writer.writeheader()
#
#     # Write only the "name" field from each dataclass, with the custom column name
#     for account in unique_account:
#         writer.writerow({fieldname: account.creator})

print("Done creating CSV")