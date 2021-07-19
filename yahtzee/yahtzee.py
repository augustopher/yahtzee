from .scoring import defaults as df
from .scoring import rules as rl
from .scoring.scoresheet import Scoresheet
from .players import Player
from .dice import Die

from typing import List, Optional


class Game:
    """Representation of the full game."""
    def __init__(
        self,
        players: int = 1,
        dice: Optional[List[Die]] = None,
        rules: Optional[List[rl.ScoringRule]] = None,
        bonuses: Optional[List[rl.BonusRule]] = None,
        yahtzee_bonus: Optional[rl.YahtzeeBonusRule] = None
    ):
        self.dice = dice if dice else df.DEFAULT_DICE
        self.rules = rules if rules else df.DEFAULT_RULES
        self.bonuses: List[rl.BonusRule] = (
            bonuses if bonuses else df.DEFAULT_UPPER_BONUSES
        )
        self.yahtzee_bonus = (
            yahtzee_bonus if yahtzee_bonus else df.DEFAULT_YAHTZEE_BONUS
        )
        self.scoresheet = Scoresheet(
            rules=self.rules,
            bonuses=self.bonuses,
            yahtzee_bonus=self.yahtzee_bonus
        )
        self.players = [
            Player(scoresheet=self.scoresheet, dice=self.dice)
            for _ in range(players)
        ]
