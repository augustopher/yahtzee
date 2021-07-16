from .dice import Die

from abc import ABC, abstractmethod
from enum import Enum
from itertools import combinations
from typing import List, Optional, Union

# scores that are constant, regardless of dice values
SCORE_FULL_HOUSE: int = 25
SCORE_SMALL_STRAIGHT: int = 30
SCORE_LARGE_STRAIGHT: int = 40
SCORE_YAHTZEE: int = 50

class Section(Enum):
    UPPER: str = "upper"
    LOWER: str = "lower"

class ScoringRule(ABC):
    """Abstract class for a scoring rule."""
    @abstractmethod
    def score(self, dice: List[Die]) -> int:
        """Method to score a given set of dice."""
        pass

class ChanceScoringRule(ScoringRule):
    """Rules which take any 5 dice."""
    def __init__(self, name: str, section: Section = Section.LOWER):
        self.name = name
        self.section = section

    def score(self, dice: List[Die]) -> int:
        """Method to score a given set of dice.
        Scores as the total of all dice."""
        return sum([die.showing_face for die in dice])

class MultiplesScoringRule(ScoringRule):
    """Rules which look for multiple dice with a specific face value."""
    def __init__(self, name: str, face_value: int, section: Section = Section.UPPER):
        self.name = name
        self.face_value = face_value
        self.section = section

    def score(self, dice: List[Die]) -> int:
        """Method to score a given set of dice.
        Scores as total of dice with the matching face value."""
        matching_dice = _find_matching_dice(dice=dice, face_value=self.face_value)
        return self.face_value * len(matching_dice)

class NofKindScoringRule(ScoringRule):
    """Rules which look for n-of-a-kind of a face value, without explicitly
    specifying the desired face value."""
    def __init__(self, name: str, n: int, section: Section = Section.LOWER, override_score: Optional[int] = None):
        self.name = name
        self.n = n
        self.section = section
        self.override_score = override_score

    def score(self, dice: List[Die]) -> int:
        """Method to score a given set of dice.
        Scores as total of all dice, given that the n-of-a-kind is present.
        Allows for a custom score value to be used (i.e., Yahtzee is worth 50)."""
        # check that n-of-a-kind is present, or any n-of-a-kind larger than n
        n_or_more_kind_present = any([
            _validate_nofkind(dice=dice, n=x)
            for x in range(self.n, len(dice) + 1)
        ])
        if n_or_more_kind_present:
            if self.override_score:
                score = self.override_score
            else:
                score = sum([die.showing_face for die in dice])
        else:
            score = 0
        return score

class FullHouseScoringRule(ScoringRule):
    """Rules which look for a full house (3-of-a-kind and 2-of-a-kind)."""
    def __init__(self, name: str, section: Section = Section.LOWER, score_value: int = SCORE_FULL_HOUSE):
        self.name = name
        self.section = section
        self.score_value = score_value

    def score(self, dice: List[Die]) -> int:
        """Method to score a given set of dice.
        Scores as SCORE_FULL_HOUSE, given that a full house is present."""
        if _validate_full_house(dice=dice):
            score = self.score_value
        else:
            score = 0
        return score

class LargeStraightScoringRule(ScoringRule):
    """Rules which look for a large straight (5 dice sequence)."""
    def __init__(self, name: str, section: Section = Section.LOWER, score_value: int = SCORE_LARGE_STRAIGHT):
        self.name = name
        self.section = section
        self.score_value = score_value

    def score(self, dice: List[Die]) -> int:
        """Method to score a given set of dice.
        Scored as SCORE_LARGE_STRAIGHT, given that a large straight is present."""
        if _validate_large_straight(dice=dice):
            score = self.score_value
        else:
            score = 0
        return score

class SmallStraightScoringRule(ScoringRule):
    """Rules which look for a small straight (4 dice sequence)."""
    def __init__(self, name: str, section: Section = Section.LOWER, score_value: int = SCORE_SMALL_STRAIGHT):
        self.name = name
        self.section = section
        self.score_value = score_value

    def score(self, dice: List[Die]) -> int:
        """Method to score a given set of dice.
        Scored as SCORE_SMALL_STRAIGHT, given that a small straight is present."""
        if _validate_small_straight(dice=dice):
            score = self.score_value
        else:
            score = 0
        return score

def _find_matching_dice(dice: List[Die], face_value: int) -> List[Union[Die, None]]:
    """Helper to find dice with the expected face value."""
    matching_dice = [die for die in dice if die.showing_face == face_value]
    return matching_dice

def _validate_nofkind(dice: List[Die], n: int) -> bool:
    """Helper to check for n-of-a-kind for a given n."""
    possible_faces = dice[0].faces
    nofkind_present = []
    for face in possible_faces:
        matches = _find_matching_dice(dice=dice, face_value=face)
        nofkind = len(matches) == n
        nofkind_present.append(nofkind)
    return any(nofkind_present)

def _validate_full_house(dice: List[Die]) -> bool:
    """Helper to check for a full house (pair and triple)."""
    pair = _validate_nofkind(dice=dice, n=2)
    triple = _validate_nofkind(dice=dice, n=3)
    return pair and triple

def _validate_straight(values: List[int]) -> bool:
    """Helper to check for a straight
    (any length sequence, in order, no missing middle values)."""
    # check that the minimum and maximum ranks are spaced properly
    ranks_check = max(values) - min(values) + 1 == len(values)
    # check that all values are unique
    unique_check = len(set(values)) == len(values)
    return ranks_check and unique_check

def _validate_large_straight(dice: List[Die]) -> bool:
    """Helper to check for a large straight
    (5 length sequence from pool of 5, in order, no missing values)."""
    faces = [die.showing_face for die in dice]
    return _validate_straight(faces)

def _validate_small_straight(dice: List[Die]) -> bool:
    """Helper to check for a small straight
    (4 length sequence from pool of 5, in order, no missing values)."""
    # pull all combinations of 4 dice, check if any are a straight
    faces = [die.showing_face for die in dice]
    face_subsets = combinations(faces, len(faces) - 1)
    return any([_validate_straight(list(subset)) for subset in face_subsets])
