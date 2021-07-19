from yahtzee.yahtzee import Game
from yahtzee.hand import Hand
from yahtzee.dice import Die
import yahtzee.scoring.rules as rl
import yahtzee.scoring.defaults as df


def test_game_init_defaults():
    """Check that Game is configured correctly with default values."""
    result = Game()
    assert len(result.players) == 1
    assert all([isinstance(p, Hand) for p in result.players])
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
    yahtzee_bonus = rl.YahtzeeBonusRule(name="rule3")

    result = Game(
        players=players,
        dice=dice,
        rules=rules,
        bonuses=bonuses,
        yahtzee_bonus=yahtzee_bonus
    )
    assert len(result.players) == 2
    assert all([isinstance(p, Hand) for p in result.players])
    assert result.dice == dice
    assert result.rules == rules
    assert result.bonuses == bonuses
    assert result.yahtzee_bonus == yahtzee_bonus
