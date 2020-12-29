from ..utils import possible_attacks
from .utils import add_dices_to_player, battle_heuristic, player_heuristic, simulate_battle
from typing import List, Tuple, Union
from dicewars.client.game.board import Board
from dicewars.client.game.area import Area
class MaxN:
    """MiniMax implemenetace pro hru více hráčů (Max^n)
    """
    def __init__(self, players_order: List[int], depth_limit=-1):
        self.best_move: Union[None, Tuple[Area, Area]] = None
        self.players_order = players_order
        self.players = len(players_order)
        self.depth_limit = self.players if depth_limit < 0 else depth_limit

    def __make_turn(self, board: Board, pl_index: int, depth=0) -> List[float]:
        scores = []
        for player in self.players_order:
            scores.append(player_heuristic(board, player))

        if depth >= self.depth_limit:
            # Jsme na konci procházení, jen vrať aktuální skóre
            return scores

        player = self.players_order[pl_index]

        attacks: List[Tuple[float, Area, Area]] = []

        for attacker, target in possible_attacks(board, player):
            bh = battle_heuristic(board, attacker, target)
            if bh > 0 or attacker.get_dice() == 8:
                attacks.append((bh, attacker, target))

        attacks = sorted(attacks, key = lambda x: x[0], reverse=True)

        if depth >= 0:
            # z výkonnostních důvodů omezit větvení na "fakt dobrý" tahy
            attacks = attacks[:5]

        # provést všechny tahy, rekurzivně pro ně provést protitahy a vybrat
        # tah s nejlepším skóre pro tohoto hráče
        for _, attacker, target in attacks:
            with simulate_battle(attacker, target):
                with add_dices_to_player(board, player):
                    new_scores = self.__make_turn(board, (pl_index+1) % self.players, depth+1)
                    if (new_scores[pl_index] == scores[pl_index]) and (sum(new_scores) > sum(scores)):
                        continue

                    if new_scores[pl_index] >= scores[pl_index]:
                        scores = new_scores
                        if depth == 0:
                            self.best_move = (attacker, target)

        return scores


    def get_best_move(self, board: Board, player_name: int) -> Union[None, Tuple[Area, Area]]:
        self.best_move = None
        self.__make_turn(board, self.players_order.index(player_name))
        return self.best_move
