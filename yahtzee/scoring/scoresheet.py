from ..dice import Die
from .rules import ScoringRule, Section
from .validators import _find_duplicates

from typing import List, Union

from tabulate import tabulate

class DuplicateRuleNamesError(ValueError):
    pass

class Scoresheet():
    """Representation of a scoring sheet."""
    def __init__(self, rules: List[ScoringRule]):
        self._validate_rule_names(rules)
        self.rules = rules
        self.scores = {rule.name: None for rule in rules}
        self.rules_map = {idx + 1: rule.name for idx, rule in enumerate(rules)}

    def _validate_rule_names(self, rules: List[ScoringRule]) -> None:
        """Check that all rule names are unique."""
        rule_names = [rule.name for rule in rules]
        duplicate_names = _find_duplicates(rule_names)
        if duplicate_names:
            raise DuplicateRuleNamesError(
                f"Rules cannot share names. Duplicate names are: "
                f"{duplicate_names}."
            )
        return None

    def update_score(self, index: int, dice: List[Die]) -> None:
        """Updates the score for a rule, chosen by user input,
        based on the given dice."""
        rule_name = self._get_name_from_index(index=index)
        self.update_rule_score(name=rule_name, dice=dice)
        return None

    def update_rule_score(self, name: str, dice: List[Die]) -> None:
        """Updates the score for a given rule, based on the given dice."""
        selected_rule = self._get_rule_from_name(name=name)
        self.scores[name] = selected_rule.score(dice=dice)
        return None

    def _get_rule_from_name(self, name: str) -> ScoringRule:
        """Helper to retrieve the rule from its name."""
        return next(rule for rule in self.rules if rule.name == name)

    def _get_name_from_index(self, index: int) -> str:
        """Helper to retrieve the rule name from the user-input index."""
        return self.rules_map[index]

    @staticmethod
    def _generate_scores_header() -> List[str]:
        """Assembles the fields header of the scoresheet."""
        scores_header = ["Rule", "Name", "Scored"]
        return scores_header

    @staticmethod
    def _generate_section_header(section: Section) -> List[str]:
        """Assembles the section header of the scoresheet."""
        section_header = [f"{section.name} Section".title()]
        return section_header

    def _generate_score_row(self, name: str) -> List[Union[str, int, None]]:
        """Assembles the row corresponding to the given rule."""
        index = [idx for idx, nm in self.rules_map.items() if nm == name][0]
        row = [index, name, self.scores[name]]
        return row

    def _generate_section(self, section: Section) -> List[List[Union[str, int, None]]]:
        """Assembles a given section of the scoresheet."""
        section_header = self._generate_section_header(section=section)
        scores_header = self._generate_scores_header()
        section_rules = [rule for rule in self.rules if rule.section == section]
        scores_rows = [self._generate_score_row(rule.name) for rule in section_rules]
        return [section_header] + [scores_header] + scores_rows

    def _generate_scoresheet(self) -> List[List[Union[str, int, None]]]:
        """Assembles the entire scoresheet."""
        upper_section = self._generate_section(section=Section.UPPER)
        lower_section = self._generate_section(section=Section.LOWER)
        return upper_section + lower_section

    def output(self) -> str:
        """Gives the full scoresheet."""
        return tabulate(self._generate_scoresheet())