from ..dice import DiceList
from .rules import ScoringRule, BonusRule, Section, AllRulesListsType
from .validators import _find_duplicates

from typing import List, Dict, Optional, Any

from tabulate import tabulate


class DuplicateRuleNamesError(ValueError):
    pass


class RuleAlreadyScoredError(ValueError):
    pass


class Scoresheet():
    """Representation of a scoring sheet."""
    def __init__(self, rules: List[ScoringRule], bonuses: List[BonusRule]):
        self._validate_rule_names(rules)
        self._validate_rule_names(bonuses)
        self.rules = rules
        self.scores: Dict[str, Optional[int]] = {rule.name: None for rule in rules}
        self.rules_map = {idx + 1: rule.name for idx, rule in enumerate(rules)}
        self.bonuses = bonuses
        self.bonus_scores: Dict[str, Optional[int]] = {
            rule.name: None for rule in bonuses
        }

    def _validate_rule_names(self, rules: AllRulesListsType) -> None:
        """Check that all rule names are unique."""
        rule_names = [rule.name for rule in rules]
        duplicate_names = _find_duplicates(rule_names)
        if duplicate_names:
            raise DuplicateRuleNamesError(
                f"Rules cannot share names. Duplicate names are: "
                f"{duplicate_names}."
            )
        return None

    def update_score(self, index: int, dice: DiceList) -> None:
        """Updates the score for a rule, chosen by user input,
        based on the given dice."""
        rule_name = self._get_name_from_index(index=index)
        self.update_rule_score(name=rule_name, dice=dice)
        return None

    def update_rule_score(self, name: str, dice: DiceList) -> None:
        """Updates the score for a given rule, based on the given dice."""
        if not self._check_rule_not_scored(name=name):
            raise RuleAlreadyScoredError(
                f"Rule {name} has already been scored."
            )
        selected_rule = self._get_rule_from_name(name=name)
        self.scores[name] = selected_rule.score(dice=dice)
        return None

    def _get_rule_from_name(self, name: str) -> ScoringRule:
        """Helper to retrieve the rule from its name."""
        return next(rule for rule in self.rules if rule.name == name)

    def _get_name_from_index(self, index: int) -> str:
        """Helper to retrieve the rule name from the user-input index."""
        return self.rules_map[index]

    def _check_rule_not_scored(self, name: str) -> bool:
        """Checks that a rule is not already scored."""
        return self.scores[name] is None

    def _get_section_subtotal_score(self, section: Section) -> int:
        """Calculates the total score for a section, before bonuses."""
        section_rules = [rule.name for rule in self.rules if rule.section == section]
        section_scores = [self.scores[rule] for rule in section_rules]
        return sum([s for s in section_scores if s])

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

    def _generate_score_row(self, name: str) -> List[Any]:
        """Assembles the row corresponding to the given rule."""
        index = next(idx for idx, nm in self.rules_map.items() if nm == name)
        row = [index, name, self.scores[name]]
        return row

    def _generate_section(self, section: Section) -> List[List[Any]]:
        """Assembles a given section of the scoresheet."""
        section_header = self._generate_section_header(section=section)
        scores_header = self._generate_scores_header()
        section_rules = [rule for rule in self.rules if rule.section == section]
        scores_rows = [self._generate_score_row(rule.name) for rule in section_rules]
        return [section_header] + [scores_header] + scores_rows

    def _generate_scoresheet(self) -> List[List[Any]]:
        """Assembles the entire scoresheet."""
        upper_section = self._generate_section(section=Section.UPPER)
        lower_section = self._generate_section(section=Section.LOWER)
        return upper_section + lower_section

    def output(self) -> str:
        """Gives the full scoresheet."""
        return tabulate(self._generate_scoresheet())
