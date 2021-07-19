from yahtzee.scoring.scoresheet import Scoresheet
from yahtzee.scoring.rules import (
    ChanceScoringRule,
    FullHouseScoringRule,
    YahtzeeBonusRule,
    CountBonusRule,
    Section,
)

import pytest


def test_scoresheet_scores_header():
    """Checks that the score header is assembled correctly."""
    sheet = Scoresheet(
        rules=[ChanceScoringRule(name="rule")],
        bonuses=[CountBonusRule(name="bonus1")],
        yahtzee_bonus=YahtzeeBonusRule(name="yahtzee")
    )
    result = sheet._generate_scores_header()
    expected = ["Rule", "Name", "Scored"]
    assert result == expected


@pytest.mark.parametrize("section, expected", [
    (Section.UPPER, ["Upper Section"]),
    (Section.LOWER, ["Lower Section"]),
])
def test_scoresheet_section_header(section, expected):
    """Checks that the section header is assembled correctly."""
    sheet = Scoresheet(
        rules=[ChanceScoringRule(name="rule")],
        bonuses=[CountBonusRule(name="bonus1")],
        yahtzee_bonus=YahtzeeBonusRule(name="yahtzee")
    )
    result = sheet._generate_section_header(section=section)
    assert result == expected


def test_scoresheet_score_row():
    """Checks that a given row is assembled correctly."""
    rules = [
        ChanceScoringRule(name="rule1"),
        FullHouseScoringRule(name="rule2"),
    ]
    bonuses = [CountBonusRule(name="bonus1")]
    yahtzee_bonus = YahtzeeBonusRule(name="yahtzee")
    sheet = Scoresheet(rules=rules, bonuses=bonuses, yahtzee_bonus=yahtzee_bonus)
    results = [sheet._generate_score_row(rule.name) for rule in rules]
    expected = [[1, "rule1", None], [2, "rule2", None]]
    assert results == expected


@pytest.mark.parametrize("section, expected", [
    (Section.UPPER, [
        ["Upper Section"],
        ["Rule", "Name", "Scored"],
        [1, "rule1", None],
    ]),
    (Section.LOWER, [
        ["Lower Section"],
        ["Rule", "Name", "Scored"],
        [2, "rule2", None],
        [3, "rule3", None],
    ]),
])
def test_scoresheet_section(section, expected):
    """Check that each section is assembled correctly."""
    rules = [
        ChanceScoringRule(name="rule1", section=Section.UPPER),
        ChanceScoringRule(name="rule2", section=Section.LOWER),
        ChanceScoringRule(name="rule3", section=Section.LOWER),
    ]
    bonuses = [CountBonusRule(name="bonus1")]
    yahtzee_bonus = YahtzeeBonusRule(name="yahtzee")
    sheet = Scoresheet(rules=rules, bonuses=bonuses, yahtzee_bonus=yahtzee_bonus)
    result = sheet._generate_section(section=section)
    assert result == expected


def test_scoresheet_scoresheet():
    """Check that the entire scoresheet is assembled correctly."""
    rules = [
        ChanceScoringRule(name="rule1", section=Section.UPPER),
        ChanceScoringRule(name="rule2", section=Section.LOWER),
        ChanceScoringRule(name="rule3", section=Section.LOWER),
    ]
    bonuses = [CountBonusRule(name="bonus1")]
    yahtzee_bonus = YahtzeeBonusRule(name="yahtzee")
    sheet = Scoresheet(rules=rules, bonuses=bonuses, yahtzee_bonus=yahtzee_bonus)
    result = sheet._generate_scoresheet()
    expected = [
        ["Upper Section"],
        ["Rule", "Name", "Scored"],
        [1, "rule1", None],
        ["Lower Section"],
        ["Rule", "Name", "Scored"],
        [2, "rule2", None],
        [3, "rule3", None],
    ]
    assert result == expected


def test_scoresheet_output():
    """Check that the entire scoresheet is output correctly."""
    rules = [
        ChanceScoringRule(name="rule1", section=Section.UPPER),
        ChanceScoringRule(name="rule2", section=Section.LOWER),
        ChanceScoringRule(name="rule3", section=Section.LOWER),
    ]
    bonuses = [CountBonusRule(name="bonus1")]
    yahtzee_bonus = YahtzeeBonusRule(name="yahtzee")
    sheet = Scoresheet(rules=rules, bonuses=bonuses, yahtzee_bonus=yahtzee_bonus)
    result = sheet.output()
    expected = (
        "-------------  -----  ------\nUpper Section\nRule           "
        "Name   Scored\n1              rule1\nLower Section\nRule           Name   "
        "Scored\n2              rule2\n3              rule3\n-------------  -----  "
        "------"
    )
    assert result == expected
