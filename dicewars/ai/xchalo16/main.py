import logging
import random

from ..utils import possible_attacks, save_state
from .utils import best_sdc_attack, is_acceptable_sdc_attack

from dicewars.client.ai_driver import BattleCommand, EndTurnCommand
from dicewars.client.game import board

class AI:
    """GOD player agent

    This agent wins everything
    """

    def __init__(self, player_name: str, board: board.Board, players_order):
        """
        Parameters
        ----------
        game : Game
        """
        self.player_name = player_name
        self.players_order = players_order
        self.logger = logging.getLogger('AI')

        self.first_attack = True
        self.area_of_interest = None

    def get_attackable(active_area, neighbours):
        attackable = []
        for nb in neighbours:
            if active_area.get_owner_name() != nb.get_owner_name():
                attackable.append(nb)

        return attackable

    def search_tree(board, active_area, player):
        """ Recursive function for tree search
        """
        possible_moves = get_attackable(active_area, active_area.get_adjacent_areas())

        for move in possible_moves:
            # Board update
            # Search tree with updated board

    def ai_turn(self, board: board.Board, nb_moves_this_turn, nb_turns_this_game, time_left):
        """ GOD AI agent's turn

        TODO At start get player area border area with most dices. Otherwise last used.

        While there is a lucrative attack possible, the agent will do it. Otherwise it will end its turn.
        """

        start_area = None
        focus_move = None
        best_move_heuristic = 0

        if self.first_attack:
            for area in board.get_player_border(self.player_name):
                if start_area is None:
                    start_area = area
                else:
                    if area.get_dice() > start_area.get_dice():
                        start_area = area
            self.first_attack = False
        else:
            start_area = self.area_of_interest

        moves = get_attackable(start_area, start_area.get_adjacent_areas())

        for move in moves:
                # Evaluate state
                # Make new path
                # Call recursive function

