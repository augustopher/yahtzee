import yahtzee.scoring.rules as rules
from yahtzee.dice import Die

import pytest

def mock_die_seq(monkeypatch, seq):
    """Helper to manually set the showing face of each die."""
    dice = []
    for x in seq:
        monkeypatch.setattr(Die, "_roll_die", lambda n: x)
        die = Die()
        dice = dice + [die]
    return dice

@pytest.mark.parametrize("seq, face, expected", [
    ([1,2,3,4,5], 1, 1),
    ([1,2,2,3,4], 2, 2),
])
def test_find_matching_dice(monkeypatch, seq, face, expected):
    """Check that the correct dice are identified and returned."""
    dice = mock_die_seq(monkeypatch=monkeypatch, seq=seq)
    result = rules._find_matching_dice(dice=dice, face_value=face)
    result_faces = [die.showing_face for die in result]
    assert len(set(result_faces)) == 1
    assert result_faces[0] == face
    assert len(result) == expected

def test_find_matching_dice_no_match(monkeypatch):
    """Check that no dice are returned when no match is found."""
    dice = mock_die_seq(monkeypatch, seq=[1,1,1,3,3])
    result = rules._find_matching_dice(dice=dice, face_value=2)
    assert len(result) == 0

@pytest.mark.parametrize("seq, expected", [
    ([1,2,3,4,5], True),
    ([1,1,3,4,5], False),
])
def test_validate_straight(seq, expected):
    """Check that straights are properly identified."""
    result = rules._validate_straight(values=seq)
    assert result is expected

@pytest.mark.parametrize("seq, expected", [
    ([1,2,3,4,5], True),
    ([1,1,3,4,5], False),
])
def test_validate_large_straight(monkeypatch, seq, expected):
    """Check that large straights are properly identified."""
    dice = mock_die_seq(monkeypatch=monkeypatch, seq=seq)
    result = rules._validate_large_straight(dice=dice)
    assert result is expected

@pytest.mark.parametrize("seq, expected", [
    ([1,2,3,4,5], True),
    ([1,1,2,3,4], True),
    ([1,1,2,2,3], False),
])
def test_validate_small_straight(monkeypatch, seq, expected):
    """Check that small straights are properly identified."""
    dice = mock_die_seq(monkeypatch=monkeypatch, seq=seq)
    result = rules._validate_small_straight(dice=dice)
    assert result is expected

@pytest.mark.parametrize("seq, n, expected", [
    ([1,1,2,3,4], 2, True),
    ([1,2,3,4,5], 2, False),
    ([1,1,3,4,5], 3, False),
    ([1,1,1,1,5], 4, True),
    ([1,1,1,1,5], 5, False),
])
def test_validate_nofkind(monkeypatch, seq, n, expected):
    """Check that n-of-a-kind are properly identified."""
    dice = mock_die_seq(monkeypatch=monkeypatch, seq=seq)
    result = rules._validate_nofkind(dice=dice, n=n)
    assert result is expected

@pytest.mark.parametrize("seq, expected", [
    ([1,1,6,6,6], True),
    ([1,2,3,4,5], False),
    ([1,1,3,4,5], False),
    ([1,1,1,4,5], False),
])
def test_validate_full_house(monkeypatch, seq, expected):
    """Check that full houses are properly identified."""
    dice = mock_die_seq(monkeypatch=monkeypatch, seq=seq)
    result = rules._validate_full_house(dice=dice)
    assert result is expected

@pytest.mark.parametrize("seq, expected", [
    ([1,2,3,4,5], 15),
    ([1,1,3,4,5], 14),
    ([2,2,3,4,5], 16),
])
def test_score_chance_rule(monkeypatch, seq, expected):
    dice = mock_die_seq(monkeypatch=monkeypatch, seq=seq)
    rule = rules.ChanceScoringRule(name="name")
    result = rule.score(dice=dice)
    assert result == expected

@pytest.mark.parametrize("seq, expected", [
    ([1,1,3,4,5], 0),
    ([1,2,3,4,5], 2),
    ([2,2,3,4,5], 4),
])
def test_score_multiples_rule(monkeypatch, seq, expected):
    dice = mock_die_seq(monkeypatch=monkeypatch, seq=seq)
    rule = rules.MultiplesScoringRule(name="name", face_value=2)
    result = rule.score(dice=dice)
    assert result == expected

@pytest.mark.parametrize("seq, override, expected", [
    ([1,2,3,4,5], None, 0),
    ([1,1,3,4,5], None, 0),
    ([1,1,1,4,5], None, 12),
    ([1,1,1,1,5], None, 9),
    ([1,1,1,1,1], None, 5),
    ([1,2,3,4,5], 20, 0),
    ([1,1,3,4,5], 20, 0),
    ([1,1,1,4,5], 20, 20),
    ([1,1,1,1,5], 20, 20),
    ([1,1,1,1,1], 20, 20),
])
def test_score_nkind_rule(monkeypatch, seq, override, expected):
    dice = mock_die_seq(monkeypatch=monkeypatch, seq=seq)
    rule = rules.NofKindScoringRule(name="name", n=3, override_score=override)
    result = rule.score(dice=dice)
    assert result == expected

@pytest.mark.parametrize("seq, expected", [
    ([1,2,3,4,5], 0),
    ([1,1,3,4,5], 0),
    ([1,1,1,4,5], 0),
    ([1,1,2,2,2], 5),
])
def test_score_full_house_rule(monkeypatch, seq, expected):
    dice = mock_die_seq(monkeypatch=monkeypatch, seq=seq)
    rule = rules.FullHouseScoringRule(name="name", score_value = 5)
    result = rule.score(dice=dice)
    assert result == expected

@pytest.mark.parametrize("seq, expected", [
    ([1,2,3,4,5], 5),
    ([1,1,3,4,5], 0),
    ([1,1,2,3,4], 0),
])
def test_score_large_straight_rule(monkeypatch, seq, expected):
    dice = mock_die_seq(monkeypatch=monkeypatch, seq=seq)
    rule = rules.LargeStraightScoringRule(name="name", score_value = 5)
    result = rule.score(dice=dice)
    assert result == expected

@pytest.mark.parametrize("seq, expected", [
    ([1,2,3,4,5], 5),
    ([1,1,3,4,5], 0),
    ([1,1,2,3,4], 5),
])
def test_score_small_straight_rule(monkeypatch, seq, expected):
    dice = mock_die_seq(monkeypatch=monkeypatch, seq=seq)
    rule = rules.SmallStraightScoringRule(name="name", score_value = 5)
    result = rule.score(dice=dice)
    assert result == expected
