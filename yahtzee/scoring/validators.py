from ..dice import Die, DiceList

from itertools import combinations
from collections import Counter
from typing import List, Union, Optional

def _find_matching_dice(dice: DiceList, face_value: int) -> DiceList:
    """Helper to find dice with the expected face value."""
    matching_dice: List[Optional[Die]] = [die for die in dice if die and die.showing_face == face_value]
    return matching_dice

def _validate_nofkind(dice: DiceList, n: int) -> bool:
    """Helper to check for n-of-a-kind for a given n."""
    faces = [die.showing_face for die in dice if die]
    counts = Counter(faces)
    return n in counts.values()

def _validate_full_house(dice: DiceList) -> bool:
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

def _validate_large_straight(dice: DiceList) -> bool:
    """Helper to check for a large straight
    (5 length sequence from pool of 5, in order, no missing values)."""
    faces = [die.showing_face for die in dice if die]
    return _validate_straight(faces)

def _validate_small_straight(dice: DiceList) -> bool:
    """Helper to check for a small straight
    (4 length sequence from pool of 5, in order, no missing values)."""
    # pull all combinations of 4 dice, check if any are a straight
    faces = [die.showing_face for die in dice if die]
    face_subsets = combinations(faces, len(faces) - 1)
    return any([_validate_straight(list(subset)) for subset in face_subsets])

def _find_duplicates(values: List) -> List:
    """Finds any duplicate values in a list."""
    counts = Counter(values)
    return [val for val, count in counts.items() if count > 1]
