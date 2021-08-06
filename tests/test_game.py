import yahtzee.game as gm
from yahtzee.players import Player
from yahtzee.dice import Die
import yahtzee.scoring.rules as rl
import yahtzee.scoring.defaults as df

import pytest


def test_game_init_defaults():
    """Check that Game is configured correctly with default values."""
    result = gm.Game()
    assert len(result.players) == 1
    assert all([isinstance(p, Player) for p in result.players])
    assert result.dice == df.DEFAULT_DICE
    assert result.rules == df.DEFAULT_RULES
    assert result.bonuses == df.DEFAULT_UPPER_BONUSES
    assert result.yahtzee_bonus == df.DEFAULT_YAHTZEE_BONUS


def test_game_init():
    """Check that Game is configured correctly."""
    players = 2
    dice = [Die() for _ in range(3)]
    rules = [rl.ChanceScoringRule(name="rule1")]
    bonuses = [rl.ThresholdBonusRule(name="rule2")]
    yahtzee_bonus = rl.YahtzeeBonusRule(
        name="rule3",
        yahtzee_rule=rl.YahtzeeScoringRule(name="name1")
    )

    result = gm.Game(
        players=players,
        dice=dice,
        rules=rules,
        bonuses=bonuses,
        yahtzee_bonus=yahtzee_bonus
    )
    assert len(result.players) == 2
    assert all([isinstance(p, Player) for p in result.players])
    assert result.dice == dice
    assert result.rules == rules
    assert result.bonuses == bonuses
    assert result.yahtzee_bonus == yahtzee_bonus


@pytest.mark.parametrize("choices, expected", [
    ([2], [1, 2, 2]),
    ([3], [1, 2, 3]),
    ([0, 2], [2, 2, 2]),
])
def test_reroll_dice(monkeypatch, choices, expected):
    """Check that the correct dice are rolled for the correct player."""
    starting_faces = [1, 2, 3]
    dice = [Die(sides=6, starting_face=i) for i in starting_faces]
    game = gm.Game(players=2, dice=dice)

    monkeypatch.setattr("yahtzee.dice.Die._roll_die", lambda self: 2)
    monkeypatch.setattr("yahtzee.game._pick_reroll_dice", lambda dice: choices)
    game.reroll_dice(player=game.players[0])

    # check that player 1's dice have been rolled
    assert [die.showing_face for die in game.players[0].dice] == expected
    # check that player 2's dice have not been rolled
    assert [die.showing_face for die in game.players[1].dice] == starting_faces


def test_game_score_rule(monkeypatch):
    """Check the correct rule is scored for the correct player."""
    rules = [rl.ChanceScoringRule(name="name1"), rl.ChanceScoringRule(name="name2")]
    game = gm.Game(players=2, rules=rules)

    monkeypatch.setattr("yahtzee.game._pick_rule_to_score", lambda rules, dice: "name1")

    game.score_rule(player=game.players[0])

    assert game.players[0].scoresheet.rules[0].rule_score > 0
    assert game.players[0].scoresheet.rules[1].rule_score is None
    assert all([
        rule.rule_score is None
        for rule in game.players[1].scoresheet.rules
    ])


@pytest.mark.parametrize("selected", [
    (1,),
    (2,),
    (3,),
    (1, 2),
    (1, 3),
    (2, 3),
    (1, 2, 3),
    (4,),
])
def test_pick_reroll_dice(monkeypatch, selected):
    """Check that dice are selected correctly."""
    dice = [Die() for _ in range(3)]

    # Mocking TerminalMenu reduces the usefulness of this test,
    # but just mocking TermainalMenu.show() fails on some systems
    # because of errors thrown during TermainalMenu.__init__().
    # Not sure of the exact cause, and I can get the mocked
    # TerminalMenu.show() to work fine on my system, but this
    # at least tests the conversion from the TerminalMenu.show()
    # output tuple to the desired list, if nothing else.
    class MockTerminalMenu:
        def __init__(self, *args, **kwargs):
            pass

        def show(self):
            return selected

    monkeypatch.setattr(
        "yahtzee.game.TerminalMenu",
        lambda *args, **kwargs: MockTerminalMenu()
    )
    result = gm._pick_reroll_dice(dice=dice)

    assert sorted(result) == sorted(list(selected))


@pytest.mark.parametrize("selected", range(3))
def test_pick_rule_to_score(monkeypatch, selected):
    """Check that rules are selected correctly from user input."""
    rules = [
        rl.ChanceScoringRule(name="rule1"),
        rl.ChanceScoringRule(name="rule2"),
        rl.ChanceScoringRule(name="rule3"),
    ]

    dice = [Die() for _ in range(5)]

    # Mocking TerminalMenu reduces the usefulness of this test,
    # but just mocking TermainalMenu.show() fails on some systems
    # because of errors thrown during TermainalMenu.__init__().
    # Not sure of the exact cause, and I can get the mocked
    # TerminalMenu.show() to work fine on my system, but this
    # at least tests the conversion from the TerminalMenu.show()
    # output tuple to the desired list, if nothing else.
    class MockTerminalMenu:
        def __init__(self, *args, **kwargs):
            pass

        def show(self):
            return selected

    monkeypatch.setattr(
        "yahtzee.game.TerminalMenu",
        lambda *args, **kwargs: MockTerminalMenu()
    )
    result = gm._pick_rule_to_score(rules=rules, dice=dice)

    assert result == rules[selected].name
