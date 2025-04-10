class State:
    def __init__(self, token: str, classroom_id: int = None, assignment_id: int = None):
        self._token = token
        self._selected_classroom = classroom_id
        self._selected_assignment = assignment_id

    # -- classrooms
    def classroom_is_selected(self) -> bool:
        return self._selected_classroom is not None

    def get_classroom(self) -> int:
        """ returns classroom id """
        if self._selected_classroom is None:
            raise ValueError("No classroom is currently selected")
        return self._selected_classroom

    def set_classroom(self, classroom_id: int):
        self._selected_classroom = classroom_id

    def deselect_classroom(self):
        self._selected_classroom = None

    # -- assignments
    def assignment_is_selected(self) -> bool:
        return self._selected_assignment is not None

    def get_assignment(self) -> int:
        """ returns assignment id """
        if self._selected_assignment is None:
            raise ValueError("No assignment is currently selected")
        return self._selected_assignment

    def set_assignment(self, assignment_id: int):
        self._selected_assignment = assignment_id

    def deselect_assignment(self):
        self._selected_assignment = None
