class IllegalDieValueError(ValueError):
    """Raised when an illegal face value is set for a die."""
    pass


class RuleAlreadyScoredError(ValueError):
    """Raised when attempting to score a previously-scored rule."""
    pass


class RuleInputValueError(ValueError):
    """Raised when rule parameters are supplied improperly."""
    pass


class DuplicateRuleNamesError(ValueError):
    """Raised when duplicate rule names are submitted in the same scoresheet."""
    pass
