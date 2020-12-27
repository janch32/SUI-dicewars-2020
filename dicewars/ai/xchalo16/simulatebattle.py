from dicewars.client.game.area import Area

class SimulateBattle:
    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        self.target.owner_name = self.orig_target.owner_name
        self.target.dice = self.orig_target.dice
        self.attacker.dice = self.orig_attacker.dice

    def __init__(self, attacker: Area, target: Area, success=True):
        self.attacker = attacker
        self.target = target
        self.orig_attacker = Area(dice=attacker.dice)
        self.orig_target = Area(owner=target.owner_name, dice=target.dice)

        self.attacker.set_dice(1)

        if success:
            self.target.set_dice(attacker.get_dice() - 1)
            self.target.set_owner(attacker.get_owner_name())
