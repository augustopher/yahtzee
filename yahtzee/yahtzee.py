from .dice import Die
# from .hand import Hand
# from .scoring.scoresheet import Scoresheet
from .scoring import rules as rules

DEFAULT_RULES = [
    rules.MultiplesScoringRule(name="Aces (Ones)", face_value=1),
    rules.MultiplesScoringRule(name="Twos", face_value=2),
    rules.MultiplesScoringRule(name="Threes", face_value=3),
    rules.MultiplesScoringRule(name="Fours", face_value=4),
    rules.MultiplesScoringRule(name="Fives", face_value=5),
    rules.MultiplesScoringRule(name="Sixes", face_value=6),
    rules.NofKindScoringRule(name="Three of a Kind", n=3),
    rules.NofKindScoringRule(name="Four of a Kind", n=4),
    rules.FullHouseScoringRule(name="Full House"),
    rules.SmallStraightScoringRule(name="Small Straight"),
    rules.LargeStraightScoringRule(name="Large Straight"),
    rules.YahtzeeScoringRule(name="YAHTZEE"),
    rules.ChanceScoringRule(name="Chance"),
]

DEFAULT_BONUSES = [
    rules.ThresholdBonusRule(name="Upper Section Bonus"),
    rules.CountBonusRule(name="Yahtzee Bonus")
]

DEFAULT_DICE = [Die(sides=6) for _ in range(5)]
