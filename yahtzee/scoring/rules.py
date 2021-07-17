from ..dice import Die
from .validators import (
    _find_matching_dice,
    _validate_nofkind,
    _validate_full_house,
    _validate_straight,
    _validate_large_straight,
    _validate_small_straight,
)

from abc import ABC, abstractmethod
from enum import Enum
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
    """Generic scoring rule."""
    def __init__(self, name: str, section: Section):
        self.name = name
        self.section = section

    @abstractmethod
    def score(self, dice: List[Die]) -> int:
        """Method to score a given set of dice."""
        pass

class PatternConstantScoringRule(ScoringRule):
    """Generic scoring rule, which looks for a particular pattern,
    and has a constant score value."""
    def __init__(self, name: str, section: Section, score_value: int = None):
        super().__init__(name=name, section=section)
        self.score_value = score_value

    def score(self, dice: List[Die]) -> int:
        """Method to score a given set of dice."""
        if self.validate(dice=dice):
            return self.score_value
        else:
            return 0

    @abstractmethod
    def validate(self, dice: List[Die]) -> bool:
        """Method to check that the desired pattern
        is present in the given dice."""
        pass

class PatternVariableScoringRule(ScoringRule):
    """Generic scoring rule, which looks for a particular pattern,
    and has a constant score value."""
    def __init__(self, name: str, section: Section):
        super().__init__(name=name, section=section)

    def score(self, dice: List[Die]) -> int:
        """Method to score a given set of dice."""
        if self.validate(dice=dice):
            return self._scoring_func(dice=dice)
        else:
            return 0

    @abstractmethod
    def _scoring_func(self, dice: List[Die]) -> int:
        """Method for calculating a dice-dependent score."""
        pass

    @abstractmethod
    def validate(self, dice: List[Die]) -> bool:
        """Method to check that the desired pattern
        is present in the given dice."""
        pass

class ChanceScoringRule(PatternVariableScoringRule):
    """Rules which take any 5 dice."""
    def __init__(self, name: str, section: Section = Section.LOWER):
        super().__init__(name=name, section=section)

    def _scoring_func(self, dice: List[Die]) -> int:
        """Method for calculating a dice-dependent score."""
        return _sum_all_showing_faces(dice=dice)

    def validate(self, dice: List[Die]) -> bool:
        """Method to check that the desired pattern
        is present in the given dice."""
        # Any dice combo is valid
        return True

class MultiplesScoringRule(PatternVariableScoringRule):
    """Rules which look for multiple dice with a specific face value."""
    def __init__(self, name: str, face_value: int, section: Section = Section.UPPER):
        super().__init__(name=name, section=section)
        self.face_value = face_value

    def _scoring_func(self, dice: List[Die]) -> int:
        """Method for calculating a dice-dependent score."""
        return _sum_matching_faces(dice=dice, face_value=self.face_value)

    def validate(self, dice: List[Die]) -> bool:
        """Method to check that the desired pattern
        is present in the given dice."""
        # Any dice combo is valid
        return True

class NofKindScoringRule(PatternVariableScoringRule):
    """Rules which look for n-of-a-kind of a face value, without explicitly
    specifying the desired face value."""
    def __init__(self, name: str, n: int, section: Section = Section.LOWER):
        super().__init__(name=name, section=section)
        self.n = n

    def _scoring_func(self, dice: List[Die]) -> int:
        """Method for calculating a dice-dependent score."""
        return _sum_all_showing_faces(dice=dice)

    def validate(self, dice: List[Die]) -> bool:
        """Method to check that the desired pattern
        is present in the given dice."""
        n_or_more_kind_present = [
            _validate_nofkind(dice=dice, n=x)
            for x in range(self.n, len(dice) + 1)
        ]
        return any(n_or_more_kind_present)

class YahtzeeScoringRule(PatternConstantScoringRule):
    """Rules which look for a Yahtzee (5-of-a-kind)."""
    def __init__(self, name: str, section: Section = Section.LOWER, score_value: int = SCORE_YAHTZEE):
        super().__init__(name=name, section=section, score_value=score_value)

    def validate(self, dice: List[Die]) -> bool:
        """Method to check that the desired pattern
        is present in the given dice."""
        return _validate_nofkind(dice=dice, n=5)

class FullHouseScoringRule(PatternConstantScoringRule):
    """Rules which look for a full house (3-of-a-kind and 2-of-a-kind)."""
    def __init__(self, name: str, section: Section = Section.LOWER, score_value: int = SCORE_FULL_HOUSE):
        super().__init__(name=name, section=section, score_value=score_value)

    def validate(self, dice: List[Die]) -> bool:
        """Method to check that a full house is present in the given dice."""
        return _validate_full_house(dice=dice)

class LargeStraightScoringRule(PatternConstantScoringRule):
    """Rules which look for a large straight (5 dice sequence)."""
    def __init__(self, name: str, section: Section = Section.LOWER, score_value: int = SCORE_LARGE_STRAIGHT):
        super().__init__(name=name, section=section, score_value=score_value)

    def validate(self, dice: List[Die]) -> bool:
        """Method to check that a full house is present in the given dice."""
        return _validate_large_straight(dice=dice)

class SmallStraightScoringRule(PatternConstantScoringRule):
    """Rules which look for a small straight (4 dice sequence)."""
    def __init__(self, name: str, section: Section = Section.LOWER, score_value: int = SCORE_SMALL_STRAIGHT):
        super().__init__(name=name, section=section, score_value=score_value)

    def validate(self, dice: List[Die]) -> bool:
        """Method to check that a full house is present in the given dice."""
        return _validate_small_straight(dice=dice)

def _sum_all_showing_faces(dice: List[Die]) -> int:
    """Sums all the showing faces for a set of dice."""
    return sum([die.showing_face for die in dice])

def _sum_matching_faces(dice: List[Die], face_value: int) -> int:
    """Sums all the showing faces which match a given value for a set of dice."""
    matching_dice = _find_matching_dice(dice=dice, face_value=face_value)
    return _sum_all_showing_faces(dice=matching_dice)
