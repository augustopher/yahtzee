import yahtzee.scoring.rules as rl
from yahtzee.dice import Die

import pytest


@pytest.mark.parametrize("seq, expected", [
    ([1, 2, 3, 4, 5], 15),
    ([1, 1, 3, 4, 5], 14),
    ([2, 2, 3, 4, 5], 16),
])
def test_score_dice_chance_rule(seq, expected):
    """Check that Chance rules score correctly."""
    dice = [Die(starting_face=s) for s in seq]
    rule = rl.ChanceScoringRule(name="name")
    result = rule._score_dice(dice=dice)
    assert result == expected


@pytest.mark.parametrize("seq, expected", [
    ([1, 2, 3, 4, 5], 15),
    ([1, 1, 3, 4, 5], 14),
    ([2, 2, 3, 4, 5], 16),
])
def test_score_chance_rule(seq, expected):
    """Check that Chance rules update the score correctly."""
    dice = [Die(starting_face=s) for s in seq]
    rule = rl.ChanceScoringRule(name="name")
    rule.score(dice=dice)
    assert rule.rule_score == expected


@pytest.mark.parametrize("seq, expected", [
    ([1, 1, 3, 4, 5], 0),
    ([1, 2, 3, 4, 5], 2),
    ([2, 2, 3, 4, 5], 4),
])
def test_score_dice_multiples_rule(seq, expected):
    """Check that Multiples rules score correctly."""
    dice = [Die(starting_face=s) for s in seq]
    rule = rl.MultiplesScoringRule(name="name", face_value=2)
    result = rule._score_dice(dice=dice)
    assert result == expected


@pytest.mark.parametrize("seq, expected", [
    ([1, 1, 3, 4, 5], 0),
    ([1, 2, 3, 4, 5], 2),
    ([2, 2, 3, 4, 5], 4),
])
def test_score_multiples_rule(seq, expected):
    """Check that Multiples rules update the score correctly."""
    dice = [Die(starting_face=s) for s in seq]
    rule = rl.MultiplesScoringRule(name="name", face_value=2)
    rule.score(dice=dice)
    assert rule.rule_score == expected


@pytest.mark.parametrize("seq, expected", [
    ([1, 2, 3, 4, 5], 0),
    ([1, 1, 3, 4, 5], 0),
    ([1, 1, 1, 4, 5], 12),
    ([1, 1, 1, 1, 5], 9),
    ([1, 1, 1, 1, 1], 5),
])
def test_score_dice_nkind_rule(seq, expected):
    """Check that N-of-a-Kind rules score correctly."""
    dice = [Die(starting_face=s) for s in seq]
    rule = rl.NofKindScoringRule(name="name", n=3)
    result = rule._score_dice(dice=dice)
    assert result == expected


@pytest.mark.parametrize("seq, expected", [
    ([1, 2, 3, 4, 5], 0),
    ([1, 1, 3, 4, 5], 0),
    ([1, 1, 1, 4, 5], 12),
    ([1, 1, 1, 1, 5], 9),
    ([1, 1, 1, 1, 1], 5),
])
def test_score_nkind_rule(seq, expected):
    """Check that N-of-a-Kind rules update the score correctly."""
    dice = [Die(starting_face=s) for s in seq]
    rule = rl.NofKindScoringRule(name="name", n=3)
    rule.score(dice=dice)
    assert rule.rule_score == expected


@pytest.mark.parametrize("seq, expected", [
    ([1, 2, 3, 4, 5], 0),
    ([1, 1, 3, 4, 5], 0),
    ([1, 1, 1, 4, 5], 0),
    ([1, 1, 1, 1, 5], 0),
    ([1, 1, 1, 1, 1], 5),
])
def test_score_dice_yahtzee_rule(seq, expected):
    """Check that Yahtzee rules score correctly."""
    dice = [Die(starting_face=s) for s in seq]
    rule = rl.YahtzeeScoringRule(name="name", score_value=5)
    result = rule._score_dice(dice=dice)
    assert result == expected


@pytest.mark.parametrize("seq, expected", [
    ([1, 2, 3, 4, 5], 0),
    ([1, 1, 3, 4, 5], 0),
    ([1, 1, 1, 4, 5], 0),
    ([1, 1, 1, 1, 5], 0),
    ([1, 1, 1, 1, 1], 5),
])
def test_score_yahtzee_rule(seq, expected):
    """Check that Yahtzee rules update the score correctly."""
    dice = [Die(starting_face=s) for s in seq]
    rule = rl.YahtzeeScoringRule(name="name", score_value=5)
    rule.score(dice=dice)
    assert rule.rule_score == expected


@pytest.mark.parametrize("seq, expected", [
    ([1, 2, 3, 4, 5], 0),
    ([1, 1, 3, 4, 5], 0),
    ([1, 1, 1, 4, 5], 0),
    ([1, 1, 2, 2, 2], 5),
])
def test_score_dice_full_house_rule(seq, expected):
    """Check that Full House rules score correctly."""
    dice = [Die(starting_face=s) for s in seq]
    rule = rl.FullHouseScoringRule(name="name", score_value=5)
    result = rule._score_dice(dice=dice)
    assert result == expected


@pytest.mark.parametrize("seq, expected", [
    ([1, 2, 3, 4, 5], 0),
    ([1, 1, 3, 4, 5], 0),
    ([1, 1, 1, 4, 5], 0),
    ([1, 1, 2, 2, 2], 5),
])
def test_score_full_house_rule(seq, expected):
    """Check that Full House rules update the score correctly."""
    dice = [Die(starting_face=s) for s in seq]
    rule = rl.FullHouseScoringRule(name="name", score_value=5)
    rule.score(dice=dice)
    assert rule.rule_score == expected


@pytest.mark.parametrize("seq, expected", [
    ([1, 2, 3, 4, 5], 5),
    ([1, 1, 3, 4, 5], 0),
    ([1, 1, 2, 3, 4], 0),
])
def test_score_dice_large_straight_rule(seq, expected):
    """Check that Large Straight rules score correctly."""
    dice = [Die(starting_face=s) for s in seq]
    rule = rl.LargeStraightScoringRule(name="name", score_value=5)
    result = rule._score_dice(dice=dice)
    assert result == expected


@pytest.mark.parametrize("seq, expected", [
    ([1, 2, 3, 4, 5], 5),
    ([1, 1, 3, 4, 5], 0),
    ([1, 1, 2, 3, 4], 0),
])
def test_score_large_straight_rule(seq, expected):
    """Check that Large Straight rules update the score correctly."""
    dice = [Die(starting_face=s) for s in seq]
    rule = rl.LargeStraightScoringRule(name="name", score_value=5)
    rule.score(dice=dice)
    assert rule.rule_score == expected


@pytest.mark.parametrize("seq, expected", [
    ([1, 2, 3, 4, 5], 5),
    ([1, 1, 3, 4, 5], 0),
    ([1, 1, 2, 3, 4], 5),
])
def test_score_dice_small_straight_rule(seq, expected):
    """Check that Small Straight rules score correctly."""
    dice = [Die(starting_face=s) for s in seq]
    rule = rl.SmallStraightScoringRule(name="name", score_value=5)
    result = rule._score_dice(dice=dice)
    assert result == expected


@pytest.mark.parametrize("seq, expected", [
    ([1, 2, 3, 4, 5], 5),
    ([1, 1, 3, 4, 5], 0),
    ([1, 1, 2, 3, 4], 5),
])
def test_score_small_straight_rule(seq, expected):
    """Check that Small Straight rules update the score correctly."""
    dice = [Die(starting_face=s) for s in seq]
    rule = rl.SmallStraightScoringRule(name="name", score_value=5)
    rule.score(dice=dice)
    assert rule.rule_score == expected


@pytest.mark.parametrize("seq, expected", [
    ([1, 2, 3, 4, 5], 15),
    ([1, 1, 3, 4, 5], 14),
    ([1, 1, 1, 4, 5], 12),
])
def test_sum_all_showing_faces(seq, expected):
    """Check that showing faces are summed correctly."""
    dice = [Die(starting_face=s) for s in seq]
    result = rl._sum_all_showing_faces(dice=dice)
    assert result == expected


@pytest.mark.parametrize("rule", [
    rl.ChanceScoringRule(name="name"),
    rl.MultiplesScoringRule(name="name", face_value=1),
    rl.NofKindScoringRule(name="name", n=3),
    rl.YahtzeeScoringRule(name="name"),
    rl.FullHouseScoringRule(name="name"),
    rl.LargeStraightScoringRule(name="name"),
    rl.SmallStraightScoringRule(name="name"),
])
def test_scoring_rules_already_scored_error(rule):
    """Check that trying to update an already-score rule
    raises the appropriate error."""
    dice = [Die(sides=6) for _ in range(5)]
    rule.score(dice=dice)
    with pytest.raises(rl.RuleAlreadyScoredError, match=r"Rule.*"):
        rule.score(dice=dice)


@pytest.mark.parametrize("seq, face, expected", [
    ([1, 1, 2, 2, 2], 1, 2),
    ([1, 1, 2, 2, 2], 2, 6),
    ([1, 1, 2, 2, 2], 3, 0),
])
def test_sum_matching_faces(seq, face, expected):
    """Check that matching showing faces are summed correctly."""
    dice = [Die(starting_face=s) for s in seq]
    result = rl._sum_matching_faces(dice=dice, face_value=face)
    assert result == expected


@pytest.mark.parametrize("count, threshold, bonus, expected", [
    (5, 10, 20, 0),
    (10, 10, 20, 20),
    (15, 10, 20, 20),
])
def test_score_bonus_threshold_bonus_rule(count, threshold, bonus, expected):
    """Check that threshold-based bonus rules score correctly."""
    rule = rl.ThresholdBonusRule(name="name", threshold=threshold, bonus_value=bonus)
    rule.increment(amt=count)
    result = rule._score_bonus()
    assert result == expected


@pytest.mark.parametrize("count, threshold, bonus, expected", [
    (5, 10, 20, 0),
    (10, 10, 20, 20),
    (15, 10, 20, 20),
])
def test_score_threshold_bonus_rule(count, threshold, bonus, expected):
    """Check that threshold-based bonus rules score correctly."""
    rule = rl.ThresholdBonusRule(name="name", threshold=threshold, bonus_value=bonus)
    rule.increment(amt=count)
    rule.score()
    assert rule.rule_score == expected


@pytest.mark.parametrize("amount", range(11))
def test_increment_threshold_bonus_rule(amount):
    """Check that threshold-based rules increment correctly."""
    rule = rl.ThresholdBonusRule(name="name", threshold=10, bonus_value=20)
    rule.increment(amt=amount)
    assert rule.counter == amount


@pytest.mark.parametrize("count, bonus, expected", [
    (0, 5, 0),
    (1, 5, 5),
    (20, 5, 100),
])
def test_score_bonus_count_bonus_rule(count, bonus, expected):
    """Check that count-based bonus rules are scored correctly."""
    rule = rl.CountBonusRule(name="name", bonus_value=bonus)
    rule.increment(amt=count)
    result = rule._score_bonus()
    assert result == expected


@pytest.mark.parametrize("count, bonus, expected", [
    (0, 5, 0),
    (1, 5, 5),
    (20, 5, 100),
])
def test_score_count_bonus_rule(count, bonus, expected):
    """Check that count-based bonus rules are scored correctly."""
    rule = rl.CountBonusRule(name="name", bonus_value=bonus)
    rule.increment(amt=count)
    rule.score()
    assert rule.rule_score == expected


@pytest.mark.parametrize("amount", range(11))
def test_increment_count_bonus_rule(amount):
    """Check that count-based rules increment correctly."""
    rule = rl.CountBonusRule(name="name", bonus_value=20)
    rule.increment(amt=amount)
    assert rule.counter == amount


@pytest.mark.parametrize("count, bonus, expected", [
    (0, 5, 0),
    (1, 5, 5),
    (20, 5, 100),
])
def test_score_bonus_yahtzee_bonus_rule(count, bonus, expected):
    """Check that yahtzee count-based rules are scored correctly."""
    rule = rl.YahtzeeBonusRule(
        name="name",
        bonus_value=bonus,
        yahtzee_rule=rl.YahtzeeScoringRule(name="name1"),
    )
    rule.increment(amt=count)
    result = rule._score_bonus()
    assert result == expected


@pytest.mark.parametrize("count, bonus, expected", [
    (0, 5, 0),
    (1, 5, 5),
    (20, 5, 100),
])
def test_score_yahtzee_bonus_rule(count, bonus, expected):
    """Check that yahtzee count-based rules are scored correctly."""
    rule = rl.YahtzeeBonusRule(
        name="name",
        bonus_value=bonus,
        yahtzee_rule=rl.YahtzeeScoringRule(name="name1"),
    )
    rule.increment(amt=count)
    rule.score()
    assert rule.rule_score == expected


@pytest.mark.parametrize("amount", range(11))
def test_increment_yahtzee_bonus_rule(amount):
    """Check that yahtzee count-based rules increment correctly."""
    rule = rl.YahtzeeBonusRule(
        name="name",
        yahtzee_rule=rl.YahtzeeScoringRule(name="name1")
    )
    rule.increment(amt=amount)
    assert rule.counter == amount


@pytest.mark.parametrize("bonus", [
    rl.ThresholdBonusRule(name="name"),
    rl.CountBonusRule(name="name"),
    rl.YahtzeeBonusRule(name="name", yahtzee_rule=rl.YahtzeeScoringRule(name="name1")),
])
def test_scoring_bonuses_already_scored_error(bonus):
    """Check that trying to update an already-score rule
    raises the appropriate error."""
    bonus.increment()
    bonus.score()
    with pytest.raises(rl.RuleAlreadyScoredError, match=r"Rule.*"):
        bonus.score()
