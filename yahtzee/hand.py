from .dice import Die

from typing import List, Optional

class Hand:
    """Representation of the player's hand."""
    def __init__(self, dice: Optional[List[Die]] = None):
        self.dice = dice if dice else self._create_dice()

    def _create_dice(self) -> List[Die]:
        """Generates a set of dice."""
        return [Die() for _ in range(6)]

    def roll_dice(dice: List[int]) -> None:
        """Rolls the selected dice."""
        for idx, die in self.dice:
            if idx in dice:
                die.roll()
        return None
