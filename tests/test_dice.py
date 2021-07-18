from yahtzee.dice import Die, IllegalDieValueError

import pytest


@pytest.mark.parametrize("sides", list(range(1, 11)))
def test_die_init(sides):
    """Checks that init values are set correctly."""
    die = Die(sides=sides)

    assert die.sides == sides
    assert die.faces == list(range(1, sides + 1))
    assert die.showing_face in die.faces


@pytest.mark.parametrize("sides", list(range(1, 11)))
def test_die_init_set_face(sides):
    """Checks that init values are set correctly
    when the starting face is specified."""
    die = Die(sides=sides, starting_face=1)

    assert die.sides == sides
    assert die.faces == list(range(1, sides + 1))
    assert die.showing_face == 1


def test_die_init_starting_face_error():
    """Checks that illegal starting faces raise the appropriate error."""
    with pytest.raises(IllegalDieValueError, match=r"Starting face.*"):
        Die(sides=6, starting_face=7)


def test_die_roll_values():
    """Checks that roll values are valid values."""
    die = Die(sides=6)
    rolls = [die._roll_die() for _ in range(100)]

    assert all([roll in die.faces for roll in rolls])


def test_die_roll_update(monkeypatch):
    """Checks that the showing face is updated based on the roll value."""
    die = Die(sides=6, starting_face=1)
    monkeypatch.setattr(Die, "_roll_die", lambda x: 2)
    die.roll()

    assert die.showing_face == 2
