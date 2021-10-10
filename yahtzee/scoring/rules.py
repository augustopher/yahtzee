from abc import ABC
from abc import abstractmethod
from enum import Enum
from typing import List
from typing import Optional
from typing import Sequence

from . import validators as vl
from .. import errors as er
from ..dice import Die

# scores that are constant, regardless of dice values
SCORE_FULL_HOUSE: int = 25
SCORE_SMALL_STRAIGHT: int = 30
SCORE_LARGE_STRAIGHT: int = 40
SCORE_YAHTZEE: int = 50

BONUS_UPPER_SCORE = 35
BONUS_UPPER_THRESHOLD = 63
BONUS_YAHTZEE_SCORE = 100
BONUS_LOWER_SCORE = BONUS_YAHTZEE_SCORE


class Section(Enum):
    """Values for the sections of the scoresheet,
    used to organize different rules and bonuses."""
    UPPER: str = "upper"
    LOWER: str = "lower"


class ScoringRule(ABC):
    """Generic scoring rule.

    Parameters
    ----------
    name : str
        Name to identify the rule.
    section : Section
        Section of the scoresheet which the rule belongs to.

    Attributes
    ----------
    name : str
        Name of the rule.
    section : Section
        Scoresheet section which the rule belongs to.
    rule_score : int
        Current scored value for the rule.
        Returns `None` until the rule is scored.
    """
    def __init__(self, name: str, section: Section):
        self.name = name
        self.section = section
        self.rule_score: Optional[int] = None

    def score(self, dice: Sequence[Optional[Die]]) -> None:
        """Method to score a given set of dice.

        Parameters
        ----------
        dice : list of Die
            A set of dice to score.

        Raises
        ------
        RuleAlreadyScoredError
            If the rule has already been scored.
        """
        if self._check_rule_not_scored():
            self.rule_score = self._score_dice(dice=dice)
        else:
            raise er.RuleAlreadyScoredError(
                f"Rule {self.name} has already been scored."
            )

    @abstractmethod
    def validate(self, dice: Sequence[Optional[Die]]) -> bool:
        """Method to check that a desired pattern
        or other trait is present in the given dice.

        Parameters
        ----------
        dice : list of Die
            A set of dice to check.

        Returns
        -------
        bool
            Whether the dice are valid for the given rule or not.
        """

    @abstractmethod
    def _score_dice(self, dice: Sequence[Optional[Die]]) -> int:
        """Method to score a given set of dice.

        Parameters
        ----------
        dice : list of Die
            A set of dice to score.

        Returns
        -------
        int
            The score resulting from the dice, based on the rule.
        """

    def _check_rule_not_scored(self) -> bool:
        """Verifies that the rule has not already been scored.

        Returns
        -------
        bool
            Whether the rule has been scored or not.
            True if not scored, False if scored.
        """
        return self.rule_score is None


class ConstantPatternScoringRule(ScoringRule):
    """Generic scoring rule, which looks for a particular pattern,
    and has a constant score value.

    Parameters
    ----------
    name : str
        Name to identify the rule.
    section : Section
        Section of the scoresheet which the rule belongs to.
    score_value : int
        The value of the rule if scored with a valid set of dice.

    Attributes
    ----------
    name : str
        Name of the rule.
    section : Section
        Scoresheet section which the rule belongs to.
    rule_score : int
        Current scored value for the rule.
        Returns `None` until the rule is scored.
    score_value : int
        The value of the rule if scored with a valid set of dice.
    """
    def __init__(self, name: str, section: Section, score_value: int):
        super().__init__(name=name, section=section)
        self.score_value = score_value

    def _score_dice(self, dice: Sequence[Optional[Die]]) -> int:
        """Method to score a given set of dice.

        Parameters
        ----------
        dice : list of Die
            A set of dice to score.

        Returns
        -------
        int
            The score resulting from the dice, based on the rule.
        """
        if self.validate(dice=dice):
            return self.score_value
        return 0


class VariablePatternScoringRule(ScoringRule):
    """Generic scoring rule, which looks for a particular pattern,
    and has a variable score value.

    Parameters
    ----------
    name : str
        Name to identify the rule.
    section : Section
        Section of the scoresheet which the rule belongs to.

    Attributes
    ----------
    name : str
        Name of the rule.
    section : Section
        Scoresheet section which the rule belongs to.
    rule_score : int
        Current scored value for the rule.
        Returns `None` until the rule is scored.
    """
    def __init__(self, name: str, section: Section):
        super().__init__(name=name, section=section)

    def _score_dice(self, dice: Sequence[Optional[Die]]) -> int:
        """Method to score a given set of dice.

        Parameters
        ----------
        dice : list of Die
            A set of dice to score.

        Returns
        -------
        int
            The score resulting from the dice, based on the rule.
        """
        if self.validate(dice=dice):
            return self._scoring_func(dice=dice)
        return 0

    @abstractmethod
    def _scoring_func(self, dice: Sequence[Optional[Die]]) -> int:
        """Method for calculating a dice-dependent score.

        Parameters
        ----------
        dice : list of Die
            A set of dice to score.

        Returns
        -------
        int
            The score resulting from the dice, based on the rule.
        """


class ChanceScoringRule(VariablePatternScoringRule):
    """Rules which take any 5 dice.

    Parameters
    ----------
    name : str
        Name to identify the rule.
    section : Section, default LOWER
        Section of the scoresheet which the rule belongs to.

    Attributes
    ----------
    name : str
        Name of the rule.
    section : Section
        Scoresheet section which the rule belongs to.
    rule_score : int
        Current scored value for the rule.
        Returns `None` until the rule is scored.
    """
    def __init__(self, name: str, section: Section = Section.LOWER):
        super().__init__(name=name, section=section)

    def _scoring_func(self, dice: Sequence[Optional[Die]]) -> int:
        """Method for calculating a dice-dependent score.
        Scores as the sum of all showing faces.

        Parameters
        ----------
        dice : list of Die
            A set of dice to score.

        Returns
        -------
        int
            The score resulting from the dice, based on the rule.
        """
        return _sum_all_showing_faces(dice=dice)

    def validate(self, dice: Sequence[Optional[Die]]) -> bool:
        """Method to check that the desired pattern
        is present in the given dice.
        Always validates, since Chance can score for any dice.

        Parameters
        ----------
        dice : list of Die
            A set of dice to check.

        Returns
        -------
        bool
            Whether the dice are valid for the given rule or not.
            Since a Chance is just scoring any set of dice,
            this will always return `True`.
        """
        # Any dice combo is valid
        return True


class MultiplesScoringRule(VariablePatternScoringRule):
    """Rules which look for multiple dice with a specific face value.

    Parameters
    ----------
    name : str
        Name to identify the rule.
    section : Section, default UPPER
        Section of the scoresheet which the rule belongs to.
    face_value : int
        Face value needed on a die to be counted in this rule's score.

    Attributes
    ----------
    name : str
        Name of the rule.
    section : Section
        Scoresheet section which the rule belongs to.
    rule_score : int
        Current scored value for the rule.
        Returns `None` until the rule is scored.
    face_value : int
        Face value needed on a die to be counted in this rule's score.
    """
    def __init__(self, name: str, face_value: int, section: Section = Section.UPPER):
        super().__init__(name=name, section=section)
        self.face_value = face_value

    def _scoring_func(self, dice: Sequence[Optional[Die]]) -> int:
        """Method for calculating a dice-dependent score.
        Scores as the sum of all showing faces which match the given face value.

        Parameters
        ----------
        dice : list of Die
            A set of dice to score.

        Returns
        -------
        int
            The score resulting from the dice, based on the rule.
        """
        return _sum_matching_faces(dice=dice, face_value=self.face_value)

    def validate(self, dice: Sequence[Optional[Die]]) -> bool:
        """Method to check that the desired pattern
        is present in the given dice.
        Always validates, since Multiples can score for any dice.

        Parameters
        ----------
        dice : list of Die
            A set of dice to check.

        Returns
        -------
        bool
            Whether the dice are valid for the given rule or not.
            Since a Multiple will naturally score ``0`` with no matching dice,
            this will always return `True`.
        """
        # Any dice combo is valid
        return True


class NofKindScoringRule(VariablePatternScoringRule):
    """Rules which look for n-of-a-kind of a face value, without explicitly
    specifying the desired face value.

    Parameters
    ----------
    name : str
        Name to identify the rule.
    section : Section, default LOWER
        Section of the scoresheet which the rule belongs to.
    n : int
        Number of matching dice needed for this rule - the "n" in "n-of-a-kind".

    Attributes
    ----------
    name : str
        Name of the rule.
    section : Section
        Scoresheet section which the rule belongs to.
    rule_score : int
        Current scored value for the rule.
        Returns `None` until the rule is scored.
    n : int
        Number of matching dice needed for this rule - the "n" in "n-of-a-kind".
    """
    def __init__(self, name: str, n: int, section: Section = Section.LOWER):
        super().__init__(name=name, section=section)
        self.n = n

    def _scoring_func(self, dice: Sequence[Optional[Die]]) -> int:
        """Method for calculating a dice-dependent score.

        Parameters
        ----------
        dice : list of Die
            A set of dice to score.

        Returns
        -------
        int
            The score resulting from the dice, based on the rule.
        """
        return _sum_all_showing_faces(dice=dice)

    def validate(self, dice: Sequence[Optional[Die]]) -> bool:
        """Method to check that the desired pattern
        is present in the given dice.
        Validates if an n-of-a-kind is present,
        or if any m-of-a-kind is present (``m > n``).

        Parameters
        ----------
        dice : list of Die
            A set of dice to check.

        Returns
        -------
        bool
            Whether the dice are valid for the given rule or not.
            Since m-of-a-kinds (``m > n``) are still valid for a given n,
            returns `True` if any m-of-a-kind is present, ``m >= n``.
        """
        n_or_more_kind_present = [
            vl.validate_nofkind(dice=dice, n=x)
            for x in range(self.n, len(dice) + 1)
        ]
        return any(n_or_more_kind_present)


class YahtzeeScoringRule(ConstantPatternScoringRule):
    """Rules which look for a Yahtzee (5-of-a-kind).

    Parameters
    ----------
    name : str
        Name to identify the rule.
    section : Section, default LOWER
        Section of the scoresheet which the rule belongs to.
    score_value : int, default SCORE_YAHTZEE
        The value of the rule if scored with a valid set of dice.

    Attributes
    ----------
    name : str
        Name of the rule.
    section : Section
        Scoresheet section which the rule belongs to.
    rule_score : int
        Current scored value for the rule.
        Returns `None` until the rule is scored.
    score_value : int
        The value of the rule if scored with a valid set of dice.
    """
    def __init__(
        self,
        name: str,
        section: Section = Section.LOWER,
        score_value: int = SCORE_YAHTZEE
    ):
        super().__init__(name=name, section=section, score_value=score_value)

    def validate(self, dice: Sequence[Optional[Die]]) -> bool:
        """Method to check that the desired pattern
        is present in the given dice.
        Validates if a Yahtzee (5-of-a-kind) is present.

        Parameters
        ----------
        dice : list of Die
            A set of dice to check.

        Returns
        -------
        bool
            Whether the dice are valid for the given rule or not.
            Returns `True` if all dice are the same.
        """
        return vl.validate_nofkind(dice=dice, n=len(dice))


class FullHouseScoringRule(ConstantPatternScoringRule):
    """Rules which look for a full house (m-of-a-kind and n-of-a-kind, ``m > n``).

    Parameters
    ----------
    name : str
        Name to identify the rule.
    section : Section, default LOWER
        Section of the scoresheet which the rule belongs to.
    score_value : int, default SCORE_FULL_HOUSE
        The value of the rule if scored with a valid set of dice.
    large_n : int, default 3
        N for the larger n-of-a-kind required for the full house.
    small_n : int, default 2
        N for the smaller n-of-a-kind required for the full house.

    Attributes
    ----------
    name : str
        Name of the rule.
    section : Section
        Scoresheet section which the rule belongs to.
    rule_score : int
        Current scored value for the rule.
        Returns `None` until the rule is scored.
    score_value : int
        The value of the rule if scored with a valid set of dice.
    large_n : int
        N for the larger n-of-a-kind required for the full house.
    small_n : int
        N for the smaller n-of-a-kind required for the full house.
    """
    def __init__(
        self,
        name: str,
        section: Section = Section.LOWER,
        large_n: int = 3,
        small_n: int = 2,
        score_value: int = SCORE_FULL_HOUSE
    ):
        super().__init__(name=name, section=section, score_value=score_value)
        self.large_n = large_n
        self.small_n = small_n

    def validate(self, dice: Sequence[Optional[Die]]) -> bool:
        """Method to check that the desired pattern
        is present in the given dice.
        Validates if a full house (m-of-a-kind and n-of-a-kind, ``m > n``) is present.

        Parameters
        ----------
        dice : list of Die
            A set of dice to check.

        Returns
        -------
        bool
            Whether the dice are valid for the given rule or not.
            Returns `True` if an two n-of-a-kinds are present,
            of sizes `large_n` and `small_n`.
        """
        return vl.validate_full_house(
            dice=dice,
            large_n=self.large_n,
            small_n=self.small_n
        )


class LargeStraightScoringRule(ConstantPatternScoringRule):
    """Rules which look for a large straight (5 dice sequence).

    Parameters
    ----------
    name : str
        Name to identify the rule.
    section : Section, default LOWER
        Section of the scoresheet which the rule belongs to.
    score_value : int, default SCORE_LARGE_STRAIGHT
        The value of the rule if scored with a valid set of dice.

    Attributes
    ----------
    name : str
        Name of the rule.
    section : Section
        Scoresheet section which the rule belongs to.
    rule_score : int
        Current scored value for the rule.
        Returns `None` until the rule is scored.
    score_value : int
        The value of the rule if scored with a valid set of dice.
    """
    def __init__(
        self,
        name: str,
        section: Section = Section.LOWER,
        score_value: int = SCORE_LARGE_STRAIGHT
    ):
        super().__init__(name=name, section=section, score_value=score_value)

    def validate(self, dice: Sequence[Optional[Die]]) -> bool:
        """Method to check that the desired pattern
        is present in the given dice.
        Validates if a large straight (5 consecutive values in 5 dice) is present.

        Parameters
        ----------
        dice : list of Die
            A set of dice to check.

        Returns
        -------
        bool
            Whether the dice are valid for the given rule or not.
            Returns `True` if all dice are sequential and unique.
        """
        return vl.validate_large_straight(dice=dice)


class SmallStraightScoringRule(ConstantPatternScoringRule):
    """Rules which look for a small straight (4 dice sequence).

    Parameters
    ----------
    name : str
        Name to identify the rule.
    section : Section, default LOWER
        Section of the scoresheet which the rule belongs to.
    score_value : int, default SCORE_SMALL_STRAIGHT
        The value of the rule if scored with a valid set of dice.

    Attributes
    ----------
    name : str
        Name of the rule.
    section : Section
        Scoresheet section which the rule belongs to.
    rule_score : int
        Current scored value for the rule.
        Returns `None` until the rule is scored.
    score_value : int
        The value of the rule if scored with a valid set of dice.
    """
    def __init__(
        self,
        name: str,
        section: Section = Section.LOWER,
        score_value: int = SCORE_SMALL_STRAIGHT
    ):
        super().__init__(name=name, section=section, score_value=score_value)

    def validate(self, dice: Sequence[Optional[Die]]) -> bool:
        """Method to check that the desired pattern
        is present in the given dice.
        Validates if a small straight (4 consecutive values in 5 dice) is present.

        Parameters
        ----------
        dice : list of Die
            A set of dice to check.

        Returns
        -------
        bool
            Whether the dice are valid for the given rule or not.
            Returns `True` if all-but-one of the dice are sequential and unique.
        """
        return vl.validate_small_straight(dice=dice)


def _sum_all_showing_faces(dice: Sequence[Optional[Die]]) -> int:
    """Sums all the showing faces for a set of dice.

    Parameters
    ----------
    dice : list of Die
        A set of dice to sum.

    Returns
    -------
    int
        The sum of all showing faces for the given dice.
    """
    return sum([die.showing_face for die in dice if die])


def _sum_matching_faces(dice: Sequence[Optional[Die]], face_value: int) -> int:
    """Sums all the showing faces which match a given value, for a set of dice.

    Parameters
    ----------
    dice : list of Die
        A set of dice to sum.
    face_value: int
        The value to match on each die's showing face.

    Returns
    -------
    int
        The sum of all showing faces for the given dice
        whose showing face matches the given value.
    """
    matching_dice = vl.find_matching_dice(dice=dice, face_value=face_value)
    return _sum_all_showing_faces(dice=matching_dice)


class BonusRule(ABC):
    """Generic rule for scoring a bonus.

    Parameters
    ----------
    name : str
        Name to identify the rule.
    section : Section
        Section of the scoresheet which the rule belongs to.
    bonus_value : int
        Value used to score the bonus.
        Depending on the specific type of bonus, this is either a constant score,
        or is multipled with a counter to get the total bonus score.
    counter : int
        Tally used in scoring the bonus.
        Depending on the specific type of bonus, this is either compared against a
        threshold value, or is multiplied with the `bonus_value` to get the total
        bonus score.
    req_rules : list of ScoringRule, optional
        Rules which influence the counter.

    Attributes
    ----------
    name : str
        Name of the rule.
    section : Section
        Scoresheet section which the rule belongs to.
    rule_score : int
        Current scored value for the rule.
        Returns `None` until the rule is scored.
    bonus_value : int
        Value used to score the bonus.
    counter : int
        Tally used in scoring the bonus.
    req_rules : list of ScoringRule
        Rules which influence the counter.
    """
    def __init__(
        self,
        name: str,
        section: Section,
        bonus_value: int,
        counter: int = 0,
        req_rules: Optional[List[ScoringRule]] = None
    ):
        self.name = name
        self.section = section
        self.bonus_value = bonus_value
        self.counter = counter
        self.req_rules = req_rules
        self.rule_score: Optional[int] = None

    def increment(self, amt: int = 1) -> None:
        """Method to increment the internal counter.

        Parameters
        ----------
        amt : int
            Amount by which to increment `counter`.
            Defaults to 1.
        """
        self.counter += amt

    def score(self) -> None:
        """Method to score a given bonus, and update the associated score value.

        Raises
        ------
        RuleAlreadyScoredError
            If the rule has already been scored.
        """
        if self._check_rule_not_scored():
            self.rule_score = self._score_bonus()
        else:
            raise er.RuleAlreadyScoredError(
                f"Rule {self.name} has already been scored."
            )

    @abstractmethod
    def _score_bonus(self) -> int:
        """Method to score a bonus rule.

        Returns
        -------
        int
            Score returned from the bonus scoring logic.
        """

    def _check_rule_not_scored(self) -> bool:
        """Verifies that the rule has not already been scored.

        Returns
        -------
        bool
            Whether or not the rule has been scored yet.
            Returns `True` if not scored, `False` if scored.
        """
        return self.rule_score is None


class ThresholdBonusRule(BonusRule):
    """Rule for a bonus of which gives points for exceeding a threshold.

    Parameters
    ----------
    name : str
        Name to identify the rule.
    section : Section, default UPPER
        Section of the scoresheet which the rule belongs to.
    bonus_value : int, default BONUS_UPPER_SCORE
        Value used to score the bonus.
        Depending on the specific type of bonus, this is either a constant score,
        or is multipled with a counter to get the total bonus score.
    counter : int
        Tally used in scoring the bonus.
        Depending on the specific type of bonus, this is either compared against a
        threshold value, or is multiplied with the `bonus_value` to get the total
        bonus score.
    req_rules : list of ScoringRule, optional
        Rules which influence the counter.
    threshold : int, default BONUS_UPPER_THRESHOLD
        Threshold to determine if bonus is awarded.

    Attributes
    ----------
    name : str
        Name of the rule.
    section : Section
        Scoresheet section which the rule belongs to.
    rule_score : int
        Current scored value for the rule.
        Returns `None` until the rule is scored.
    bonus_value : int
        Value used to score the bonus.
    counter : int
        Tally used in scoring the bonus.
    req_rules : list of ScoringRule
        Rules which influence the counter.
    threshold : int
        Threshold to determine if bonus is awarded.
    """
    def __init__(
        self,
        name: str,
        section: Section = Section.UPPER,
        threshold: int = BONUS_UPPER_THRESHOLD,
        bonus_value: int = BONUS_UPPER_SCORE,
        counter: int = 0,
        req_rules: Optional[List[ScoringRule]] = None
    ):
        super().__init__(
            name=name,
            section=section,
            bonus_value=bonus_value,
            counter=counter,
            req_rules=req_rules
        )
        self.threshold = threshold

    def _score_bonus(self) -> int:
        """Method to score a threshold bonus rule.
        Scores as the bonus value if the counter meets the threshold, 0 otherwise.

        Returns
        -------
        int
            Score returned from the bonus scoring logic.
            If `counter` meets `threshold`, return `bonus_value`, otherwise ``0``.
        """
        if self.counter >= self.threshold:
            return self.bonus_value

        return 0


class CountBonusRule(BonusRule):
    """Rule for a bonus which gives a point value per a count of something.

    Parameters
    ----------
    name : str
        Name to identify the rule.
    section : Section, default LOWER
        Section of the scoresheet which the rule belongs to.
    bonus_value : int, default BONUS_LOWER_SCORE
        Value used to score the bonus.
        Depending on the specific type of bonus, this is either a constant score,
        or is multipled with a counter to get the total bonus score.
    counter : int
        Tally used in scoring the bonus.
        Depending on the specific type of bonus, this is either compared against a
        threshold value, or is multiplied with the `bonus_value` to get the total
        bonus score.
    req_rules : list of ScoringRule, optional
        Rules which influence the counter.

    Attributes
    ----------
    name : str
        Name of the rule.
    section : Section
        Scoresheet section which the rule belongs to.
    rule_score : int
        Current scored value for the rule.
        Returns `None` until the rule is scored.
    bonus_value : int
        Value used to score the bonus.
    counter : int
        Tally used in scoring the bonus.
    req_rules : list of ScoringRule
        Rules which influence the counter.
    """
    def __init__(
        self,
        name: str,
        section: Section = Section.LOWER,
        bonus_value: int = BONUS_LOWER_SCORE,
        counter: int = 0,
        req_rules: Optional[List[ScoringRule]] = None,
    ):
        super().__init__(
            name=name,
            section=section,
            bonus_value=bonus_value,
            counter=counter,
            req_rules=req_rules
        )

    def _score_bonus(self) -> int:
        """Method to score a count-based bonus.
        Scores as a counter times the bonus value.

        Returns
        -------
        int
            Score returned from the bonus scoring logic.
            Simply `counter` times `bonus_value`.
        """
        return self.counter * self.bonus_value


class YahtzeeBonusRule(CountBonusRule):
    """Counting bonus rule, specifically for additional Yahtzees rolled after
    a `YahtzeeScoringRule`  has been scored.

    Parameters
    ----------
    name : str
        Name to identify the rule.
    section : Section, default LOWER
        Section of the scoresheet which the rule belongs to.
    bonus_value : int, default BONUS_YAHTZEE_SCORE
        Value used to score the bonus.
        Depending on the specific type of bonus, this is either a constant score,
        or is multipled with a counter to get the total bonus score.
    counter : int
        Tally used in scoring the bonus.
        Depending on the specific type of bonus, this is either compared against a
        threshold value, or is multiplied with the `bonus_value` to get the total
        bonus score.
    req_rules : list of ScoringRule, optional
        Rules which influence the counter.
    yahtzee_rule : YahtzeeScoringRule
        The Yahtzee rule associated with the bonus.
        Used to check if a Yahtzee has already been scored,
        which impacts how the bonus is scored.

    Attributes
    ----------
    name : str
        Name of the rule.
    section : Section
        Scoresheet section which the rule belongs to.
    rule_score : int
        Current scored value for the rule.
        Returns `None` until the rule is scored.
    bonus_value : int
        Value used to score the bonus.
    counter : int
        Tally used in scoring the bonus.
    req_rules : list of ScoringRule
        Rules which influence the counter.
    yahtzee_rule : YahtzeeScoringRule
        The Yahtzee rule associated with the bonus.
    """
    def __init__(
        self,
        name: str,
        yahtzee_rule: YahtzeeScoringRule,
        bonus_value: int = BONUS_YAHTZEE_SCORE,
        section: Section = Section.LOWER,
        counter: int = 0,
    ):
        super().__init__(
            name=name,
            section=section,
            bonus_value=bonus_value,
            counter=counter,
            req_rules=None
        )
        self.yahtzee_rule = yahtzee_rule
