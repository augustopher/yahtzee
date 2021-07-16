from yahtzee.dice import Die

import pytest

@pytest.mark.parametrize("sides", list(range(1, 11)))
def test_die_init(sides):
    """Checks that init values are set correctly."""
    die = Die(sides=sides)

    assert die.sides == sides
    assert die.faces == list(range(1, sides + 1))
    assert die.showing_face in die.faces

def test_die_roll_values():
    """Checks that roll values are valid values."""
    die = Die(sides=6)
    rolls = [die._roll_die() for _ in range(100)]
    assert all([roll in die.faces for roll in rolls])

def test_die_roll_update(monkeypatch):
    """Checks that the showing face is updated based on the roll value."""
    def mock_roll(self):
        return 2
    monkeypatch.setattr(Die, "_roll_die", mock_roll)

    die = Die(sides=6)
    die.roll()

    assert die.showing_face == 2
