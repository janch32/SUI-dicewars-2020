import logging
from typing import List
from dicewars.client.ai_driver import BattleCommand, EndTurnCommand
from dicewars.client.game.board import Board

from .maxn import MaxN

class AI:
    """Umělá inteligence pro válku kostek týmu xchalo16 založená na
    implementaci algoritmu ExpectiMiniMax s rozšířením pro hru více hráčů.

    Tato umělá inteligence je optimalizovaná pro hru čtyřech hráčů, ale dokáže
    hrát i v jiném počtu hráčů.
    """

    def __init__(self, player_name: int, board: Board, players_order: List[int]):

        self.player_name = player_name
        self.players_order = players_order
        self.logger = logging.getLogger('AI')
        self.max_n = MaxN(players_order, 8)

    def ai_turn(self, board: Board, nb_moves_this_turn: int, nb_turns_this_game: int, time_left: float):
        """Provede jeden tah podle vyhodnocení algoritmem MaxN. Pokud algoritmus
        nenalezne výhodnější stav po bitvě než je ten současný, ukončuje kolo.
        """

        # Ochrana proti vypršení času. V případě velkého poklesu zbývajícího času
        # se provede omezení hloubky prohledávání.
        if time_left > 8:
            self.max_n.depth_limit = 8
        elif time_left > 5:
            self.max_n.depth_limit = 4
            self.logger.info("Limiting depth to 4, time left: {}".format(time_left))
        else:
            self.max_n.depth_limit = 1
            self.logger.info("Limiting depth to 1, time left: {}".format(time_left))

        move = self.max_n.get_best_move(board, self.player_name)
        if move == None:
            return EndTurnCommand()
        return BattleCommand(move[0].get_name(), move[1].get_name())
