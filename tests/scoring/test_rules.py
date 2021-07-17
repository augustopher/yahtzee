import yahtzee.scoring.rules as rules
from yahtzee.dice import Die

import pytest

@pytest.mark.parametrize("seq, expected", [
    ([1,2,3,4,5], 15),
    ([1,1,3,4,5], 14),
    ([2,2,3,4,5], 16),
])
def test_score_chance_rule(seq, expected):
    dice = [Die(starting_face=s) for s in seq]
    rule = rules.ChanceScoringRule(name="name")
    result = rule.score(dice=dice)
    assert result == expected

@pytest.mark.parametrize("seq, expected", [
    ([1,1,3,4,5], 0),
    ([1,2,3,4,5], 2),
    ([2,2,3,4,5], 4),
])
def test_score_multiples_rule(seq, expected):
    dice = [Die(starting_face=s) for s in seq]
    rule = rules.MultiplesScoringRule(name="name", face_value=2)
    result = rule.score(dice=dice)
    assert result == expected

@pytest.mark.parametrize("seq, expected", [
    ([1,2,3,4,5], 0),
    ([1,1,3,4,5], 0),
    ([1,1,1,4,5], 12),
    ([1,1,1,1,5], 9),
    ([1,1,1,1,1], 5),
])
def test_score_nkind_rule(seq, expected):
    dice = [Die(starting_face=s) for s in seq]
    rule = rules.NofKindScoringRule(name="name", n=3)
    result = rule.score(dice=dice)
    assert result == expected

@pytest.mark.parametrize("seq, expected", [
    ([1,2,3,4,5], 0),
    ([1,1,3,4,5], 0),
    ([1,1,1,4,5], 0),
    ([1,1,2,2,2], 5),
])
def test_score_full_house_rule(seq, expected):
    dice = [Die(starting_face=s) for s in seq]
    rule = rules.FullHouseScoringRule(name="name", score_value = 5)
    result = rule.score(dice=dice)
    assert result == expected

@pytest.mark.parametrize("seq, expected", [
    ([1,2,3,4,5], 5),
    ([1,1,3,4,5], 0),
    ([1,1,2,3,4], 0),
])
def test_score_large_straight_rule(seq, expected):
    dice = [Die(starting_face=s) for s in seq]
    rule = rules.LargeStraightScoringRule(name="name", score_value = 5)
    result = rule.score(dice=dice)
    assert result == expected

@pytest.mark.parametrize("seq, expected", [
    ([1,2,3,4,5], 5),
    ([1,1,3,4,5], 0),
    ([1,1,2,3,4], 5),
])
def test_score_small_straight_rule(seq, expected):
    dice = [Die(starting_face=s) for s in seq]
    rule = rules.SmallStraightScoringRule(name="name", score_value = 5)
    result = rule.score(dice=dice)
    assert result == expected
