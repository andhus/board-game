from __future__ import division, print_function

from abc import ABCMeta, abstractproperty, abstractmethod

import numpy


class InvalidMove(ValueError):
    pass


class InvalidGameState(ValueError):
    pass


class SquareBoardGame(object):
    """ Represent a (two player) square board game like Go, checkers etc...
    """
    __metaclass__ = ABCMeta

    # game status
    GAME_CONTINUOUS = 0
    FIRST_PLAYER_WIN = 1
    SECOND_PLAYER_WIN = 2
    DRAW = 3

    # players
    PLAYER_ONE = 1  # the starting player
    PLAYER_TWO = 2

    @abstractproperty
    def initial_game_state(self):
        raise NotImplementedError('')

    @abstractmethod
    def evaluate(self, game_state):
        """
        Parameters
        ----------
        game_state : numpy.ndarray(dtype=int)

        Returns
        -------
        status : int \in {0, 1, 2}, where:
            0 = game continues
            1 = first player win
            2 = second player win
            3 = draw
        """
        raise NotImplementedError('')

    @abstractproperty
    def position_states(self):
        """ Returns the possible states that a position can be in.
        """
        raise NotImplementedError('')

    @abstractproperty
    def moves(self):
        """ The "set" of moves possible to play sometime during

        Returns
        -------
        [str]
        """
        raise NotImplementedError('')

    def n_moves(self):
        return len(self.moves)

    @abstractmethod
    def valid_moves(self, game_state, player):
        """
        Parameters
        ----------
        game_state : ndarray(dtype=int)
        player : int \in {1, 2}
            where player 1 made first move.

        Returns
        -------
        numpy.ndarray(dtype=bool)
        """
        raise NotImplementedError('')

    def play_move(self, game_state, player, move):
        """ Verifies the move and returns the new game state, checks its status
        and valid moves for next player (if game is not finished).

        NOTE this method can be overwritten for efficiency since validating a
        move, playing it and computing status and the next valid moves often
        duplicates the same operations.

        Parameters
        ----------
        game_state : numpy.ndarray(dtype=int)
        player : int \in {1, 2}
            where player 1 made first move.
        move : int \in range(self.n_moves)

        Return
        ------
        new_game_state : numpy.ndarray(dtype=int)
        status : int
        next_player_valid_moves : numpy.ndarray(dtype=bool)
        """
        if not self.valid_moves(game_state, player)[move]:
            raise InvalidMove('This move is not valid.')

        new_game_state = self._make_move(game_state, player, move)
        status = self.evaluate(game_state)
        if status == self.GAME_CONTINUOUS:
            next_player_valid_moves = self.valid_moves(
                game_state,
                player=self._next_player(player)
            )
        else:
            next_player_valid_moves = numpy.zeros(self.n_moves()).astype(bool)

        return new_game_state, status, next_player_valid_moves

    @abstractmethod
    def _make_move(self, game_state, player, move):
        """
        Parameters
        ----------
        game_state : ndarray(dtype=int)
        player : int \in {1, 2}
            where player 1 made first move.
        move : int \in range(self.n_moves)

        Return
        ------
        new_game_state : ndarray(dtype=int)
        """
        raise NotImplementedError('')

    def _next_player(self, player):
        if player == self.PLAYER_ONE:
            return self.PLAYER_TWO
        elif player == self.PLAYER_TWO:
            return self.PLAYER_ONE
        else:
            raise ValueError('player must be (the integer) 1 or 2')

    @abstractproperty
    def board_size(self):
        """
        Return
        ------
        board_size : (int, int)
        """
        return NotImplementedError('')

from itertools import product


class NoughtsAndCrosses(SquareBoardGame):

    # position_states
    EMPTY = 0
    PLAYER_ONE_PIECE = 1
    PLAYER_TWO_PIECE = 2
    _position_states = ['empty', 'player one piece', 'player two piece']
    _board_size = (3, 3)

    def __init__(self):
        self._moves_place_coordinates = product(
            self._board_size[0],
            self.board_size[1]
        )

    @property
    def initial_game_state(self):
        return numpy.zeros(self.board_size)

    def evaluate(self, game_state):
        """ TODO
        """
        def wins(player):
            return (
                ((game_state == player).sum(axis=0) == 3).any() or
                ((game_state == player).sum(axis=1) == 3).any() or
                (game_state[[0, 1, 2], [0, 1, 2]] == player).all() or
                (game_state[[0, 1, 2], [2, 1, 0]] == player).all()
            )

        if wins(self.PLAYER_ONE):
            return self.FIRST_PLAYER_WIN
        elif wins(self.PLAYER_TWO):
            return self.SECOND_PLAYER_WIN
        elif (game_state != 0).all():
            return self.DRAW
        else:
            return self.GAME_CONTINUOUS

    @property
    def position_states(self):
        return self._position_states

    def valid_moves(self, game_state, player):
        return (game_state == 0).flatten()

    def _make_move(self, game_state, player, move):
        new_game_state = numpy.array(game_state)
        new_game_state[self._moves_place_coordinates[move]] = player

    @property
    def moves(self):
        """
        moves = [
            '(0, 0)', '(0, 1)', '(0, 2)',
            '(1, 0)', '(1, 1)', '(1, 2)',
            '(2, 0)', '(2, 1)', '(2, 2)'
        ]
        """
        moves = map(str, self._moves_place_coordinates)

        return moves

    @property
    def board_size(self):
        return self._board_size
