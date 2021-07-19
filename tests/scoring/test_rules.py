import yahtzee.scoring.rules as rules
from yahtzee.dice import Die

import pytest


@pytest.mark.parametrize("seq, expected", [
    ([1, 2, 3, 4, 5], 15),
    ([1, 1, 3, 4, 5], 14),
    ([2, 2, 3, 4, 5], 16),
])
def test_score_chance_rule(seq, expected):
    """Check that Chance rules score correctly."""
    dice = [Die(starting_face=s) for s in seq]
    rule = rules.ChanceScoringRule(name="name")
    result = rule.score(dice=dice)
    assert result == expected


@pytest.mark.parametrize("seq, expected", [
    ([1, 1, 3, 4, 5], 0),
    ([1, 2, 3, 4, 5], 2),
    ([2, 2, 3, 4, 5], 4),
])
def test_score_multiples_rule(seq, expected):
    """Check that Multiples rules score correctly."""
    dice = [Die(starting_face=s) for s in seq]
    rule = rules.MultiplesScoringRule(name="name", face_value=2)
    result = rule.score(dice=dice)
    assert result == expected


@pytest.mark.parametrize("seq, expected", [
    ([1, 2, 3, 4, 5], 0),
    ([1, 1, 3, 4, 5], 0),
    ([1, 1, 1, 4, 5], 12),
    ([1, 1, 1, 1, 5], 9),
    ([1, 1, 1, 1, 1], 5),
])
def test_score_nkind_rule(seq, expected):
    """Check that N-of-a-Kind rules score correctly."""
    dice = [Die(starting_face=s) for s in seq]
    rule = rules.NofKindScoringRule(name="name", n=3)
    result = rule.score(dice=dice)
    assert result == expected


@pytest.mark.parametrize("seq, expected", [
    ([1, 2, 3, 4, 5], 0),
    ([1, 1, 3, 4, 5], 0),
    ([1, 1, 1, 4, 5], 0),
    ([1, 1, 1, 1, 5], 0),
    ([1, 1, 1, 1, 1], 5),
])
def test_score_yahtzee_rule(seq, expected):
    """Check that Yahtzee rules score correctly."""
    dice = [Die(starting_face=s) for s in seq]
    rule = rules.YahtzeeScoringRule(name="name", score_value=5)
    result = rule.score(dice=dice)
    assert result == expected


@pytest.mark.parametrize("seq, expected", [
    ([1, 2, 3, 4, 5], 0),
    ([1, 1, 3, 4, 5], 0),
    ([1, 1, 1, 4, 5], 0),
    ([1, 1, 2, 2, 2], 5),
])
def test_score_full_house_rule(seq, expected):
    """Check that Full House rules score correctly."""
    dice = [Die(starting_face=s) for s in seq]
    rule = rules.FullHouseScoringRule(name="name", score_value=5)
    result = rule.score(dice=dice)
    assert result == expected


@pytest.mark.parametrize("seq, expected", [
    ([1, 2, 3, 4, 5], 5),
    ([1, 1, 3, 4, 5], 0),
    ([1, 1, 2, 3, 4], 0),
])
def test_score_large_straight_rule(seq, expected):
    """Check that Large Straight rules score correctly."""
    dice = [Die(starting_face=s) for s in seq]
    rule = rules.LargeStraightScoringRule(name="name", score_value=5)
    result = rule.score(dice=dice)
    assert result == expected


@pytest.mark.parametrize("seq, expected", [
    ([1, 2, 3, 4, 5], 5),
    ([1, 1, 3, 4, 5], 0),
    ([1, 1, 2, 3, 4], 5),
])
def test_score_small_straight_rule(seq, expected):
    """Check that Small Straight rules score correctly."""
    dice = [Die(starting_face=s) for s in seq]
    rule = rules.SmallStraightScoringRule(name="name", score_value=5)
    result = rule.score(dice=dice)
    assert result == expected


@pytest.mark.parametrize("seq, expected", [
    ([1, 2, 3, 4, 5], 15),
    ([1, 1, 3, 4, 5], 14),
    ([1, 1, 1, 4, 5], 12),
])
def test_sum_all_showing_faces(seq, expected):
    """Check that showing faces are summed correctly."""
    dice = [Die(starting_face=s) for s in seq]
    result = rules._sum_all_showing_faces(dice=dice)
    assert result == expected


@pytest.mark.parametrize("seq, face, expected", [
    ([1, 1, 2, 2, 2], 1, 2),
    ([1, 1, 2, 2, 2], 2, 6),
    ([1, 1, 2, 2, 2], 3, 0),
])
def test_sum_matching_faces(seq, face, expected):
    """Check that matching showing faces are summed correctly."""
    dice = [Die(starting_face=s) for s in seq]
    result = rules._sum_matching_faces(dice=dice, face_value=face)
    assert result == expected


@pytest.mark.parametrize("count, threshold, bonus, expected", [
    (5, 10, 20, 0),
    (10, 10, 20, 20),
    (15, 10, 20, 20),
])
def test_score_threshold_bonus_rule(count, threshold, bonus, expected):
    """Check that threshold-based bonus rules score correctly."""
    rule = rules.ThresholdBonusRule(name="name", threshold=threshold, bonus_value=bonus)
    result = rule.score(count=count)
    assert result == expected


@pytest.mark.parametrize("amount", range(11))
def test_increment_threshold_bonus_rule(amount):
    """Check that threshold-based rules increment correctly."""
    rule = rules.ThresholdBonusRule(name="name", threshold=10, bonus_value=20)
    rule.increment(amt=amount)
    assert rule.counter == amount


@pytest.mark.parametrize("count, bonus, expected", [
    (0, 5, 0),
    (1, 5, 5),
    (20, 5, 100),
])
def test_score_count_bonus_rule(count, bonus, expected):
    """Check that count-based bonus rules are scored correctly."""
    rule = rules.CountBonusRule(name="name", bonus_value=bonus)
    result = rule.score(count=count)
    assert result == expected


@pytest.mark.parametrize("amount", range(11))
def test_increment_count_bonus_rule(amount):
    """Check that count-based rules increment correctly."""
    rule = rules.CountBonusRule(name="name", bonus_value=20)
    rule.increment(amt=amount)
    assert rule.counter == amount
