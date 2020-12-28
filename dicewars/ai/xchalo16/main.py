import logging
import copy

from ..utils import possible_attacks, save_state
from .utils import battle_heuristic, get_attackable, path_heuristics
from .simulatebattle import simulate_battle

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
                if h <= -3:
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

        start_area = None
        focus_area = None
        best_heuristics = -1000

        if self.start_turn:
            self.start_turn = False
            with open('debugxchalo16.save', 'wb') as f:
                    save_state(f, board, self.player_name, self.players_order)

        a = [ar.get_name() for ar in board.get_player_border(self.player_name)]
        all_a = [ar.get_name() for ar in board.get_player_areas(self.player_name)]
        #TODO DEBUG
        self.logger.info("Border Areas: {}".format(a))

        if self.path_of_interest is not None and len(self.path_of_interest) <= 1:
            self.first_attack = True

        if self.area_of_interest is not None and self.area_of_interest.get_name() not in all_a:
            self.first_attack = True

        if not a:
            self.start_turn = True
            self.first_attack = True
            return EndTurnCommand()

        self.logger.info("First Turn: {}".format(self.first_attack))
        if self.first_attack:
            for area in board.get_player_border(self.player_name):
                if start_area is None:
                    start_area = copy.deepcopy(area)
                else:
                    if area.get_dice() > start_area.get_dice():
                        start_area = copy.deepcopy(area)
            self.first_attack = False

            #TODO DEBUG
            self.logger.info("Starting area: {}".format(start_area.get_name()))

            paths = self.search_tree(board, start_area)

            if not paths:
                self.first_attack = True
                self.start_turn = True
                return EndTurnCommand()

            #TODO DEBUG
            self.logger.info(paths)

            for path in paths:
                if len(path) > 1:
                    p_h = path_heuristics(board, path)
                    #TODO DEBUG
                    self.logger.info("Evaluate attack to: {} with h={}".format(path[1],p_h))
                    if p_h > best_heuristics:
                        focus_area = path[1]
                        best_heuristics = p_h
                        self.path_of_interest = path[1:]
        else:
            start_area = self.area_of_interest
            focus_area = self.path_of_interest[1]
            self.path_of_interest = self.path_of_interest[1:]
            #TODO DEBUG
            self.logger.info("Will go on to path: {}".format(self.path_of_interest))

        #TODO DEBUG
        self.logger.info("Attack to: {}".format(focus_area))

        if focus_area is None:
            self.start_turn = True
            self.first_attack = True
            return EndTurnCommand()

        self.area_of_interest = board.get_area(focus_area)
        #TODO DEBUG
        self.logger.info("AOI: {}".format(self.area_of_interest.get_name()))

        return BattleCommand(start_area.get_name(), focus_area)



