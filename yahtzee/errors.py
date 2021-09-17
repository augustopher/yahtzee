class IllegalDieValueError(ValueError):
    """Raised when an illegal face value is set for a die."""
    ...


class RuleAlreadyScoredError(ValueError):
    """Raised when attempting to score a previously-scored rule."""
    ...


class RuleInputValueError(ValueError):
    """Raised when rule parameters are supplied improperly."""
    ...


class DuplicateRuleNamesError(ValueError):
    """Raised when duplicate rule names are submitted in the same scoresheet."""
    ...
