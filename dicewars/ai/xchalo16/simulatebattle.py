from dicewars.client.game.area import Area

class SimulateBattle:
    """Simuluje bitvu a dočasně modifikuje herní pole podle úspěchu útoku.
    """

    def __exit__(self, type, value, traceback):
        self.attacker.dice = self.orig_atk_dice
        self.target.dice = self.orig_tgt_dice
        self.target.owner_name = self.orig_tgt_owner

    def __init__(self, attacker: Area, target: Area, success=True):
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
            with SimulateBattle(attacker, target, success=True):
                board # Zde má board hodnotu po bitvě
                ...
            board # Zde má board opět hodnotu před bitvou
        """
        self.attacker = attacker
        self.target = target
        self.orig_atk_dice = attacker.dice
        self.orig_tgt_dice = target.dice
        self.orig_tgt_owner = target.owner_name

        self.attacker.set_dice(1)

        if success:
            self.target.set_dice(self.orig_atk_dice - 1)
            self.target.set_owner(attacker.get_owner_name())
