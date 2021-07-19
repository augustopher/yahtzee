from .dice import Die

from typing import List, Optional


class Hand:
    """Representation of the player's hand."""
    def __init__(
        self,
        dice: Optional[List[Die]] = None,
        num_dice: int = 5,
        dice_sides: int = 6
    ):
        self.dice = dice if dice else self._create_dice(num=num_dice, sides=dice_sides)

    def _create_dice(self, num: int, sides: int) -> List[Die]:
        """Generates a set of dice."""
        return [Die(sides=sides) for _ in range(num)]

    def roll_dice(self, dice: List[int]) -> None:
        """Rolls the selected dice."""
        for idx in dice:
            self.dice[idx - 1].roll()
        return None
