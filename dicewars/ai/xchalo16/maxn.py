from ..utils import possible_attacks
from .utils import player_heuristic, simulate_battle
from typing import List, Tuple
from dicewars.client.game.board import Board
from dicewars.client.game.area import Area

class MaxN:
    """MiniMax implemenetace pro hru více hráčů
    """
    def __init__(self, players_order: List[int], depth_limit=4):
        self.players_order = players_order
        self.players = len(players_order)
        self.depth_limit = depth_limit

    def make_turn(self, board: Board, player_index: int, depth=0) -> List[float]:
        scores = []
        for player in self.players_order:
            scores.append(player_heuristic(board, player))

        if depth >= self.depth_limit:
            # Jsme na konci procházení, jen vrať aktuální skóre
            return scores


        player = self.players_order[player_index]
        for attacker, target in possible_attacks(board, player):
            with simulate_battle(attacker, target):
                new_scores = self.make_turn(board, player_index+1 % self.players, depth+1)
                if new_scores[player_index] >= scores[player_index]:
                    scores = new_scores

        return scores


    def best_move(self, board: Board, active_player: int) -> Tuple[Area, Area]:



        pass
