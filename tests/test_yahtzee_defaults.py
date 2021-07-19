from yahtzee import yahtzee as yh
from yahtzee.scoring import rules as rl


def test_default_upper_rules():
    """Check that the default upper section rules are set correctly."""
    upper_rules = yh.DEFAULT_UPPER_RULES
    expected_faces = {
        "Aces (Ones)": 1,
        "Twos": 2,
        "Threes": 3,
        "Fours": 4,
        "Fives": 5,
        "Sixes": 6,
    }
    assert len(upper_rules) == 6
    assert all([isinstance(rule, rl.MultiplesScoringRule) for rule in upper_rules])
    assert all([
        upper_rules[idx].name == name and upper_rules[idx].face_value == value
        for idx, (name, value) in enumerate(expected_faces.items())
    ])


def test_default_lower_rules():
    """Check that the default lower section rules are set correctly."""
    lower_rules = yh.DEFAULT_LOWER_RULES
    expected_types = {
        "Three of a Kind": rl.NofKindScoringRule,
        "Four of a Kind": rl.NofKindScoringRule,
        "Full House (Two of a Kind and Three of a Kind)": rl.FullHouseScoringRule,
        "Small Straight (Four in a Row)": rl.SmallStraightScoringRule,
        "Large Straight (Five in a Row)": rl.LargeStraightScoringRule,
        "YAHTZEE (Five of a Kind)": rl.YahtzeeScoringRule,
        "Chance (Any Five Dice)": rl.ChanceScoringRule,
    }
    expected_nkind = {
        "Three of a Kind": 3,
        "Four of a Kind": 4,
    }
    assert len(lower_rules) == 7
    assert all([
        lower_rules[idx].name == name and isinstance(lower_rules[idx], type)
        for idx, (name, type) in enumerate(expected_types.items())
    ])
    assert all([
        lower_rules[idx].name == name and lower_rules[idx].n == n
        for idx, (name, n) in enumerate(expected_nkind.items())
        if isinstance(lower_rules[idx], rl.NofKindScoringRule)
    ])


def test_default_rules():
    """Check that the default rules are set correctly."""
    assert all([
        rule in yh.DEFAULT_RULES for rule in yh.DEFAULT_UPPER_RULES
    ])
    assert all([
        rule in yh.DEFAULT_RULES for rule in yh.DEFAULT_LOWER_RULES
    ])


def test_default_bonuses():
    """Check that the default bonus rules are set correctly."""
    bonuses = yh.DEFAULT_BONUSES
    expected_types = {
        "Upper Section Bonus": rl.ThresholdBonusRule,
        "Yahtzee Bonus": rl.YahtzeeBonusRule,
    }
    assert len(bonuses) == 2
    assert all([
        bonuses[idx].name == name and isinstance(bonuses[idx], type)
        for idx, (name, type) in enumerate(expected_types.items())
    ])
    assert bonuses[0].req_rules == yh.DEFAULT_UPPER_RULES


def test_default_dice():
    """Check that the default dice are set correctly."""
    dice = yh.DEFAULT_DICE
    expected_faces = [1, 2, 3, 4, 5, 6]
    assert len(dice) == 5
    assert all([die.sides == 6 for die in dice])
    assert all([die.faces == expected_faces for die in dice])
