import os
from functools import partial
from pathlib import Path

from InquirerPy import prompt, inquirer

from state import State
from src.github_classroom.wrapper import GithubClassroom
from src.utils.create_feedback_excel import create_feedback_excel_file


def delayed_dump_get_classroom(ghc: GithubClassroom, state: State):
    json = ghc.get_classroom(state.get_classroom())
    path = get_data_path() / Path('classroom')
    ghc.dump('dump_get_classroom', path=path, json_data=json)


def delayed_dump_get_assignment(ghc: GithubClassroom, state: State):
    json = ghc.get_assignment(choose_assignment(ghc, state.get_classroom()))
    path = get_data_path() / Path('assignment')
    ghc.dump('dump_get_assignment', path=path, json_data=json),


def delayed_dump_list_assignments(ghc: GithubClassroom, state: State):
    json = ghc.list_assignments(state.get_classroom())
    path = get_data_path() / Path('assignments')
    ghc.dump('dump_list_assignments', path=path, json_data=json),


def delayed_dump_list_accepted_assignments(ghc: GithubClassroom, state: State):
    assignment = choose_assignment(ghc, state.get_classroom())
    assignment_obj = ghc.get_assignment(assignment)
    assignment_name = assignment_obj['title']
    json = ghc.list_accepted_assignments(assignment)
    path = get_data_path() / Path('accepted_assignments')
    ghc.dump(f'dump_{assignment_name}_accepted_assignments', path=path, json_data=json),


def delayed_dump_list_grades(ghc: GithubClassroom, state: State):
    json = ghc.list_grades(choose_assignment(ghc, state.get_classroom()))
    path = get_data_path() / Path('grades')
    ghc.dump('dump_list_grades', path=path, json_data=json),


def delayed_create_feedback_excel(ghc: GithubClassroom, state: State):
    assignment_id = choose_assignment(ghc, state.get_classroom())
    assignment_name = ghc.get_assignment(assignment_id)['title']
    print('Downloading accepted assignments...')
    json = ghc.list_accepted_assignments(assignment_id)
    columns = get_user_list('column name')
    create_feedback_excel_file(
        json_data=json,
        assignment_code=assignment_name,
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
        "get_assignment": partial(delayed_dump_get_assignment, ghc, state),
        "list_assignments": partial(delayed_dump_list_assignments, ghc, state),
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

    # Get the selected menu option
    selected_option = response["menu_option"]
    # and call the corresponding function
    menu_functions[selected_option]()


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

    # Get the selected menu option
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

    # Get the selected menu option
    selected_option = response["menu_option"]

    if selected_option == "Exit":
        exit()
    else:
        return selected_option


def authenticate() -> tuple[str, bool]:
    """
    Function for authentication into GitHub. First tries to find the token in a pre-defined place on the local machine.
    If we cannot find the token or cannot authenticate successfully with the token,
    we prompt the user for a (new) token. The expected location of the token
    is given by the ``get_token_path()`` function.

    :return: tuple (token, boolean), where the boolean stands for if we used a previously saved token or not
    """
    if os.path.exists(get_token_path()):
        with open(get_token_path(), "r") as token_file:
            read_token: str = token_file.read().strip()
            if GithubClassroom.is_valid(read_token):
                return read_token, True

    user_input_token = inquirer.secret(
        message="Fill in your GitHub Token:",
        transformer=lambda _: "[hidden]",
        validate=lambda text: GithubClassroom.is_valid(text),
        invalid_message="Token is not valid",
    ).execute()
    return user_input_token, False


def save_token(token: str) -> None:
    with open(get_token_path(), "w") as token_file:
        token_file.write(token)


def get_token_path() -> Path:
    """
    Returns Path to where we expect the user GitHub token to be, in a file named ``.github_token``.
    We can choose to change this function if we want to change where we save the token.
    """
    current_file_path = Path(__file__).resolve()
    root_dir = current_file_path.parent.parent.parent
    token_file_path = Path('.github_token')
    token_path = root_dir / token_file_path
    return token_path


def get_data_path() -> Path:
    """
    Returns Path to where we expect the GitHub Classroom-specific data folder to be.
    We can choose to change this if we want to change the data folder structure.
    """
    current_file_path = Path(__file__).resolve()
    root_dir = current_file_path.parent.parent.parent
    data_sub_path = Path('data/raw_data/github_classroom')
    data_path = root_dir / data_sub_path
    return data_path


if __name__ == "__main__":
    token, token_already_saved = authenticate()
    if not token_already_saved:
        # todo: (Jasper) ability to remove token?
        wants_to_save_token = inquirer.confirm(message="Save token on local machine for later use?").execute()
        if wants_to_save_token:
            save_token(token)
    state = State(token=token)
    ghc = GithubClassroom(token=token)
    state.set_classroom(choose_class(ghc))
    while True:
        main_menu(ghc, state)
