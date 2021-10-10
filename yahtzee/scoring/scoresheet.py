from typing import Any
from typing import List
from typing import cast

from tabulate import tabulate

from . import rules as rl
from . import validators as vl
from .. import errors as er
from ..dice import DiceList


class Scoresheet:
    """Representation of a scoring sheet.

    Parameters
    ----------
    rules : list of ScoringRule
        Rules to include on the sheet.
    bonuses : list of BonusRule
        Bonuses to include on the sheet
    yahtzee_bonus : YahtzeeBonusRule
        Bonus rule for additional Yahtzees to include on the sheet.

    Attributes
    ----------
    rules : list of ScoringRule
        Rules to include on the sheet.
    bonuses : list of BonusRule
        Bonuses to include on the sheet
    yahtzee_bonus : YahtzeeBonusRule
        Bonus rule for additional Yahtzees to include on the sheet.
    """
    def __init__(
        self,
        rules: List[rl.ScoringRule],
        bonuses: List[rl.BonusRule],
        yahtzee_bonus: rl.YahtzeeBonusRule
    ):
        self._validate_rule_names(
            rules=rules,
            bonuses=bonuses,
            yahtzee_bonus=yahtzee_bonus
        )
        self.rules = rules
        self.bonuses = bonuses
        self.yahtzee_bonus = yahtzee_bonus

    def _validate_rule_names(
        self,
        rules: List[rl.ScoringRule],
        bonuses: List[rl.BonusRule],
        yahtzee_bonus: rl.YahtzeeBonusRule
    ) -> None:
        """Check that all rule names are unique.

        Parameters
        ----------
        rules : list of ScoringRule
            Rules to check.
        bonuses : list of BonusRule
            Bonuses to check.
        yahtzee_bonus : YahtzeeBonusRule
            Bonus rule (for additional Yahtzees) to check.

        Raises
        ------
        DuplicateRuleNamesError
            If any rules (standard, bonus, or otherwise) are duplicative.
        """
        rule_names = [rule.name for rule in rules]
        bonus_names = [bonus.name for bonus in bonuses]
        all_names = rule_names + bonus_names + [yahtzee_bonus.name]
        duplicate_names = vl.find_duplicates(all_names)
        if duplicate_names:
            raise er.DuplicateRuleNamesError(
                f"Rules cannot share names. Duplicate names are: "
                f"{duplicate_names}."
            )

    def update_score(self, name: str, dice: DiceList) -> None:
        """Updates the score for a rule, from a rule name,
        based on the given dice.

        Parameters
        ----------
        name : str
            Name of rule to update.
        dice : list of Die
            Set of dice to score.
        """
        rule = self._get_rule_from_name(name=name)
        rule.score(dice=dice)

    def _update_dep_bonuses(self, name: str) -> None:
        """Increments the counters for any bonuses which are dependent
        on the given rule.

        Parameters
        ----------
        name : str
            Name of the rule whose bonuses should be updated.
        """
        rule = self._get_rule_from_name(name=name)
        for bonus in self.bonuses:
            if bonus.req_rules and rule in bonus.req_rules:
                # placate mypy
                rule_amt = cast(int, rule.rule_score)
                bonus.increment(amt=rule_amt)

    def _get_rule_from_name(self, name: str) -> rl.ScoringRule:
        """Helper to retrieve the rule from its name.

        Parameters
        ----------
        name : str
            Name of rule to retrieve.

        Returns
        -------
        ScoringRule
            The requested rule.
        """
        return next(rule for rule in self.rules if rule.name == name)

    def _get_section_subtotal_score(self, section: rl.Section) -> int:
        """Calculates the total score for a section, before bonuses.

        Parameters
        ----------
        section : Section
            Which scoresheet section to score.

        Returns
        -------
        int
            Sub-total score for the section.
        """
        section_rules = [
            self._get_rule_from_name(name=rule.name)
            for rule in self.rules
            if rule.section == section
        ]
        section_scores = [rule.rule_score for rule in section_rules]
        return sum([s for s in section_scores if s])

    def update_yahtzee_bonus(self, amt: int = 1) -> None:
        """Increments the counter of the yahtzee bonus rule.

        Parameters
        ----------
        amt : int
            Amount of additional Yahtzees to add to the `yahtzee_bonus`.
            Defaults to 1.
        """
        self.yahtzee_bonus.increment(amt=amt)

    @staticmethod
    def _generate_scores_header() -> List[str]:
        """Assembles the fields header of the scoresheet.

        Returns
        -------
        list of str
            The header for a set of rules on the scoresheet.
        """
        scores_header = ["Rule", "Scored"]
        return scores_header

    @staticmethod
    def _generate_section_header(section: rl.Section) -> List[str]:
        """Assembles the section header of the scoresheet.

        Parameters
        ----------
        section : Section
            Which section of the scoresheet to get a header for.

        Returns
        -------
        list of str
            The header for a section on the scoresheet.
        """
        section_header = [f"{section.name} Section".title()]
        return section_header

    def _generate_score_row(self, name: str) -> List[Any]:
        """Assembles the row corresponding to the given rule.

        Parameters
        ----------
        name : str
            Name of the rule in the scoresheet to get a row for.

        Returns
        -------
        list
            The row for a rule, showing its index (for selection), name, and score.
        """
        rule = self._get_rule_from_name(name=name)
        row = [name, rule.rule_score]
        return row

    def _generate_section(self, section: rl.Section) -> List[List[Any]]:
        """Assembles a given section of the scoresheet.

        Parameters
        ----------
        section : Section
            Which section of the scoresheet to get.

        Returns
        -------
        list of list
            The section of the scoresheet, showing all headers and rules (with scores).
        """
        section_header = self._generate_section_header(section=section)
        scores_header = self._generate_scores_header()
        section_rules = [rule for rule in self.rules if rule.section == section]
        scores_rows = [self._generate_score_row(rule.name) for rule in section_rules]
        return [section_header] + [scores_header] + scores_rows

    def _generate_scoresheet(self) -> List[List[Any]]:
        """Assembles the entire scoresheet.

        Returns
        -------
        list of list
            The scoresheet, listing all sections with rules and associated scores.
        """
        upper_section = self._generate_section(section=rl.Section.UPPER)
        lower_section = self._generate_section(section=rl.Section.LOWER)
        return upper_section + lower_section

    def output(self) -> str:
        """Gives the full scoresheet.

        Returns
        -------
        str
            The full scoresheet, in a well-formatted tabular format.
        """
        return tabulate(self._generate_scoresheet())
