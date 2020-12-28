import copy
import logging
from .simulatebattle import SimulateBattle
from dicewars.client.game.board import Board
from dicewars.client.game.area import Area
from ..utils import attack_succcess_probability

def heuristic_coefficient(board: Board, player_name: int) -> int:
    """
    koeficient = (počet_polí_hlavního_území - napadnutelná_pole - nepřímo_napadnutelná_pole)
    """
    score = 0
    attackable_areas = 0
    p_attackable_areas = 0 # TODO

    regions = board.get_players_regions(player_name)
    for region in regions:
        score = max(score, len(region))

        for area_id in region:
            area: Area = board.get_area(area_id)
            area_dice = area.get_dice()
            neigh = area.get_adjacent_areas()

            for nid in neigh:
                n: Area = board.get_area(nid)
                if n.get_owner_name() != player_name and n.get_dice() > area_dice:
                    attackable_areas += 1
                    break # TODO koeficient když o to můžeme přijít jako fakt hodně


    return score - attackable_areas - p_attackable_areas


def battle_heuristic(board: Board, attacker: Area, target: Area) -> float:
    """
    heuristika = pst_úspěchu * koeficient(úspěch) - pst_prohry * koeficient(prohra)
    """

    with SimulateBattle(attacker, target, success=True):
        succ_coef = heuristic_coefficient(board, attacker.get_owner_name())

    with SimulateBattle(attacker, target, success=False):
        fail_coef = heuristic_coefficient(board, attacker.get_owner_name())

    succ_prob = attack_succcess_probability(attacker.get_dice(), target.get_dice())
    return (succ_coef * succ_prob) - (fail_coef * (1 - succ_prob))


# Místo toho použij SimulateBattle z modulu .simulatebattle
#def simulate_attack(board: Board, attacker: Area, target: Area) -> Board:
#    """Simuluje útok se 100% úspěšností a vrátí nový stav hracího pole
#
#    Args:
#        board (Board): Aktuální stav hracího pole
#        attacker (Area): Název políčka ze kterého se útočí
#        target (Area): Název políčka na které se útočí
#
#    Returns:
#        Board: Nový stav hracího pole (jako deepcopy)
#    """
#    new_board = copy.deepcopy(board)
#
#    new_attacker: Area = new_board.get_area(attacker.name)
#    new_target: Area = new_board.get_area(target.name)
#
#    new_target.set_owner(new_attacker.get_owner_name())
#    new_target.set_dice(new_attacker.get_dice() - 1)
#    new_attacker.set_dice(1)

    return new_board

def get_attackable(board: Board, active_area: Area):
        neighbors = active_area.get_adjacent_areas()
        attackable = []
        for nb in neighbors:
            a = board.get_area(nb)
            if active_area.get_owner_name() != a.get_owner_name():
                attackable.append(a)

        return attackable


# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⢛⢋⢩⢩⢸⣪⣪⣮⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⢋⢉⢈⢀⢨⢨⢨⢨⢪⢪⣪⣪⣸⣫⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⠉⢀⢀⢀⢈⢀⢈⢨⢈⢨⢨⢨⢪⢨⢪⣪⣪⣫⣽⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠉⢀⢀⢀⢀⢀⢀⢀⢈⢈⢀⢈⢨⢨⢨⢨⢨⢨⣪⣪⣪⣹⣿⣿⣿⢫⣫⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣤⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢈⢨⢨⢨⢨⢨⢨⢸⣪⣸⣯⣿⣯⢈⣹⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢈⢨⢨⢨⢨⢪⣪⢻⢻⢻⢻⣻⣸⣻⢻⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢨⠈⢈⣨⣨⣶⣾⣿⢿⣻⢻⣿⣿⣿⣿⣿⣿⣌⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣀⢀⢀⢀⢀⢀⢀⢀⠈⠈⣠⣰⣪⠪⢈⢀⢠⢠⢪⢪⣪⣹⣯⣿⣿⣿⣿⣿⣮⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⢀⢀⢀⢀⠈⢠⢢⣪⢨⠈⢀⢨⢀⢀⢠⢠⢠⢈⢈⢸⣿⢻⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣀⠀⢠⠪⢪⢨⢀⢨⢀⢀⢀⢀⠈⢈⢠⢠⣀⠈⠈⠋⠛⢠⣿⡹⠛⢻⢋⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢀⢀⠀⠈⢨⢈⣪⢀⢀⢀⠀⠀⠈⢠⢠⣴⣾⣶⣠⢠⢨⣹⣤⣴⣤⢉⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⢀⢀⢀⠀⢸⣨⡪⢠⢀⢀⢠⣢⣢⣪⣼⣾⣩⣪⢨⢨⢪⢪⣿⣿⣾⣮⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢀⢈⠀⣰⢀⢀⢀⢀⢀⢀⢀⢈⢈⢪⢹⣻⢈⢈⢈⢠⣨⢪⣾⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⢠⢠⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢈⢨⢨⣠⣠⣈⢨⣫⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⢪⢠⣠⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢠⢨⢨⢪⣾⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⢨⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠈⢈⢈⠋⠘⠋⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣾⣿⣿⣾⣮⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣀⢠⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢈⢈⢫⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣫⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⢠⠀⠀⠀⢀⠀⢀⢀⢀⠀⢀⢀⢠⣠⣀⣰⣿⢫⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢈⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠈⢨⢪⢠⢀⢈⢨⣫⣩⣫⢹⣻⢉⢹⣻⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⠻⠛⠉⢁⢀⠀⠀⠀⢀⢀⠀⢀⠀⠀⠀⢀⠀⠀⠀⠀⣨⠀⢨⢨⢨⣪⣾⢛⣺⣮⣪⣪⢀⣪⣾⣪⢨⣾⣋⢨⢉⢛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⠋⢀⢀⢀⢀⢀⢠⢨⢀⢀⢀⢀⠀⠀⠀⢀⢀⢀⢀⣰⣾⣀⢀⠀⠀⢈⢨⣨⣼⣿⢉⣻⣮⣮⣪⢠⣼⣿⡫⢠⣾⣿⢀⢀⢀⢈⢈⢪⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⢈⢀⢰⢪⣤⣠⢈⢪⢢⣠⢀⢀⢀⢀⢀⢀⢀⢀⠀⠀⢀⣠⢀⠈⢻⠃⠘⠀⢈⠈⢘⣿⢋⢈⣪⣮⣸⢈⣰⣾⣿⢁⣠⣾⣿⢁⢀⢀⢀⢀⠀⠀⢪⢫⢿⣯⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢋⠀⠈⢪⢠⣠⢠⠊⢈⣶⣪⢈⢊⣈⢙⢺⣶⣮⣨⣠⣢⣢⣠⣰⣠⢈⢀⢀⣠⣠⣨⠀⢀⢀⢠⣸⣺⣠⣨⢈⣠⣾⣿⠋⢠⣾⣿⡟⢀⢀⢀⢀⢀⢠⣠⠀⢸⢈⢪⢹⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠉⠀⢸⣸⣤⢀⠈⠘⢺⣬⣪⣨⢈⢸⢪⢨⣠⣴⢂⢪⢨⣨⣈⣨⣨⣨⣨⣨⣨⢀⠊⣨⣆⣄⢀⢠⣠⢨⢸⢪⢨⣾⣿⠟⢀⣸⣾⣿⢁⢀⢀⢀⢀⢀⢀⢀⢈⣠⢀⢈⢈⢨⢪⣻⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠈⢺⣘⣤⣀⢀⠉⢻⢺⣬⣪⣬⣀⢸⢀⠈⢺⣏⢈⣢⣴⣿⣢⣢⢰⣿⣨⢪⢈⠻⢀⣸⢀⢈⢨⣠⣾⣻⠫⢈⣴⣾⣿⠋⢀⢀⢀⢀⢀⢀⢀⢀⢨⢀⢈⢀⢀⢀⢨⢨⢪⣻⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠙⣮⣺⣄⢠⢀⠈⠋⢻⣮⣮⣲⣦⣬⣪⣈⢀⢈⣫⣨⢈⢀⢈⢣⣨⣈⠀⢀⣨⣼⣦⠈⢫⢈⣠⣶⣿⢿⢉⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠀⢠⢀⢀⢨⢈⢨⢪⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠺⣹⢲⣦⣤⣠⣠⢈⢈⢻⣿⢻⢾⣾⣾⣾⣮⣮⣮⣮⣾⣾⢻⣠⢸⢈⠀⢈⣠⣴⣦⠾⠋⠀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢈⢀⠀⢀⠀⢈⢨⢠⢈⢨⢻⣿⣿⣿
# ⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠪⣬⣙⢀⢀⢸⢫⣢⣠⣠⣠⣨⣈⣈⢨⢨⢀⣀⣠⣤⣴⣺⣫⠯⠛⢉⠀⢪⢸⣪⣢⣴⣄⠈⠘⢪⢀⢀⢀⢀⢀⢀⢈⢀⢀⢠⢨⠀⢨⢪⢨⢠⢈⢨⢻⣿⣿
# ⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢨⢀⢀⣠⠚⠪⠪⢨⢩⣩⣩⣩⣩⣩⣩⠼⠺⢚⢉⢈⠀⠀⢀⠀⠀⢈⢀⢢⣢⣪⣪⣪⣼⢰⠀⣤⠘⢪⢀⢀⢀⢈⠀⢀⢈⢀⠀⢪⣪⢠⢀⢈⢨⣻⣿⣿
# ⣿⣿⣿⣿⣟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⢨⣨⣼⣾⠁⠀⠀⠀⠀⢀⢀⢀⣀⣠⣴⣾⣾⣿⣿⣻⣿⠃⢀⢀⢀⢀⢢⣢⢪⢪⢪⢪⢪⢪⣪⣪⣪⢪⣦⡈⢪⢀⠀⠀⢈⢀⠀⠀⢨⢪⢀⢀⢀⢈⢪⣿
# ⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⢠⢪⢪⢪⢪⣿⣾⣶⣶⣾⣽⣮⣪⢪⢪⢨⠋⠋⠈⠀⠀⠀⢀⠀⢀⠀⠀⢀⢨⣨⢊⢊⣊⣊⣪⣊⣸⣪⣊⢪⢪⣤⠘⠀⠀⢨⢀⠀⠀⢈⢨⣠⢀⢀⢀⢨⣪
# ⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⢠⢀⢀⢈⢨⢪⢪⢨⣸⣪⣸⣾⣮⣦⣠⣠⣤⣴⣶⣾⣾⣾⣿⣿⣿⣿⣦⠀⢠⢘⣻⢨⣨⣨⣨⣨⣨⣨⣨⣸⣪⢪⢪⣀⢠⠀⢀⢀⠂⢠⣠⣴⢈⠀⠀⢈⢨⢪
# ⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⢠⢀⢠⣢⣢⢪⢨⢪⢨⢨⢈⣪⢻⣻⣫⢪⢪⠪⠻⠯⠫⠛⠋⠉⢈⠈⠈⠀⠀⢨⢨⣿⣨⣨⣨⣨⣨⣨⣨⣸⣪⣨⣊⢪⢈⠀⠀⠀⠀⠀⠀⠘⢻⢪⣄⠀⠀⢨⢪
#
# Drž se každý své amfóry a nezbude čas na fóry
