from .scoring import defaults as df
from .scoring import rules as rl
from .scoring.scoresheet import Scoresheet
from .players import Player
from .dice import Die

from typing import List, Optional


class Game:
    """Representation of the full game.

    Parameters
    ----------
    players : int, default 1
        Number of players for the game.
    dice : list of Die, optional
        A set of dice to use for the game.
        If not specified, defaults to a standard set of 5 six-sided dice.
    rules : list of ScoringRule, optional
        A set of scoring rules to use in the game.
        If not specified, defaults to the usual set of Yahtzee rules:

        - Aces (Ones): sum of all 1s
        - Twos: sum of all 2s
        - Threes: sum of all 3s
        - Fours: sum of all 4s
        - Fives: sum of all 5s
        - Sixes: sum of all 6s
        - Three-of-a-Kind: total of all dice
        - Four-of-a-Kind: total of all dice
        - Full House (Two-of-a-Kind & Three-of-a-Kind): 25 points
        - Small Straight (four dice sequence): 30 points
        - Large Straight (five dice sequence): 40 points
        - Yahtzee (Five-of-a-Kind): 50 points
        - Chance (any five dice): total of all dice

    bonuses : list of BonusRule, optional
        A set of bonus rules to use in the game.
        If not specified, defaults to the usual bonus rules:

        - Upper Section Bonus: 35 points if the upper section score is at least 63

    yahtzee_bonus : YahtzeeBonusRule, optional
        A bonus rule for scoring the Yahtzee bonus in the game.
        If not specified, defaults to the usual Yahtzee bonus rule:

        - Yahtzee Bonus: 100 points per additional Yahtzee

    Attributes
    ----------
    dice : list of Die
        The dice to be rolled in the game.
    rules : list of ScoringRule
        The rules to be scored in the game.
    bonuses : list of BonusRule
        The bonus rules to be scored in the game.
    yahtzee_bonus : YahtzeeBonusRule
        The Yahtzee bonus rule to be scored in the game.
    scoresheet : Scoresheet
        The scoresheet to be used by each player, which contains the various rules
        and bonuses, along with the player's scores for those rules.
    players : list of Player
        The players in the game.
    """
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
