from yahtzee.players import Hand
from yahtzee.dice import Die


def test_hand_init_dice():
    """Checks that init values are set when dice are specified."""
    dice = [Die(4), Die(6)]

    hand = Hand(dice=dice)

    assert len(hand.dice) == 2
    assert [die.faces for die in hand.dice] == [die.faces for die in dice]


def test_hand_init_no_dice_defaults():
    """Checks that init values are set when no dice are specified."""
    hand = Hand()

    assert len(hand.dice) == 5
    assert [die.faces for die in hand.dice] == [list(range(1, 7)) for _ in range(5)]


def test_hand_init_no_dice():
    """Checks that init values are set when no dice are specified,
    but dice specs are specified."""
    hand = Hand(num_dice=3, dice_sides=3)

    assert len(hand.dice) == 3
    assert [die.faces for die in hand.dice] == [list(range(1, 4)) for _ in range(3)]


def test_hand_roll_dice(monkeypatch):
    """Checks that rolling the dice updates the faces."""
    hand = Hand()

    monkeypatch.setattr(Die, "_roll_die", lambda n: 2)

    hand.roll_dice(dice=list(range(1, 6)))

    assert [die.showing_face for die in hand.dice] == [2 for _ in range(5)]
