# github-classroom-toolkit


finally upload grade json to brightspace. if brightspace grades are created in the correct way, this will import all grades correctly.
if cli:

if scripts:
1. download accepted students (or student grades) json from github classroom or buddycheck csv from brightspace
2. run scripts for GA (..), PA (..) or BC (..)
3. upload 

warning: as of xxx/xx/2025 it seems grade file sometimes does not correspond to passing... ?

#### github classroom
The Github Classroom API only has 6 endpoints:
Listing Classrooms for a user, retrieving data for a single Classroom, retrieving a list of assignments for a classroom,
retrieving data for a single assignment, retrieving accepted assignments for an assignment 
and retrieving grades for an assignment.
The assignment grades endpoint returns a list of JSON objects. For example:
```json
{
        "assignment_name": "GA_2_8",
        "assignment_url": "https://classroom.github.com/classrooms/181358687-mude-2024-classroom/assignments/ga-2-8",
        "starter_code_url": "https://api.github.com/repos/MUDE-2024/mude-2024-classroom-ga_2_8-GA2.8",
        "github_username": "<...>",
        "roster_identifier": "",
        "student_repository_name": "ga-2-8-zeachers2",
        "student_repository_url": "https://github.com/MUDE-2024/ga-2-8-zeachers2",
        "submission_timestamp": "",
        "points_awarded": "0",
        "points_available": "0",
        "group_name": "ZEACHERS2"
    }
```
The accepted assignments endpoint also returns a list of JSON objects. For example:

```json
{
        "id": 17749957,
        "submitted": false,
        "passing": false,
        "commit_count": 0,
        "grade": null,
        "students": [
            {
                "id": 1234567,
                "login": "<...>",
                "name": "<...>",
                "avatar_url": "<...>",
                "html_url": "<...>"
            }
        ],
        "assignment": {
            "id": 738829,
            "public_repo": false,
            "title": "GA_2_8",
            "type": "group",
            "invite_link": "https://classroom.github.com/a/mZzvfEsU",
            "invitations_enabled": false,
            "slug": "ga-2-8",
            "students_are_repo_admins": false,
            "feedback_pull_requests_enabled": false,
            "max_teams": null,
            "max_members": null,
            "editor": null,
            "accepted": 54,
            "submissions": 53,
            "passing": 0,
            "language": null,
            "deadline": "2025-01-28T13:44:00Z",
            "classroom": {
                "id": 234373,
                "name": "MUDE-2024-classroom",
                "archived": false,
                "url": "https://classroom.github.com/classrooms/181358687-mude-2024-classroom"
            }
        },
        "repository": {
            "id": 918046619,
            "name": "ga-2-8-zeachers2",
            "full_name": "MUDE-2024/ga-2-8-zeachers2",
            "html_url": "https://github.com/MUDE-2024/ga-2-8-zeachers2",
            "node_id": "R_kgDONrhHmw",
            "private": true,
            "default_branch": "main"
        }
    }
```

Both seem to allow checking for passing of students; `[points_awarded]` being 0 or 10 for grades and `passing` being true.
But, as of my (Jasper) january 2025 testing - the grades endpoint seem to be wrong in  a small amount of cases. 
(TODO: Write a test for this?) This is why I use accepted assignments for the passing check.

- general remarks (api errors out alot, accepted assignments > )
#### start of the course workflow
- classlist deep dive + assumed structure
- first create grades on brightspace in a certain format. see brightspace section
  and get classlist file from brightspace and edit it in a certain way (most importantly: get the github usernames)
#### grading during the course
then either use CLI or run scripts to get raw json, summaries and grade files.
for buddycheck: download csv from brightspace
#### end of the course workflow

### brightspace
- brightspace grades structure:
---

-
- downloading classlist from brightspace
- downloading buddy check results from brightspace
- brightspace grades importing workflow
- brightspace grades remarks: naming, grading and csv structure 
- see also brightspace official documentation


#### running CLI
run cli from root directory with either

```
py -m src.cli.app
```
or
```
python -m src.cli.app
```

#### future work