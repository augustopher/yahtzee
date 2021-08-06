from .dice import Die
from .scoring.scoresheet import Scoresheet

from typing import List, Optional


class Player:
    """Representation of the player.

    Parameters
    ----------
    scoresheet : Scoresheet
        A scoresheet of rules and bonuses for the player to score.
    dice : list of Die, optional
        A set of dice for the player to roll.
        If omitted, a set will be generated based on `num_dice` and `dice_sides`.
    num_dice : int, default 5
        Number of dice to generate for the player.
        Only used if `dice` is omitted.
    dice_sides : int, default 6
        Number of sides to use for the generated dice.
        Only used if `dice` is omitted.

    Attributes
    ----------
    scoresheet : Scoresheet
        The player's scoresheet, which houses rules and bonuses to be scored.
    dice : list of Die
        A set of dice to be rolled by the player,
        and used for scoring rules and bonuses.
    """
    def __init__(
        self,
        scoresheet: Scoresheet,
        dice: Optional[List[Die]] = None,
        num_dice: int = 5,
        dice_sides: int = 6
    ):
        self.scoresheet = scoresheet
        self.dice = dice if dice else self._create_dice(num=num_dice, sides=dice_sides)

    def _create_dice(self, num: int, sides: int) -> List[Die]:
        """Generates a set of dice.

        Parameters
        ----------
        num : int
            Number of dice to generate.
        sides : int
            Number of sides to create each die with.

        Returns
        -------
        dice : list of Die
            A set of dice for the player to roll.
        """
        return [Die(sides=sides) for _ in range(num)]

    def roll_dice(self, dice: List[int]) -> None:
        """Rolls the selected dice.

        Parameters
        ----------
        dice : list of int
            Indexes of which dice to roll.
        """
        for idx in dice:
            self.dice[idx].roll()
        return None

    def score_rule(self, rule_name: str) -> None:
        """Updates the score for a given rule, based on the current dice values.

        Parameters
        ----------
        rule_name : str
            Name of the rule to score.
        """
        self.scoresheet.update_score(name=rule_name, dice=self.dice)
        return None
