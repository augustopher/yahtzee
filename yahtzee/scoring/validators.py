from ..dice import DiceList
from .. import errors as er

from itertools import combinations
from collections import Counter
from typing import List


def find_matching_dice(dice: DiceList, face_value: int) -> DiceList:
    """Helper to find dice with the expected face value.

    Parameters
    ----------
    dice : list of Die
        Set of dice to check.
    face_value : int
        Value to check for in `dice`.

    Returns
    -------
    matching_dice : list of Die
        List of dice whose `showing_face` matched `face_value`, if any.
    """
    matching_dice: DiceList = [
        die for die in dice
        if die and die.showing_face == face_value
    ]
    return matching_dice


def validate_nofkind(dice: DiceList, n: int) -> bool:
    """Helper to check for n-of-a-kind for a given n.

    Parameters
    ----------
    dice : list of Die
        Set of dice to check.
    n : int
        What size n-of-a-kind to check for.

    Returns
    -------
    is_nofkind : bool
        Whether an n-of-a-kind (size `n`) is present in `dice`.
    """
    faces = [die.showing_face for die in dice if die]
    counts = Counter(faces)
    return n in counts.values()


def validate_full_house(dice: DiceList, large_n: int, small_n: int) -> bool:
    """Helper to check for a full house (2 n-of-a-kind, large_n > small_n).

    Parameters
    ----------
    dice : list of Die
        Set of dice to check.
    large_n : int
        What size n-of-a-kind to check for, as the larger n-of-a-kind.
    small_n : int
        What size n-of-a-kind to check for, as the smaller n-of-a-kind.

    Returns
    -------
    is_full_house : bool
        Whether a full house is present in `dice`.

    Raises
    ------
    RuleInputValueError
        If `small_n` is greater than (or equal to) `large_n`.
    """
    if small_n >= large_n:
        raise er.RuleInputValueError(
            f"A full house requires `large_n` > `small_n`. "
            f"Received large_n {large_n}, small_n {small_n}."
        )
    small_nkind = validate_nofkind(dice=dice, n=small_n)
    large_nkind = validate_nofkind(dice=dice, n=large_n)
    return small_nkind and large_nkind


def validate_straight(values: List[int]) -> bool:
    """Helper to check for a straight
    (any length sequence, in order, no missing middle values).

    Parameters
    ----------
    values : list of int
        Values to check.

    Returns
    -------
    is_straight : bool
        Whether `values` form a straight.
        All values must be in the straight, with no duplicates.
    """
    # check that the minimum and maximum ranks are spaced properly
    ranks_check = max(values) - min(values) + 1 == len(values)
    # check that all values are unique
    unique_check = len(set(values)) == len(values)
    return ranks_check and unique_check


def validate_large_straight(dice: DiceList) -> bool:
    """Helper to check for a large straight
    (5 length sequence from pool of 5, in order, no missing values).

    Parameters
    ----------
    dice : list of Die
        Set of dice to check.

    Returns
    -------
    is_large_straight : bool
        Whether `dice` form a large straight.
        All dice must be in the straight, with no duplicates.
    """
    faces = [die.showing_face for die in dice if die]
    return validate_straight(faces)


def validate_small_straight(dice: DiceList) -> bool:
    """Helper to check for a small straight
    (4 length sequence from pool of 5, in order, no missing values).

    Parameters
    ----------
    dice : list of Die
        Set of dice to check.

    Returns
    -------
    is_small_straight : bool
        Whether any combination of ``n-1`` of values in `dice` form a small straight.
        All dice in the subset must be in the straight, with no duplicates.
        The last die (not in the valid subset) may have any value.
    """
    # pull all combinations of 4 dice, check if any are a straight
    faces = [die.showing_face for die in dice if die]
    face_subsets = combinations(faces, len(faces) - 1)
    return any([validate_straight(list(subset)) for subset in face_subsets])


def find_duplicates(values: List) -> List:
    """Finds any duplicate values in a list.

    Parameters
    ----------
    values : list
        Values to check.

    Returns
    -------
    duplicates : list
        List of duplicates, if any.
    """
    counts = Counter(values)
    return [val for val, count in counts.items() if count > 1]
