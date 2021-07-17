from yahtzee.scoring.scoresheet import (
    Scoresheet,
    DuplicateRuleNamesError,
)
from yahtzee.scoring.rules import (
    ChanceScoringRule,
    FullHouseScoringRule,
    Section,
)
from yahtzee.dice import Die

import pytest

def test_scoresheet_scores_header():
    """Checks that the score header is assembled correctly."""
    sheet = Scoresheet(rules=[ChanceScoringRule(name="rule")])
    result = sheet._generate_scores_header()
    expected = ["Rule", "Scored"]
    assert result == expected

@pytest.mark.parametrize("section, expected",[
    (Section.UPPER, ["Upper Section", "~~"]),
    (Section.LOWER, ["Lower Section", "~~"]),
])
def test_scoresheet_section_header(section, expected):
    """Checks that the section header is assembled correctly."""
    sheet = Scoresheet(rules=[ChanceScoringRule(name="rule")])
    result = sheet._generate_section_header(section=section)
    assert result == expected

def test_scoresheet_score_row():
    """Checks that a given row is assembled correctly."""
    rules = [
        ChanceScoringRule(name="rule1"),
        FullHouseScoringRule(name="rule2"),
    ]
    sheet = Scoresheet(rules=rules)
    results = [sheet._generate_score_row(rule.name) for rule in rules]
    expected = [["rule1", None], ["rule2", None]]
    assert results == expected

@pytest.mark.parametrize("section, expected", [
    (Section.UPPER, [
        ["Upper Section", "~~"],
        ["Rule", "Scored"],
        ["rule1", None],
    ]),
    (Section.LOWER, [
        ["Lower Section", "~~"],
        ["Rule", "Scored"],
        ["rule2", None],
        ["rule3", None],
    ]),
])
def test_scoresheet_section(section, expected):
    """Check that each section is assembled correctly."""
    rules = [
        ChanceScoringRule(name="rule1", section=Section.UPPER),
        ChanceScoringRule(name="rule2", section=Section.LOWER),
        ChanceScoringRule(name="rule3", section=Section.LOWER),
    ]
    sheet = Scoresheet(rules=rules)
    result = sheet._generate_section(section=section)
    assert result == expected

def test_scoresheet_scoresheet():
    """Check that the entire scoresheet is assembled correctly."""
    rules = [
        ChanceScoringRule(name="rule1", section=Section.UPPER),
        ChanceScoringRule(name="rule2", section=Section.LOWER),
        ChanceScoringRule(name="rule3", section=Section.LOWER),
    ]
    sheet = Scoresheet(rules=rules)
    result = sheet._generate_scoresheet()
    expected = [
        ["Upper Section", "~~"],
        ["Rule", "Scored"],
        ["rule1", None],
        ["Lower Section", "~~"],
        ["Rule", "Scored"],
        ["rule2", None],
        ["rule3", None],
    ]
    assert result == expected

def test_scoresheet_output():
    """Check that the entire scoresheet is output correctly."""
    rules = [
        ChanceScoringRule(name="rule1", section=Section.UPPER),
        ChanceScoringRule(name="rule2", section=Section.LOWER),
        ChanceScoringRule(name="rule3", section=Section.LOWER),
    ]
    sheet = Scoresheet(rules=rules)
    result = sheet.output()
    expected = "-------------  ------\nUpper Section  ~~\nRule           Scored\nrule1\nLower Section  ~~\nRule           Scored\nrule2\nrule3\n-------------  ------"
    assert result == expected
