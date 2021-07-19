from .dice import Die
from .scoring.scoresheet import Scoresheet

from typing import List, Optional


class Player:
    """Representation of the player."""
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
        """Generates a set of dice."""
        return [Die(sides=sides) for _ in range(num)]

    def roll_dice(self, dice: List[int]) -> None:
        """Rolls the selected dice."""
        for idx in dice:
            self.dice[idx - 1].roll()
        return None
