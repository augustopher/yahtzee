import yahtzee.terminal as tm

import pytest
from abc import ABC, abstractmethod


# Since these functions use `TerminalMenu`, these tests are pretty trivial.
# They mostly just check that the return values are correct.
# On my machine, using `monkeypatch.setattr` on  `TerminalMenu.show()`
# works just fine, but not so on other machines - namely, the build agent
# used in GitHub Actions.
# For now, this will at least give some testing for the module, if not much.
class MockTerminalMenu(ABC):
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def show(self):
        pass


@pytest.mark.parametrize("selected", range(3))
def test_single_choice_from_menu(monkeypatch, selected):
    """Check that a single-choice menu returns the correct value."""
    choices = ["a", "b", "c"]

    class MockTerminalMenuSingle(MockTerminalMenu):
        def show(self):
            return selected

    monkeypatch.setattr(
        "yahtzee.terminal.TerminalMenu",
        lambda *args, **kwargs: MockTerminalMenuSingle()
    )

    result = tm.single_choice_from_menu(choices=choices)

    assert result == selected


def test_mutliple_choice_from_menu(monkeypatch):
    """Check that a multi-choice menu returns the correct value."""
    choices = ["a", "b", "c"]

    selected = (0, 1)

    class MockTerminalMenuMultiple(MockTerminalMenu):
        def show(self):
            return selected

    monkeypatch.setattr(
        "yahtzee.terminal.TerminalMenu",
        lambda *args, **kwargs: MockTerminalMenuMultiple()
    )

    result = tm.mutliple_choice_from_menu(choices=choices)

    assert result == selected
