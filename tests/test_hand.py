from yahtzee.hand import Hand
from yahtzee.dice import Die

import pytest

def test_hand_init_dice():
    """Checks that init values are set when dice are specified."""
    dice = [Die(4), Die(6)]

    hand = Hand(dice=dice)

    assert len(hand.dice) == 2
    assert [die.faces for die in hand.dice] == [die.faces for die in dice]

def test_hand_init_no_dice():
    """Checks that init values are set when no dice are specified."""
    hand = Hand()

    assert len(hand.dice) == 6
    assert [die.faces for die in hand.dice] == [list(range(1, 7)) for _ in range(6)]
