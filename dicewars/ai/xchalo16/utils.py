import copy
from dicewars.client.game.board import Board
from dicewars.client.game.area import Area

def simulate_attack(board: Board, attacker: Area, target: Area) -> Board:
    """Simuluje útok se 100% úspěšností a vrátí nový stav hracího pole

    Args:
        board (Board): Aktuální stav hracího pole
        attacker (Area): Název políčka ze kterého se útočí
        target (Area): Název políčka na které se útočí

    Returns:
        Board: Nový stav hracího pole (jako deepcopy)
    """
    new_board = copy.deepcopy(board)

    new_attacker: Area = new_board.get_area(attacker.name)
    new_target: Area = new_board.get_area(target.name)

    new_target.set_owner(new_attacker.get_owner_name())
    new_target.set_dice(new_attacker.get_dice() - 1)
    new_attacker.set_dice(1)

    return new_board

def get_attackable(active_area : Area, neighbours):
        attackable = []
        for nb in neighbours:
            if active_area.get_owner_name() != nb.get_owner_name():
                attackable.append(nb)

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
