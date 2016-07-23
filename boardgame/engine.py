from __future__ import division, print_function

from clint.textui.prompt import query
from clint.textui.validators import OptionValidator

import numpy


class CMDLineEngine(object):
    """
    Parameters
    ----------
    definition : definition.SquareBoardGameDefinition
    """
    def __init__(
        self,
        definition,
        cmd_line_game_state,
        player_one='player one',
        player_two='player two',
    ):
        self.definition = definition
        self.cmd_line_game_state = cmd_line_game_state
        self.player_names = {
            definition.PLAYER_ONE: player_one,
            definition.PLAYER_TWO: player_two,
        }

    def start(self):
        game_state = self.definition.initial_game_state()
        player = self.definition.PLAYER_ONE
        status = self.definition.GAME_CONTINUOUS
        print('Started new game')
        print(self.cmd_line_game_state(game_state))
        while status == self.definition.GAME_CONTINUOUS:
            move_name = query(
                prompt='\n{} - make a move:'.format(self.player_names[player]),
                validators=[
                    OptionValidator(
                        options=self.definition.valid_move_names(
                            game_state,
                            player
                        )
                    )
                ]
            )
            game_state, status, next_player_valid_moves = \
                self.definition.play_move_name(game_state, player, move_name)
            print(self.cmd_line_game_state(game_state))
            player = self.definition.next_player(player)

        print('\nGAME OVER - ', end='')
        if status == self.definition.DRAW:
            print('It\'s a draw.')
        elif status == self.definition.PLAYER_ONE_WIN:
            print('{} WINS!'.format(
                self.player_names[self.definition.PLAYER_ONE])
            )
        elif status == self.definition.PLAYER_TWO_WIN:
            print('{} WINS!'.format(
                self.player_names[self.definition.PLAYER_TWO])
            )
        else:
            raise Exception('Game finished with status {}'.format(status))


class RLEngine(object):

    def __init__(
        self,
        definition
    ):
        self.definition = definition
        self.reset()

    def reset(self):
        self.game_state = self.definition.initial_game_state()
        self.next_player = self.definition.PLAYER_ONE
        self.valid_moves = self.definition.valid_moves(
            self.game_state,
            self.next_player
        )
        self.status = self.definition.GAME_CONTINUOUS
        self.game_states = []
        self.player_to_moves = {
            self.definition.PLAYER_ONE: [],
            self.definition.PLAYER_TWO: []
        }

    def play_move(self, move):
        self.player_to_moves[self.next_player].append(move)
        (
            self.game_state,
            self.status,
            self.valid_moves
        ) = self.definition.play_move(
            self.game_state,
            self.next_player,
            move
        )
        self.game_states.append(numpy.array(self.game_state))
        self.next_player = self.definition.next_player(self.next_player)
