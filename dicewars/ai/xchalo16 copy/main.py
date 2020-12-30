from typing import List
from dicewars.client.ai_driver import BattleCommand, EndTurnCommand
from dicewars.client.game.board import Board

from .maxn import MaxN

class AI:
    """GOD player agent

    This agent wins everything
    """

    def __init__(self, player_name: int, board: Board, players_order: List[int]):
        self.player_name = player_name
        self.players_order = players_order
        self.max_n = MaxN(players_order)

    def ai_turn(self, board: Board, nb_moves_this_turn: int, nb_turns_this_game: int, time_left: float):
        """ GOD AI agent's turn

        TODO At start get player area border area with most dices. Otherwise last used.

        While there is a lucrative attack possible, the agent will do it. Otherwise it will end its turn.
        """

        #if time_left > 8:
        #    self.max_n.depth_limit = 8
        #if time_left > 5:
        #    self.max_n.depth_limit = 4
        #else:
        #    self.max_n.depth_limit = 1

        move = self.max_n.get_best_move(board, self.player_name)
        if move == None:
            return EndTurnCommand()
        return BattleCommand(move[0].get_name(), move[1].get_name())
