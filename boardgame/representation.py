from __future__ import division, print_function

from definition import NoughtsAndCrosses


class NoughtsAndCrossesCMDLine():
    # TODO make general for "single piece" board games...
    _board_template = (
        "    0   1   2\n"
        "0 | {} | {} | {} |\n"
        "1 | {} | {} | {} |\n"
        "2 | {} | {} | {} |"
    )

    def _symbol(self, position_state):
        if position_state == NoughtsAndCrosses.EMPTY:
            return ' '
        if position_state == NoughtsAndCrosses.PLAYER_ONE:
            return 'x'
        if position_state == NoughtsAndCrosses.PLAYER_TWO:
            return 'o'

    def __call__(self, game_state):
        """
        Parameters
        ----------
        game_state : numpy.ndarray(shape(3, 3), dtype_int)
        """
        symbols = map(
            self._symbol,
            game_state.flatten()
        )
        representation_str = self._board_template.format(*symbols)

        return representation_str