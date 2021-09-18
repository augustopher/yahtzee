from typing import List, Tuple, Optional

from simple_term_menu import TerminalMenu  # type: ignore


def single_choice_from_menu(
    choices: List[str],
    title: Optional[str] = None,
) -> int:
    """Presents the user with a menu and returns the index of the user's choice.

    Parameters
    ----------
    choices : list of str
        The choices to present to the user.
    title : str, optional
        The title to show for the menu.

    Returns
    -------
    choice : int
        The index of the selected choice.
    """
    menu = TerminalMenu(choices, title=title)
    selected: int = menu.show()

    return selected


def mutliple_choice_from_menu(
    choices: List[str],
    title: Optional[str] = None,
    cursor_end: bool = True,
) -> Tuple[int, ...]:
    """Presents the user with a menu and returns the index of the user's choices.

    Parameters
    ----------
    choices : list of str
        The choices to present to the user.
    title : str, optional
        The title to show for the menu.
    cursor_end : bool, default True
        Whether to start the cursor at the end of the list.
        Defaults to True.
        If False, the cursor will start at the beginning of the list.

    Returns
    -------
    choices : tuple of int
        The indexes of the selected choice(s).
    """
    cursor_index = len(choices) if cursor_end else 0

    menu = TerminalMenu(
        choices,
        title=title,
        multi_select=True,
        show_multi_select_hint=True,
        multi_select_select_on_accept=False,
        cursor_index=cursor_index,
    )

    selected: Tuple[int, ...] = menu.show()

    return selected
