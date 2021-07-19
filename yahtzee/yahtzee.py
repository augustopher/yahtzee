from .dice import Die
# from .hand import Hand
# from .scoring.scoresheet import Scoresheet
from .scoring import rules as rules

from typing import List


DEFAULT_UPPER_RULES: List[rules.ScoringRule] = [
    rules.MultiplesScoringRule(name="Aces (Ones)", face_value=1),
    rules.MultiplesScoringRule(name="Twos", face_value=2),
    rules.MultiplesScoringRule(name="Threes", face_value=3),
    rules.MultiplesScoringRule(name="Fours", face_value=4),
    rules.MultiplesScoringRule(name="Fives", face_value=5),
    rules.MultiplesScoringRule(name="Sixes", face_value=6),
]

DEFAULT_LOWER_RULES: List[rules.ScoringRule] = [
    rules.NofKindScoringRule(name="Three of a Kind", n=3),
    rules.NofKindScoringRule(name="Four of a Kind", n=4),
    rules.FullHouseScoringRule(name="Full House (Two of a Kind and Three of a Kind)"),
    rules.SmallStraightScoringRule(name="Small Straight (Four in a Row)"),
    rules.LargeStraightScoringRule(name="Large Straight (Five in a Row)"),
    rules.YahtzeeScoringRule(name="YAHTZEE (Five of a Kind)"),
    rules.ChanceScoringRule(name="Chance (Any Five Dice)"),
]

DEFAULT_RULES = DEFAULT_UPPER_RULES + DEFAULT_LOWER_RULES

DEFAULT_UPPER_BONUSES = [
    rules.ThresholdBonusRule(name="Upper Section Bonus", req_rules=DEFAULT_UPPER_RULES)
]

DEFAULT_YAHTZEE_BONUS = rules.YahtzeeBonusRule(name="Yahtzee Bonus")
DEFAULT_LOWER_BONUSES = [DEFAULT_YAHTZEE_BONUS]

DEFAULT_DICE = [Die(sides=6) for _ in range(5)]
