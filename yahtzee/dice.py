from . import errors as er

import random
from typing import Optional, List


class Die:
    """Representation of a n-sided die."""
    def __init__(self, sides: int = 6, starting_face: Optional[int] = None):
        self.sides = sides
        self.faces = list(range(1, sides + 1))
        self.showing_face = starting_face if starting_face else self._roll_die()

        if self.showing_face not in self.faces:
            raise er.IllegalDieValueError(
                f"Starting face {self.showing_face} is not in valid faces: "
                f"{self.faces}."
            )

    def roll(self) -> None:
        """Rolls the die, updating the showing face."""
        self.showing_face = self._roll_die()
        return None

    def _roll_die(self) -> int:
        """Returns the value resulting from a die roll."""
        return random.choice(self.faces)


DiceList = List[Optional[Die]]
