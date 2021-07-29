from yahtzee.scoring.scoresheet import Scoresheet
import yahtzee.scoring.rules as rl
from yahtzee.dice import Die
import yahtzee.errors as er

import pytest


def test_scoresheet_init_valid_rules():
    """Check that scoresheets are initialized properly with valid arguments."""
    rules = [
        rl.ChanceScoringRule(name="rule1"),
        rl.ChanceScoringRule(name="rule2"),
        rl.YahtzeeScoringRule(name="name1"),
    ]
    bonuses = [rl.CountBonusRule(name="bonus1")]
    yahtzee_bonus = rl.YahtzeeBonusRule(
        name="yahtzee",
        yahtzee_rule=rl.YahtzeeScoringRule(name="name1")
    )
    result = Scoresheet(rules=rules, bonuses=bonuses, yahtzee_bonus=yahtzee_bonus)
    assert len(result.rules) == 3
    assert len(result.bonuses) == 1


@pytest.mark.parametrize("rules, bonuses", [
    (
        [rl.ChanceScoringRule(name="rule"), rl.FullHouseScoringRule(name="rule")],
        [rl.CountBonusRule(name="bonus")]
    ),
    (
        [rl.ChanceScoringRule(name="rule")],
        [rl.CountBonusRule(name="bonus"), rl.ThresholdBonusRule(name="bonus")]
    ),
])
def test_scoresheet_init_dupe_rules_error(rules, bonuses):
    """Check that duplicate rule names raise the appropriate error."""
    with pytest.raises(er.DuplicateRuleNamesError, match=r"Rules cannot.*"):
        Scoresheet(
            rules=rules,
            bonuses=bonuses,
            yahtzee_bonus=rl.YahtzeeBonusRule(
                name="yahtzee",
                yahtzee_rule=rl.YahtzeeScoringRule(name="name1")
            )
        )


def test_get_rule_from_name():
    """Checks that the correct rule is retrieved by name."""
    rules = [
        rl.ChanceScoringRule(name="rule1"),
        rl.ChanceScoringRule(name="rule2"),
    ]
    bonuses = [rl.CountBonusRule(name="bonus1")]
    yahtzee_bonus = rl.YahtzeeBonusRule(
        name="yahtzee",
        yahtzee_rule=rl.YahtzeeScoringRule(name="name1")
    )
    sheet = Scoresheet(rules=rules, bonuses=bonuses, yahtzee_bonus=yahtzee_bonus)
    result = sheet._get_rule_from_name(name="rule2")
    assert result == rules[1]


def test_update_score():
    """Check that a rule's score is updated properly from a requested index."""
    rules = [
        rl.ChanceScoringRule(name="rule1"),
        rl.ChanceScoringRule(name="rule2"),
    ]
    bonuses = [rl.CountBonusRule(name="bonus1")]
    yahtzee_bonus = rl.YahtzeeBonusRule(
        name="yahtzee",
        yahtzee_rule=rl.YahtzeeScoringRule(name="name1")
    )
    dice = [Die(starting_face=1), Die(starting_face=2)]

    sheet = Scoresheet(rules=rules, bonuses=bonuses, yahtzee_bonus=yahtzee_bonus)

    sheet.update_score(name="rule1", dice=dice)

    expected_scores = {
        "rule1": 3,
        "rule2": None,
    }

    assert all([
        rule.rule_score == expected_scores[rule.name] for rule in rules
    ])


def test_update_dep_bonuses():
    """Check that bonuses based on specific rules is incremented correctly."""
    rules = [rl.ChanceScoringRule(name="rule")]
    bonuses = [
        rl.CountBonusRule(name="bonus", req_rules=rules),
        rl.CountBonusRule(name="bonus2"),
    ]
    yahtzee_bonus = rl.YahtzeeBonusRule(
        name="yahtzee",
        yahtzee_rule=rl.YahtzeeScoringRule(name="name1")
    )
    sheet = Scoresheet(rules=rules, bonuses=bonuses, yahtzee_bonus=yahtzee_bonus)

    rules[0].rule_score = 5
    sheet._update_dep_bonuses(name="rule")
    assert bonuses[0].counter == 5
    # second bonus should not be affected
    assert bonuses[1].counter == 0


def test_update_yahtzee_bonus():
    """Check that the yahtzee bonus is incremented correctly."""
    rules = [rl.ChanceScoringRule(name="rule")]
    bonuses = [rl.CountBonusRule(name="bonus")]
    yahtzee_bonus = rl.YahtzeeBonusRule(
        name="yahtzee",
        yahtzee_rule=rl.YahtzeeScoringRule(name="name1")
    )
    sheet = Scoresheet(rules=rules, bonuses=bonuses, yahtzee_bonus=yahtzee_bonus)

    sheet.update_yahtzee_bonus(amt=5)
    assert sheet.yahtzee_bonus.counter == 5


@pytest.mark.parametrize("section, expected", [
    (rl.Section.UPPER, 5),
    (rl.Section.LOWER, 10),
])
def test_get_section_subtotal_score(section, expected):
    rules = [
        rl.ChanceScoringRule(name="rule1", section=rl.Section.UPPER),
        rl.ChanceScoringRule(name="rule2", section=rl.Section.UPPER),
        rl.ChanceScoringRule(name="rule3", section=rl.Section.LOWER),
        rl.ChanceScoringRule(name="rule4", section=rl.Section.LOWER),
    ]
    bonuses = [rl.CountBonusRule(name="bonus1")]
    yahtzee_bonus = rl.YahtzeeBonusRule(
        name="yahtzee",
        yahtzee_rule=rl.YahtzeeScoringRule(name="name1")
    )
    sheet = Scoresheet(rules=rules, bonuses=bonuses, yahtzee_bonus=yahtzee_bonus)

    # set score for rule1 to 5
    sheet.update_score(name="rule1", dice=[Die(sides=6, starting_face=5)])
    # set score for rule3 to 10
    sheet.update_score(
        name="rule3",
        dice=[Die(sides=6, starting_face=5), Die(sides=6, starting_face=5)]
    )

    result = sheet._get_section_subtotal_score(section=section)
    assert result == expected
