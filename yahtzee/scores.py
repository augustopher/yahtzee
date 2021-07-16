from .dice import Die

from abc import ABC, abstractmethod
from typing import List, Optional

class ScoringRule(ABC):
    """Abstract class for a scoring rule."""
    @abstractmethod
    def score(self):
        """Method to score a given set of dice."""
        pass

class MultiplesScoringRule(ScoringRule):
    """Rules which look for multiple dice with a specific face value."""
    def __init__(self, name: str, section: str, face_value: int):
        self.name = name
        self.section = section
        self.face_value = face_value

    def score(self, dice: List[Die]) -> int:
        """Method to score a given set of dice.
        Scores as total of dice with the matching face value."""
        matching_dice = _find_matching_dice(dice=dice, face_value=self.face_value)
        return self.face_value * len(matching_dice)

class NofKindScoringRule(ScoringRule):
    """Rules which look for n-of-a-kind of a face value, without explicitly
    specifying the desired face value."""
    def __init__(self, name: str, section: str, n: int):
        self.name = name
        self.section = section
        self.n = n

    def score(self, dice: List[Die]) -> int:
        """Method to score a given set of dice.
        Scores as total of all dice, given that the n-of-a-kind is present."""
        if self._validate_nofkind(dice=dice):
            score = sum([die.face_value for die in Dice])
        else:
            score = 0
        return score

    def _validate_nofkind(self, dice: List[Die]) -> bool:
        """Helper to confirm that an n-of-kind is present."""
        possible_faces = dice[0].faces
        nofkind_present = []
        for face in possible_faces:
            matches = _find_matching_dice(dice=dice, face_value=face)
            nofkind = len(matches) >= self.n
            nofkind_present.append(nofkind)
        return any(nofkind_present)

def _find_matching_dice(dice: List[Die], face_value: int) -> List[Union[Die, None]]:
    """Helper to find dice with the expected face value."""
    matching_dice = [die for die in dice if die.face_value == face_value]
    return matching_dice
