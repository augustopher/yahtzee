import pytest

import yahtzee.errors as er
import yahtzee.scoring.validators as vl
from yahtzee.dice import Die


@pytest.mark.parametrize("seq, face, expected", [
    ([1, 2, 3, 4, 5], 1, 1),
    ([1, 2, 2, 3, 4], 2, 2),
])
def test_find_matching_dice(seq, face, expected):
    """Check that the correct dice are identified and returned."""
    dice = [Die(starting_face=s) for s in seq]
    result = vl.find_matching_dice(dice=dice, face_value=face)
    result_faces = [die.showing_face for die in result]
    assert len(set(result_faces)) == 1
    assert result_faces[0] == face
    assert len(result) == expected


def test_find_matching_dice_no_match():
    """Check that no dice are returned when no match is found."""
    dice = [Die(starting_face=s) for s in [1, 1, 1, 3, 3]]
    result = vl.find_matching_dice(dice=dice, face_value=2)
    assert len(result) == 0


@pytest.mark.parametrize("seq, expected", [
    ([1, 2, 3, 4, 5], True),
    ([1, 1, 3, 4, 5], False),
])
def test_validate_straight(seq, expected):
    """Check that straights are properly identified."""
    result = vl.validate_straight(values=seq)
    assert result is expected


@pytest.mark.parametrize("seq, expected", [
    ([1, 2, 3, 4, 5], True),
    ([1, 1, 3, 4, 5], False),
])
def test_validate_large_straight(seq, expected):
    """Check that large straights are properly identified."""
    dice = [Die(starting_face=s) for s in seq]
    result = vl.validate_large_straight(dice=dice)
    assert result is expected


@pytest.mark.parametrize("seq, expected", [
    ([1, 2, 3, 4, 5], True),
    ([1, 1, 2, 3, 4], True),
    ([1, 1, 2, 2, 3], False),
])
def test_validate_small_straight(seq, expected):
    """Check that small straights are properly identified."""
    dice = [Die(starting_face=s) for s in seq]
    result = vl.validate_small_straight(dice=dice)
    assert result is expected


@pytest.mark.parametrize("seq, n, expected", [
    ([1, 1, 2, 3, 4], 2, True),
    ([1, 2, 3, 4, 5], 2, False),
    ([1, 1, 3, 4, 5], 3, False),
    ([1, 1, 1, 1, 5], 4, True),
    ([1, 1, 1, 1, 5], 5, False),
])
def test_validate_nofkind(seq, n, expected):
    """Check that n-of-a-kind are properly identified."""
    dice = [Die(starting_face=s) for s in seq]
    result = vl.validate_nofkind(dice=dice, n=n)
    assert result is expected


@pytest.mark.parametrize("seq, n1, n2, expected", [
    ([1, 1, 6, 6, 6], 3, 2, True),
    ([1, 2, 3, 4, 5], 3, 2, False),
    ([1, 1, 3, 4, 5], 3, 2, False),
    ([1, 1, 1, 4, 5], 3, 2, False),
    ([1, 1, 1, 6, 6, 6, 6], 4, 3, True),
])
def test_validate_full_house(seq, n1, n2, expected):
    """Check that full houses are properly identified."""
    dice = [Die(starting_face=s) for s in seq]
    result = vl.validate_full_house(dice=dice, large_n=n1, small_n=n2)
    assert result is expected


def test_validate_full_house_error():
    """Check that invalid n values raise the appropriate error."""
    with pytest.raises(er.RuleInputValueError, match=r"A full house.*"):
        vl.validate_full_house(dice=[Die()], large_n=2, small_n=3)


@pytest.mark.parametrize("vals, expected", [
    ([1, 2, 3, 4, 5], []),
    ([1, 1, 3, 4, 5], [1]),
    ([1, 1, 2, 2, 3], [1, 2]),
    ([1, 1, 1, 1, 1], [1]),
])
def test_find_duplicates(vals, expected):
    """Check that duplicates are found properly."""
    result = vl.find_duplicates(vals)
    assert sorted(result) == sorted(expected)
