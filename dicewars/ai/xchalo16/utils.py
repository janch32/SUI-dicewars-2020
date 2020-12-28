from dicewars.client.game.board import Board
from dicewars.client.game.area import Area
from ..utils import attack_succcess_probability
from contextlib import contextmanager

@contextmanager
def simulate_battle(attacker: Area, target: Area, success=True):
    """Simuluje bitvu a dočasně modifikuje herní pole podle úspěchu útoku.
    Výsledek po bitvě je dostupný jen uvnitř `with` bloku. Obě pole musí
    být součástí jednoho herního pole. Na rozdíl od deepcopy je tento postup
    výrazně rychlejší.

    Args
    ----
        attacker (Area): Pole ze kterého se útočí
        target (Area): Pole na které se útočí
        success (bool, optional): Má být boj úspěšný. Výchozí True.

    Example
    -------
        board # Zde má board hodnotu před bitvou
        with simulate_battle(attacker, target, success=True):
            board # Zde má board hodnotu po bitvě
            ...
        board # Zde má board opět hodnotu před bitvou
    """
    orig_attack_dice = attacker.dice
    orig_target_dice = target.dice
    orig_target_owner = target.owner_name

    attacker.set_dice(1)

    if success:
        target.set_dice(orig_attack_dice - 1)
        target.set_owner(attacker.get_owner_name())

    try:
        yield
    finally:
        # Vrátit herní pole do původního stavu
        attacker.dice = orig_attack_dice
        target.dice = orig_target_dice
        target.owner_name = orig_target_owner


def player_heuristic(board: Board, player_name: int) -> int:
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

    with simulate_battle(attacker, target, success=True):
        succ_coef = player_heuristic(board, attacker.get_owner_name())

    with simulate_battle(attacker, target, success=False):
        fail_coef = player_heuristic(board, attacker.get_owner_name())

    succ_prob = attack_succcess_probability(attacker.get_dice(), target.get_dice())
    return (succ_prob * succ_coef) - (2 * (1 - succ_prob) * fail_coef)

def path_heuristics(board: Board, path: list) -> float:
    """
        Heuristika = součet všech dílčích heuristik v cestě
    """
    if len(path) < 2:
        return 0

    with simulate_battle(board.get_area(path[0]), board.get_area(path[1])):
        h = path_heuristics(board, path[1:])

    h += battle_heuristic(board, board.get_area(path[0]), board.get_area(path[1]))

    return h

def get_attackable(board: Board, active_area: Area):
        neighbors = active_area.get_adjacent_areas()
        attackable = []
        for nb in neighbors:
            a = board.get_area(nb)
            if active_area.get_owner_name() != a.get_owner_name():
                attackable.append(a)

        return attackable

# ╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╩╜╜╜╜╙╙╜╜║╢╢╢╢╫╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬
# ╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╝╜╙└└││││││╙╜║╢╢╢╢╢╣╢╢╣╢╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬
# ╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╜╙─└└││││││││││╙╜║╢╢╢╫╢╢╢╢╢╫╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬
# ╬╬╬╬╬╬╬╬╬╬╬╬╬╬╣└┌┌┌┌└└└└└│││││││└╜║╢╢║╠╬╢╢╢╣╫╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬
# ╬╬╬╬╬╬╬╬╬╬╬╬╬╬╖┌┌┌┌└└└└└└│││││││└╙│╢╖└╙║╣╢╣╢╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬
# ╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬┐┌  ┌┌┌┌└└└└││││╙╙││║╖║╢║║╙╫╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬
# ╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╫╬╗┌┌     └└└ ┌┌─┘╙││╙║╢╢╢║║╖╫╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬
# ╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬┐┌      ┌└└  │└└└└╙╢╢╢╢╢╣╠╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬
# ╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╗┌   ┌││  ┌ └    └┘╙╙╜╙╜╜╫╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬
# ╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╫╣   └││ ┌     ┌╥┐ ┌╙╖  ╙╫╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬
# ╬╬╫╬╫╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╣    ││ ┌┌ ┌┌╓╖│││││╠╣╖┘╟╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬
# ╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╣┐└ ┌     └└└└╜│││││║╢╣╫╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬
# ╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╣╖│┌┌        ┌└││┌┌╓╓╣╢╫╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╣╨╬╬╬╬╬╬╬╬
# ╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╣─ └     ┌  └└│└╙╙╢╢╣╫╬╬╬╬╬╬╬╬╬╬╬╬╣╜║╜╢╢║╫╬╬╬╬╬╬
# ╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬  ┌   ┌┌┌ ┌┌┌┌┌╖╖╥╫╬╬╬╬╬╬╬╬╬╬╣╢╠╣╢╬╠╬╬╬╬╬╬╬╬╬╬
# ╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╖│          ┌┌└║╢╟╬╬╬╬╬╬╣╢╢╢╫╣╣╢╫╬╣╬╢╫╬╬╬╬╬╬╬
# ╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╜└           └└│└└└╙╜╙╙╨╜╨╢╨╢╢╬╣╢╣╢╣╢╢╢╬╬╬╬╬╬
# ╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╣╝╜╜╙┌                ┌│╓║╜┘││┌│┤─├│└╙╙╢╣╢╢╢╢╫╫╬╬╬╬
# ╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╩╨╙└┌┌             ┌╢┐    ┌╥╜│╙╖┘│╓╬┘╓╬─  └└╙╢╫╬╢╢╫╬╬╬╬
# ╬╬╬╬╬╬╬╬╬╬╬╬╜└└└└└─ └└┐┌ ┌      └┌ ╙└    ╙└└╙┘│╓╬╜┌╓╬┘      │╙╢╬╬╬╬╬╬╬
# ╬╬╬╬╬╬╬╬╬╝└   └┐┌ │┘└┐┐└│└└┘│┐┐─┘──┐│└   ┌│└┘┌╠╝└╓╫╜─    ┌┐ └││╙╬╬╬╬╬╬
# ╬╬╬╬╬╬╫╬└   │┐  └╜╖┌┐└ ╙┘┌╓┐┌┌╓│└╓│┐╙╖   ┘└┌╢╜╙┌╫╣╜      ┌└┌ └││╙╬╬╬╬╬
# ╬╬╬╬╬╫╣       ┘┌┐  └╙╖╓┘╓ ││└╙┘│└╙┤│┘  ┌╓ ╙╙└╓╣╜└        └─   └││╙╬╬╬╬
# ╬╬╬╬╬╣          └╜─╖┌ └╙└╢┴╖╖╖╖╖╓╓╖┬┬ ┌└└ ╓╖╜╜─           ┌    │││╙╬╬╬
# ╬╬╬╬╣               ─│└  ╜┌     ┌┌┌┌╓┌─┐╙┘└  ┌┐┐     └└┌  ┌    ││││╙╬╬
#
#           "Drž se každý své amfóry a nezbude čas na fóry"
#                                     - Amonbofis, Mise Kleopatra
