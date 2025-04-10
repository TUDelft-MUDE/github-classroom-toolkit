import os
from functools import partial
from pathlib import Path

from InquirerPy import prompt, inquirer

from create_feedback_excel import create_feedback_excel_file
from src.github_classroom.wrapper import GithubClassroom
from src.github_classroom.state import State


def delayed_dump_get_classroom(ghc: GithubClassroom, state: State):
    json = ghc.get_classroom(state.get_classroom())
    ghc.dump('dump_get_classroom', path=get_data_path(), json_data=json)


def delayed_dump_list_assignments(ghc: GithubClassroom, state: State):
    json = ghc.list_assignments(state.get_classroom())
    ghc.dump('dump_list_assignments', path=get_data_path(), json_data=json),


def delayed_dump_get_assignment(ghc: GithubClassroom, state: State):
    json = ghc.get_assignment(choose_assignment(ghc, state.get_classroom()))
    ghc.dump('dump_get_assignment', path=get_data_path(), json_data=json),


def delayed_dump_list_accepted_assignments(ghc: GithubClassroom, state: State):
    assignment = choose_assignment(ghc, state.get_classroom())
    assignment_obj = ghc.get_assignment(assignment)
    assignment_name = assignment_obj['title']
    print(f"assgnment obj: {assignment_obj}")
    print(f'dump_{assignment_name}_accepted_assignments')
    json = ghc.list_accepted_assignments(assignment)
    ghc.dump(f'dump_{assignment_name}_accepted_assignments', path=get_data_path(), json_data=json),


def delayed_dump_list_grades(ghc: GithubClassroom, state: State):
    json = ghc.list_grades(choose_assignment(ghc, state.get_classroom()))
    ghc.dump('dump_list_grades', path=get_data_path(), json_data=json),


def delayed_create_feedback_excel(ghc: GithubClassroom, state: State):
    assignment_id = choose_assignment(ghc, state.get_classroom())
    assignment_name = ghc.get_assignment(assignment_id)['title']
    print('Downloading accepted assignments...')
    json = ghc.list_accepted_assignments(assignment_id)
    columns = get_user_list('column name')
    create_feedback_excel_file(
        json_data=json,
        assignment_name=assignment_name,
        columns=columns,
        path=get_data_path(),
    )


def get_user_list(item_name: str = 'item') -> list[str]:
    user_list = []

    while True:
        response = prompt([
            {
                'type': 'input',
                'name': 'item',
                'message': f'Enter a [{item_name}] (or type "stop" to finish):',
                'instruction': f'Current list: {user_list}'
            }
        ])

        item = response['item']
        if item.lower() == 'stop':
            break
        user_list.append(item)

    return user_list


def main_menu(ghc: GithubClassroom, state: State):
    # Create a mapping of menu choices to functions
    menu_functions = {
        "get_classroom": partial(delayed_dump_get_classroom, ghc, state),
        "list_assignments": partial(delayed_dump_list_assignments, ghc, state),
        "get_assignment": partial(delayed_dump_get_assignment, ghc, state),
        "list_accepted_assignments": partial(delayed_dump_list_accepted_assignments, ghc, state),
        "list_grades": partial(delayed_dump_list_grades, ghc, state),
        "create_feedback_excel": partial(delayed_create_feedback_excel, ghc, state),
        "Exit": exit,
    }

    # Define the menu options
    menu = [
        {"name": "Dump CSV: Get Classroom", "value": "get_classroom"},
        {"name": "Dump CSV: List Assignments", "value": "list_assignments"},
        {"name": "Dump CSV: Get Assignment", "value": "get_assignment"},
        {"name": "Dump CSV: List Accepted Assignments", "value": "list_accepted_assignments"},
        {"name": "Dump CSV: List Grades", "value": "list_grades"},
        {"name": "Create feedback excel", "value": "create_feedback_excel"},
        {"name": "Exit", "value": "Exit"}
    ]

    # Prompt the user for their selection
    response = prompt({
        "type": "list",
        "name": "menu_option",
        "message": "Select an option:",
        "choices": menu
    })

    # Get the selected menu option and call the corresponding function
    selected_option = response["menu_option"]
    menu_functions[selected_option]()  # Call the function


def choose_assignment(ghc: GithubClassroom, classroom_id: int):
    assignments = ghc.list_assignments(classroom_id=classroom_id)

    menu = []
    for assignment in assignments:
        menu.append({
            "name": assignment['title'],
            "value": assignment['id'],
        })
    menu.append({"name": "Exit", "value": "Exit"})

    # Prompt the user for their selection
    response = prompt({
        "type": "list",
        "name": "menu_option",
        "message": "Select an assignment:",
        "choices": menu,
        "instruction": "(list may continue below, so check by arrow down)"
    })

    # Get the selected menu option and call the corresponding function
    selected_option = response["menu_option"]

    if selected_option == "Exit":
        exit()
    else:
        return selected_option


def choose_class(ghc: GithubClassroom):
    classes = ghc.list_classrooms()

    menu = []
    for classroom in classes:
        menu.append({
            "name": classroom['name'],
            "value": classroom['id'],
        })
    menu.append({"name": "Exit", "value": "Exit"})

    # Prompt the user for their selection
    response = prompt({
        "type": "list",
        "name": "menu_option",
        "message": "Select a classroom:",
        "choices": menu
    })

    # Get the selected menu option and call the corresponding function
    selected_option = response["menu_option"]

    if selected_option == "Exit":
        exit()
    else:
        return selected_option


def authenticate():
    if os.path.exists(get_token_path()):
        with open(get_token_path(), "r") as token_file:
            read_token = token_file.read().strip()
            if GithubClassroom.is_valid(read_token):
                return read_token, True

    user_input_token = inquirer.secret(
        message="Fill in your GitHub Token:",
        transformer=lambda _: "[hidden]",
        validate=lambda text: GithubClassroom.is_valid(text),
        invalid_message="Token is not valid",
        # instruction="(abc)",
    ).execute()
    return user_input_token, False


def save_token(token: str) -> None:
    with open(get_token_path(), "w") as token_file:
        token_file.write(token)


def get_token_path():
    current_file_path = Path(__file__).resolve()
    current_dir = current_file_path.parent
    token_file_path = Path('.github_token')
    token_path = current_dir / token_file_path
    return token_path


def get_data_path():
    current_file_path = Path(__file__).resolve()
    current_dir = current_file_path.parent
    token_file_path = Path('data')
    token_path = current_dir / token_file_path
    return token_path


if __name__ == "__main__":
    token, token_already_saved = authenticate()
    if not token_already_saved:
        # todo ability to remove token
        wants_to_save_token = inquirer.confirm(message="Save token on local machine for later use?").execute()
        if wants_to_save_token:
            save_token(token)
    state = State(token=token)
    ghc = GithubClassroom(token=token)
    state.set_classroom(choose_class(ghc))
    while True:
        main_menu(ghc, state)
