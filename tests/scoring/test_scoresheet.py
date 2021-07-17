from yahtzee.scoring.scoresheet import (
    Scoresheet,
    DuplicateRuleNamesError,
)
from yahtzee.scoring.rules import (
    ChanceScoringRule,
    FullHouseScoringRule,
)
from yahtzee.dice import Die

import pytest

def test_scoresheet_init_valid_rules():
    """Check that scoresheets are initialized properly with valid arguments."""
    rules = [
        ChanceScoringRule(name="rule1"),
        ChanceScoringRule(name="rule2"),
    ]
    result = Scoresheet(rules=rules)
    assert len(result.rules) == 2
    assert all([score is None for score in result.scores.values()])

def test_scoresheet_init_dupe_rules_error():
    """Check that duplicate rule names raise the appropriate error."""
    rules = [
        ChanceScoringRule(name="rule"),
        FullHouseScoringRule(name="rule")
    ]
    with pytest.raises(DuplicateRuleNamesError, match=r"Rules cannot.*"):
        result = Scoresheet(rules=rules)

def test_get_rule_from_name():
    """Checks that the correct rule is retrieved by name."""
    rules = [
        ChanceScoringRule(name="rule1"),
        ChanceScoringRule(name="rule2"),
    ]
    sheet = Scoresheet(rules=rules)
    result = sheet._get_rule_from_name(name="rule2")
    assert result == rules[1]

def test_update_rule_score():
    """Check that a rule's score is updated properly."""
    rules = [
        ChanceScoringRule(name="rule1"),
        ChanceScoringRule(name="rule2"),
    ]
    dice = [Die(starting_face=1), Die(starting_face=2)]

    sheet = Scoresheet(rules=rules)

    sheet.update_rule_score(name="rule1", dice=dice)

    expected_scores = {
        "rule1": 3,
        "rule2": None,
    }

    assert all([
        score == expected_scores[rule] for rule, score in sheet.scores.items()
    ])
