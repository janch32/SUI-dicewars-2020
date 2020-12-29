import logging
import copy

from ..utils import save_state
from .utils import battle_heuristic, get_attackable, path_heuristics, simulate_battle
from .maxn import MaxN

from typing import List

from dicewars.client.ai_driver import BattleCommand, EndTurnCommand
from dicewars.client.game.board import Board
from dicewars.client.game.area import Area

class AI:
    """GOD player agent

    This agent wins everything
    """


    def __init__(self, player_name: int, board: Board, players_order: List[int]):
        self.player_name = player_name
        self.players_order = players_order
        self.logger = logging.getLogger('AI')
        self.first_attack = True
        self.area_of_interest = None
        self.path_of_interest = None
        self.start_turn = True #TODO DEBUGGING ONLY
        self.max_n = MaxN(players_order,player_name, 4)

    def search_tree(self, board : Board, active_area : Area):

        """ Recursive function for tree search
        """
        possible_targets = get_attackable(board, active_area)
        node = True
        paths = []

        if active_area.get_dice() > 1:
            for target in possible_targets:
                # Evaluate
                # If Evaluate not good pass
                h = battle_heuristic(board, active_area, target)
                #TODO DEBUG
                self.logger.info("Active: {} Target: {} Heuristics: {}".format(active_area.get_name(), target.get_name(), h))
                #TODO
                if h <= -5:
                    pass
                else:
                    node = False
                    with simulate_battle(active_area, target):
                        # Search tree with updated board
                        r_paths = self.search_tree(board, board.get_area(target.get_name()))

                    for path in r_paths:
                        path.insert(0, active_area.get_name())
                        paths.append(path)

        if node:
            return [ [active_area.get_name()] ]

        return paths


    def ai_turn(self, board: Board, nb_moves_this_turn: int, nb_turns_this_game: int, time_left: float):
        """ GOD AI agent's turn

        TODO At start get player area border area with most dices. Otherwise last used.

        While there is a lucrative attack possible, the agent will do it. Otherwise it will end its turn.
        """

        move = self.max_n.get_best_move(board, self.player_name)
        if move == None:
            return EndTurnCommand()
        return BattleCommand(move[0].get_name(), move[1].get_name())
