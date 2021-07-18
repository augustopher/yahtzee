from yahtzee.scoring.scoresheet import (
    Scoresheet,
    DuplicateRuleNamesError,
    RuleAlreadyScoredError,
)
from yahtzee.scoring.rules import (
    ChanceScoringRule,
    FullHouseScoringRule,
    ThresholdBonusRule,
    CountBonusRule,
    Section
)
from yahtzee.dice import Die

import pytest


def test_scoresheet_init_valid_rules():
    """Check that scoresheets are initialized properly with valid arguments."""
    rules = [
        ChanceScoringRule(name="rule1"),
        ChanceScoringRule(name="rule2"),
    ]
    bonuses = [CountBonusRule(name="bonus1")]
    result = Scoresheet(rules=rules, bonuses=bonuses)
    assert len(result.rules) == 2
    assert all([score is None for score in result.scores.values()])
    assert len(result.bonuses) == 1
    assert all([score is None for score in result.bonus_scores.values()])


@pytest.mark.parametrize("rules, bonuses", [
    ([ChanceScoringRule(name="rule"), FullHouseScoringRule(name="rule")],
    [CountBonusRule(name="bonus")]),
    ([ChanceScoringRule(name="rule")],
    [CountBonusRule(name="bonus"), ThresholdBonusRule(name="bonus")]),
])
def test_scoresheet_init_dupe_rules_error(rules, bonuses):
    """Check that duplicate rule names raise the appropriate error."""
    with pytest.raises(DuplicateRuleNamesError, match=r"Rules cannot.*"):
        Scoresheet(rules=rules, bonuses=bonuses)


def test_get_name_from_index():
    """Checks that the correct rule name is retrieved by index."""
    rules = [
        ChanceScoringRule(name="rule1"),
        ChanceScoringRule(name="rule2"),
    ]
    bonuses = [CountBonusRule(name="bonus1")]
    sheet = Scoresheet(rules=rules, bonuses=bonuses)
    result = sheet._get_name_from_index(index=1)
    assert result == rules[0].name


def test_get_rule_from_name():
    """Checks that the correct rule is retrieved by name."""
    rules = [
        ChanceScoringRule(name="rule1"),
        ChanceScoringRule(name="rule2"),
    ]
    bonuses = [CountBonusRule(name="bonus1")]
    sheet = Scoresheet(rules=rules, bonuses=bonuses)
    result = sheet._get_rule_from_name(name="rule2")
    assert result == rules[1]


@pytest.mark.parametrize("score_rule, expected", [
    ("rule1", False),
    ("rule2", True),
])
def test_check_rule_not_scored(score_rule, expected):
    """Checks that a rule already scored or not, properly."""
    rules = [
        ChanceScoringRule(name="rule1"),
        ChanceScoringRule(name="rule2"),
    ]
    bonuses = [CountBonusRule(name="bonus1")]
    sheet = Scoresheet(rules=rules, bonuses=bonuses)
    sheet.scores[score_rule] = 1
    result = sheet._check_rule_not_scored(name="rule1")
    assert result is expected


def test_update_rule_score():
    """Check that a rule's score is updated properly from a requested name."""
    rules = [
        ChanceScoringRule(name="rule1"),
        ChanceScoringRule(name="rule2"),
    ]
    bonuses = [CountBonusRule(name="bonus1")]
    dice = [Die(starting_face=1), Die(starting_face=2)]

    sheet = Scoresheet(rules=rules, bonuses=bonuses)

    sheet.update_rule_score(name="rule1", dice=dice)

    expected_scores = {
        "rule1": 3,
        "rule2": None,
    }

    assert all([
        score == expected_scores[rule] for rule, score in sheet.scores.items()
    ])


def test_update_rule_score_error():
    """Check that scoring a previously-scored rule raises
    the appropriate error."""
    rules = [
        ChanceScoringRule(name="rule1"),
        ChanceScoringRule(name="rule2"),
    ]
    bonuses = [CountBonusRule(name="bonus1")]
    dice = [Die(starting_face=1), Die(starting_face=2)]

    sheet = Scoresheet(rules=rules, bonuses=bonuses)

    sheet.update_rule_score(name="rule1", dice=dice)
    with pytest.raises(RuleAlreadyScoredError, match=r"Rule.*"):
        sheet.update_rule_score(name="rule1", dice=dice)


def test_update_score():
    """Check that a rule's score is updated properly from a requested index."""
    rules = [
        ChanceScoringRule(name="rule1"),
        ChanceScoringRule(name="rule2"),
    ]
    bonuses = [CountBonusRule(name="bonus1")]
    dice = [Die(starting_face=1), Die(starting_face=2)]

    sheet = Scoresheet(rules=rules, bonuses=bonuses)

    sheet.update_score(index=1, dice=dice)

    expected_scores = {
        "rule1": 3,
        "rule2": None,
    }

    assert all([
        score == expected_scores[rule] for rule, score in sheet.scores.items()
    ])


@pytest.mark.parametrize("section, expected", [
    (Section.UPPER, 5),
    (Section.LOWER, 10),
])
def test_get_section_subtotal_score(section, expected):
    rules = [
        ChanceScoringRule(name="rule1", section=Section.UPPER),
        ChanceScoringRule(name="rule2", section=Section.UPPER),
        ChanceScoringRule(name="rule3", section=Section.LOWER),
        ChanceScoringRule(name="rule4", section=Section.LOWER),
    ]
    bonuses = [CountBonusRule(name="bonus1")]
    sheet = Scoresheet(rules=rules, bonuses=bonuses)

    # set score for rule1 to 5
    sheet.update_rule_score(name="rule1", dice=[Die(sides=6, starting_face=5)])
    # set score for rule3 to 10
    sheet.update_rule_score(
        name="rule3",
        dice=[Die(sides=6, starting_face=5), Die(sides=6, starting_face=5)]
    )

    result = sheet._get_section_subtotal_score(section=section)
    assert result == expected
