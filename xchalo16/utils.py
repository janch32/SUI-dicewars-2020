import random
from typing import Dict, List
from contextlib import contextmanager
from dicewars.client.game.board import Board
from dicewars.client.game.area import Area
from dicewars.ai.utils import attack_succcess_probability, probability_of_holding_area

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

@contextmanager
def add_dice_to_player(board: Board, player_name: int):
    """Vytvoří dočasné herní pole s náhodně přidělenými kostkami pro vybraného
    hráče. Základní logika předělování kostek je převzatá z implemenetace hry
    viz dicewars/server/game.py line:230.

    Funkce se používá stejně jako funkce simulate_battle.

    Args
    ----
        board (Board): Aktuální stav herního pole
        player_name (int): Jméno hráče, kterému se mají přiřadit kostky
    """

    affected_areas: Dict[int, int] = {}
    dice = 0
    regions = board.get_players_regions(player_name)
    for region in regions:
        dice = max(dice, len(region))

    areas: List[Area] = []
    for area in board.get_player_areas(player_name):
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


# Heuristiky pro MaxN algoritmus

def player_heuristic(board: Board, player_name: int) -> int:
    """Výpočet heuristiky pro hráče podle aktuálního stavu herní plochy.
    koeficient = počet_polí_hlavního_území

    Args
    ----
        board (Board): Aktuální stav herní plochy
        player_name (int): Jméno hráče

    Returns
    -------
        int: Výsledná hodnota heuristiky. Větší znamená lepší
    """

    score = 0
    regions = board.get_players_regions(player_name)
    for region in regions:
        score = max(score, len(region))
    return score

def battle_heuristic(board: Board, attacker: Area, target: Area) -> float:
    """Výpočet heuristiky potenciální bitvy
    heuristika = pst_úspěchu * koeficient(úspěch) - pst_prohry * koeficient(prohra)

    Args
    ----
        board (Board): Aktuální stav herní plochy
        attacker (Area): Úzení ze kterého se útočí
        target (Area): Území na které se útočí

    Returns
    -------
        float: Výsledná hodnota heuristiky. Větší znamená lepší.
    """

    with simulate_battle(attacker, target, success=True):
        succ_coef = player_heuristic(board, attacker.get_owner_name())

    with simulate_battle(attacker, target, success=False):
        fail_coef = player_heuristic(board, attacker.get_owner_name())

    succ_prob = attack_succcess_probability(attacker.get_dice(), target.get_dice())
    hold_prob = probability_of_holding_area(board, target.get_name(), attacker.get_dice()-1, attacker.get_owner_name())
    # Pokus o přidání koeficientu pravděpodobnosti ztráty útočného pole v případě neúspěchu.
    # Toto nemělo žádný pozitivní výsledek na % výher.
    #fail_hold_prob = probability_of_holding_area(board, attacker.get_name(), 1, attacker.get_owner_name())
    #return (hold_prob * succ_prob * succ_coef) - (2*(1 - fail_hold_prob) * (1 - succ_prob) * fail_coef)
    return (hold_prob * succ_prob * succ_coef) - ((1 - succ_prob) * fail_coef)


# ############################################################################ #
#    Funkce níže se nepoužívají. Jde o pozůstatek z testování různých          #
#    přístupů při tvorbě AI.                                                   #
# ############################################################################ #

@contextmanager
def add_dice_to_player_worst_case(board: Board, player_name: int, is_yourself: bool, logger):
    affected_areas: Dict[int, int] = {}
    dice = 0
    regions = board.get_players_regions(player_name)
    for region in regions:
        dice = max(dice, len(region))

    if is_yourself:
        areas = board.get_player_areas(player_name)
        b_a = board.get_player_border(player_name)
        areas = list(set(areas)-set(b_a))
        if areas is None:
            areas = b_a
    else:
        areas =  board.get_player_border(player_name)

    arr = [a.get_name() for a in areas]
    logger.info("PLayer: {} with areas: {}".format(player_name, arr))

    if dice > 64:
        dice = 64

    while dice and areas:
        if is_yourself:
            area = random.choice(areas)
            while area.dice < 8:
                area.dice += 1
                dice -= 1
        else:
            area = areas.pop(0)
            areas.append(area)

        if area.dice >= 8:
            areas.remove(area)
        elif not is_yourself:
            if area.name not in affected_areas:
                affected_areas[area.name] = area.dice
            area.dice += 1
            dice -= 1

    if dice > 0:
        if is_yourself:
            areas = board.get_player_border(player_name)
        else:
            areas = board.get_player_areas(player_name)
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
