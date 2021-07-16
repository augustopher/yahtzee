from yahtzee.dice import Die

import pytest

def test_die_init():
    die = Die(sides=2)

    assert die.sides == 2
    assert die.faces == [1, 2]
    assert die.showing_face in die.faces

def test_die_roll_values():
    die = Die(sides=6)
    rolls = [die._roll_die() for _ in range(100)]
    assert all([roll in die.faces for roll in rolls])

def test_die_roll_update(monkeypatch):
    def mock_roll(self):
        return 2
    monkeypatch.setattr(Die, "_roll_die", mock_roll)

    die = Die(sides=6)
    die.roll()

    assert die.showing_face == 2
