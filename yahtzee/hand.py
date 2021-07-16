from .dice import Die

from typing import List, Optional

class Hand:
    """Representation of the player's hand."""
    def __init__(self, dice: Optional[List[Die]] = None):
        self.dice = dice if dice else self._create_dice()

    def _create_dice(self) -> List[Die]:
        """Generates a set of dice, using five standard 6-sided dice."""
        return [Die(sides=6) for _ in range(5)]

    def roll_dice(self, dice: List[int]) -> None:
        """Rolls the selected dice."""
        for idx in dice:
            self.dice[idx - 1].roll()
        return None
