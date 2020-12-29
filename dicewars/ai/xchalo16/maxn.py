import random
from ..utils import possible_attacks, attack_succcess_probability, probability_of_holding_area
from .utils import simulate_battle
from typing import Dict, List, Tuple, Union
from dicewars.client.game.board import Board
from dicewars.client.game.area import Area
from contextlib import contextmanager

def player_heuristic(board: Board, player_name: int) -> int:
    """
    koeficient = počet_polí_hlavního_území
    """
    score = 0
    regions = board.get_players_regions(player_name)
    for region in regions:
        score = max(score, len(region))
    return score

def battle_heuristic(board: Board, attacker: Area, target: Area) -> float:
    """
    heuristika = pst_úspěchu * koeficient(úspěch) - pst_prohry * koeficient(prohra)
    """

    with simulate_battle(attacker, target, success=True):
        succ_coef = player_heuristic(board, attacker.get_owner_name())

    with simulate_battle(attacker, target, success=False):
        fail_coef = player_heuristic(board, attacker.get_owner_name())

    succ_prob = attack_succcess_probability(attacker.get_dice(), target.get_dice())
    hold_prob = probability_of_holding_area(board, target.get_name(), attacker.get_dice()-1, attacker.get_owner_name())
    fail_hold_prob = probability_of_holding_area(board, attacker.get_name(), 1, attacker.get_owner_name())
    #return (hold_prob * succ_prob * succ_coef) - (2*(1 - fail_hold_prob) * (1 - succ_prob) * fail_coef)
    return (hold_prob * succ_prob * succ_coef) - ((1 - succ_prob) * fail_coef)


@contextmanager
def add_dices_to_player(board: Board, player_name: int):
    affected_areas: Dict[int, int] = {}
    dice = 0
    regions = board.get_players_regions(player_name)
    for region in regions:
        dice = max(dice, len(region))

    areas: List[Area] = []
    for area in board.get_player_areas(player_name):
        dice += area.dice
        areas.append(area)

    if dice > 64:
        dice = 64

    while dice and areas:
        area = random.choice(areas)
        if area.dice >= 8:
            areas.remove(area)
        else:
            if area.name not in affected_areas:
                affected_areas[area.name] = area.dice
            area.dice += 1
            dice -= 1

    try:
        yield
    finally:
        # Vrátit herní pole do původního stavu
        for name in affected_areas:
            board.get_area(name).dice = affected_areas[name]

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
