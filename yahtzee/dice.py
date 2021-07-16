import random

class Die:
    """Representation of a n-sided die."""
    def __init__(self, sides: int = 6):
        self.sides = sides
        self.faces = list(range(1, sides + 1))
        self.showing_face = self._roll_die()

    def roll(self) -> None:
        """Rolls the die, updating the face."""
        self.showing_face = self._roll_die()
        return None

    def _roll_die(self) -> int:
        """Returns the value resulting from a die roll."""
        return random.choice(self.faces)
