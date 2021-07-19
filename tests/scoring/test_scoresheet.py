from yahtzee.scoring.scoresheet import (
    Scoresheet,
    DuplicateRuleNamesError,
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
    assert len(result.bonuses) == 1


@pytest.mark.parametrize("rules, bonuses", [
    (
        [ChanceScoringRule(name="rule"), FullHouseScoringRule(name="rule")],
        [CountBonusRule(name="bonus")]
    ),
    (
        [ChanceScoringRule(name="rule")],
        [CountBonusRule(name="bonus"), ThresholdBonusRule(name="bonus")]
    ),
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
        0: 3,
        1: None,
    }

    assert all([
        rule.rule_score == expected_scores[idx] for idx, rule in enumerate(rules)
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
