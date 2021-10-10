import random
from typing import Optional
from typing import Sequence

from . import errors as er


class Die:
    """Representation of a n-sided die.

    Parameters
    ----------
    sides : int, default 6
        Number of sides the die should have.
        This will set `faces` as [1, ..., n].
    starting_face : int, optional
        Face value of the initial showing face of the die.
        Defaults to a random values from `faces`.

    Attributes
    ----------
    sides : int
        Number of sides on the die.
    faces : list of int
        Face values on the die.
    showing_face : int
        The showing face of the die.
        The value that is used when the die is scored.

    Raises
    ------
    IllegalDieValueError
        If `starting_face` is not in `faces`.
    """
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

    def _roll_die(self) -> int:
        """
        Returns the value resulting from a die roll.

        Returns
        -------
        int
            Showing face value resulting from the roll.
        """
        return random.choice(self.faces)


DiceList = Sequence[Optional[Die]]
