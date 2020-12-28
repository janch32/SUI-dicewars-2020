from dicewars.client.game.area import Area
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
