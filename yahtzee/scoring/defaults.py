from typing import List

from . import rules as rl
from ..dice import Die

DEFAULT_UPPER_RULES: List[rl.ScoringRule] = [
    rl.MultiplesScoringRule(name="Aces (Ones)", face_value=1),
    rl.MultiplesScoringRule(name="Twos", face_value=2),
    rl.MultiplesScoringRule(name="Threes", face_value=3),
    rl.MultiplesScoringRule(name="Fours", face_value=4),
    rl.MultiplesScoringRule(name="Fives", face_value=5),
    rl.MultiplesScoringRule(name="Sixes", face_value=6),
]

_DEFAULT_YAHTZEE_RULE = rl.YahtzeeScoringRule(name="YAHTZEE (Five of a Kind)")
DEFAULT_LOWER_RULES: List[rl.ScoringRule] = [
    rl.NofKindScoringRule(name="Three of a Kind", n=3),
    rl.NofKindScoringRule(name="Four of a Kind", n=4),
    rl.FullHouseScoringRule(name="Full House (Two of a Kind and Three of a Kind)"),
    rl.SmallStraightScoringRule(name="Small Straight (Four in a Row)"),
    rl.LargeStraightScoringRule(name="Large Straight (Five in a Row)"),
    _DEFAULT_YAHTZEE_RULE,
    rl.ChanceScoringRule(name="Chance (Any Five Dice)"),
]

DEFAULT_RULES = DEFAULT_UPPER_RULES + DEFAULT_LOWER_RULES

DEFAULT_UPPER_BONUSES: List[rl.BonusRule] = [
    rl.ThresholdBonusRule(name="Upper Section Bonus", req_rules=DEFAULT_UPPER_RULES)
]

DEFAULT_YAHTZEE_BONUS = rl.YahtzeeBonusRule(
    name="Yahtzee Bonus",
    yahtzee_rule=_DEFAULT_YAHTZEE_RULE
)
DEFAULT_LOWER_BONUSES = [DEFAULT_YAHTZEE_BONUS]

DEFAULT_DICE = [Die(sides=6) for _ in range(5)]
