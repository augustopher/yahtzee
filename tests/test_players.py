from yahtzee.players import Player
from yahtzee.dice import Die
from yahtzee.scoring.scoresheet import Scoresheet
import yahtzee.scoring.rules as rl


def test_hand_init_dice():
    """Checks that init values are set when dice are specified."""
    dice = [Die(4), Die(6)]
    sheet = Scoresheet(
        rules=[rl.ChanceScoringRule(name="rule1")],
        bonuses=[rl.CountBonusRule(name="bonus1")]
    )

    player = Player(scoresheet=sheet, dice=dice)

    assert len(player.dice) == 2
    assert [die.faces for die in player.dice] == [die.faces for die in dice]


def test_hand_init_no_dice_defaults():
    """Checks that init values are set when no dice are specified."""
    sheet = Scoresheet(
        rules=[rl.ChanceScoringRule(name="rule1")],
        bonuses=[rl.CountBonusRule(name="bonus1")]
    )

    player = Player(scoresheet=sheet)

    assert len(player.dice) == 5
    assert [die.faces for die in player.dice] == [list(range(1, 7)) for _ in range(5)]


def test_hand_init_no_dice():
    """Checks that init values are set when no dice are specified,
    but dice specs are specified."""
    sheet = Scoresheet(
        rules=[rl.ChanceScoringRule(name="rule1")],
        bonuses=[rl.CountBonusRule(name="bonus1")]
    )

    player = Player(scoresheet=sheet, num_dice=3, dice_sides=3)

    assert len(player.dice) == 3
    assert [die.faces for die in player.dice] == [list(range(1, 4)) for _ in range(3)]


def test_hand_roll_dice(monkeypatch):
    """Checks that rolling the dice updates the faces."""
    sheet = Scoresheet(
        rules=[rl.ChanceScoringRule(name="rule1")],
        bonuses=[rl.CountBonusRule(name="bonus1")]
    )

    player = Player(scoresheet=sheet)

    monkeypatch.setattr(Die, "_roll_die", lambda n: 2)

    player.roll_dice(dice=list(range(1, 6)))

    assert [die.showing_face for die in player.dice] == [2 for _ in range(5)]
