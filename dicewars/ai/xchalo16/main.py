import logging
import copy

from ..utils import possible_attacks
from .utils import battle_heuristic, get_attackable
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
                if False:
                    pass
                else:
                    node = False
                    with simulate_battle(active_area, target):
                        # Search tree with updated board
                        r_paths = self.search_tree(board, board.get_area(active_area.get_name()))

                    for path in r_paths:
                        path.insert(0, active_area.get_name())
                        paths.append(path)

            return paths

        if node:
            return [ [active_area.get_name()] ]


    def ai_turn(self, board: Board, nb_moves_this_turn: int, nb_turns_this_game: int, time_left: float):
        """ GOD AI agent's turn

        TODO At start get player area border area with most dices. Otherwise last used.

        While there is a lucrative attack possible, the agent will do it. Otherwise it will end its turn.
        """

        # TODO jen test, potom můžeš smazat až po první return
        for attack in possible_attacks(board, self.player_name):
            self.logger.info("battle {}({})->{}({}) \theuristic: {}".format(
                attack[0].get_name(),
                attack[0].get_dice(),
                attack[1].get_name(),
                attack[1].get_dice(),
                battle_heuristic(board, attack[0], attack[1])))

        return EndTurnCommand()
        start_area = None
        focus_move = None

        #TODO check for succesfull attack
        if self.first_attack:
            for area in board.get_player_border(self.player_name):
                if start_area is None:
                    start_area = copy.deepcopy(area)
                else:
                    if area.get_dice() > start_area.get_dice():
                        start_area = copy.deepcopy(area)
            self.first_attack = False
        else:
            start_area = self.area_of_interest

        paths = self.search_tree(board, start_area)

        if not paths:
            self.first_attack = True
            return EndTurnCommand()

        #TODO tempfix aby se zabránilo poslání žádnýho příkazu
        return EndTurnCommand()

        #Evaluate all paths, find the best one
        #area_of_interest = targeted area
        #Battle Command with first area of best path


