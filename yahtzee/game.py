from .scoring import defaults as df
from .scoring import rules as rl
from .scoring.scoresheet import Scoresheet
from .players import Player
from .dice import Die

from copy import deepcopy
from typing import List, Optional, Tuple

from simple_term_menu import TerminalMenu  # type: ignore


class Game:
    """Representation of the full game.

    Parameters
    ----------
    players : int, default 1
        Number of players for the game.
    dice : list of Die, optional
        A set of dice to use for the game.
        If not specified, defaults to a standard set of 5 six-sided dice.
    rules : list of ScoringRule, optional
        A set of scoring rules to use in the game.
        If not specified, defaults to the usual set of Yahtzee rules:

        - Aces (Ones): sum of all 1s
        - Twos: sum of all 2s
        - Threes: sum of all 3s
        - Fours: sum of all 4s
        - Fives: sum of all 5s
        - Sixes: sum of all 6s
        - Three-of-a-Kind: total of all dice
        - Four-of-a-Kind: total of all dice
        - Full House (Two-of-a-Kind & Three-of-a-Kind): 25 points
        - Small Straight (four dice sequence): 30 points
        - Large Straight (five dice sequence): 40 points
        - Yahtzee (Five-of-a-Kind): 50 points
        - Chance (any five dice): total of all dice

    bonuses : list of BonusRule, optional
        A set of bonus rules to use in the game.
        If not specified, defaults to the usual bonus rules:

        - Upper Section Bonus: 35 points if the upper section score is at least 63

    yahtzee_bonus : YahtzeeBonusRule, optional
        A bonus rule for scoring the Yahtzee bonus in the game.
        If not specified, defaults to the usual Yahtzee bonus rule:

        - Yahtzee Bonus: 100 points per additional Yahtzee

    Attributes
    ----------
    dice : list of Die
        The dice to be rolled in the game.
    rules : list of ScoringRule
        The rules to be scored in the game.
    bonuses : list of BonusRule
        The bonus rules to be scored in the game.
    yahtzee_bonus : YahtzeeBonusRule
        The Yahtzee bonus rule to be scored in the game.
    scoresheet : Scoresheet
        The scoresheet to be used by each player, which contains the various rules
        and bonuses, along with the player's scores for those rules.
    players : list of Player
        The players in the game.
    """
    def __init__(
        self,
        players: int = 1,
        dice: Optional[List[Die]] = None,
        rules: Optional[List[rl.ScoringRule]] = None,
        bonuses: Optional[List[rl.BonusRule]] = None,
        yahtzee_bonus: Optional[rl.YahtzeeBonusRule] = None
    ):
        self.dice = dice if dice else df.DEFAULT_DICE
        self.rules = rules if rules else df.DEFAULT_RULES
        self.bonuses: List[rl.BonusRule] = (
            bonuses if bonuses else df.DEFAULT_UPPER_BONUSES
        )
        self.yahtzee_bonus = (
            yahtzee_bonus if yahtzee_bonus else df.DEFAULT_YAHTZEE_BONUS
        )
        self.scoresheet = Scoresheet(
            rules=self.rules,
            bonuses=self.bonuses,
            yahtzee_bonus=self.yahtzee_bonus
        )
        self.players = [
            Player(scoresheet=deepcopy(self.scoresheet), dice=deepcopy(self.dice))
            for _ in range(players)
        ]

    def reroll_dice(self, player: Player) -> None:
        """Rerolls a subset of the player's dice, based on user input.

        Parameters
        ----------
        player : Player
            Which player is currently rolling.
        """
        dice_to_reroll = _pick_reroll_dice(dice=player.dice)

        # if no dice are selected, the index should be out-of-range
        if max(dice_to_reroll) < len(player.dice):
            player.roll_dice(dice=dice_to_reroll)

        return None


def _pick_reroll_dice(dice: List[Die]) -> List[int]:
    """Gets user input for which dice to re-roll.

    Parameters
    ----------
    dice : list of Die
        The set of dice to choose from.

    Returns
    -------
    dice : list of int
        Indexes of dice to re-roll.
        If no dice are selected, returns an index that is out-of-bounds for
        the dice list.
    """
    dice_choices = [str(die.showing_face) for die in dice]
    dice_choices = dice_choices + ["None"]

    dice_menu = TerminalMenu(
        dice_choices,
        title="Pick which dice to re-roll (if any).",
        multi_select=True,
        show_multi_select_hint=True,
        multi_select_select_on_accept=False,
        cursor_index=len(dice_choices),
    )

    selected_indexes: Tuple[int] = dice_menu.show()

    return list(selected_indexes)
