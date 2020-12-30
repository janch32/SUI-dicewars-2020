from ..utils import possible_attacks
from .utils import add_dice_to_player, battle_heuristic, player_heuristic, simulate_battle
from typing import List, Tuple, Union
from dicewars.client.game.board import Board
from dicewars.client.game.area import Area

class MaxN:
    """MiniMax implemenetace pro hru více hráčů (Max^n)
    """

    def __init__(self, players_order: List[int], depth_limit=-1, spread_limit=5):
        """MiniMax implemenetace pro hru více hráčů (Max^n)

        Args
        ----
            players_order (List[int]): Pořadí hráčů ve hře
            depth_limit (int, optional): Kolik tahů předem se má propočítat.
                Pokud není zadáno, je počet tahů = počet hráčů
            spread_limit (int, optional): Kolik útoků se maximálně může simulovat
                v jednom větvení.
        """

        self.best_move: Union[None, Tuple[Area, Area]] = None
        self.players_order = players_order
        self.players = len(players_order)
        self.spread_limit = spread_limit
        if depth_limit < 0:
            self.depth_limit = self.players
        else:
            self.depth_limit = depth_limit

    def __make_turn(self, board: Board, pl_index: int, depth=0) -> List[float]:
        """Provede jedno větvení MiniMax algoritmu

        Args
        ----
            board (Board): Aktuální stav hrací plochy
            pl_index (int): Pořadí hráče, který je na tahu
            depth (int, optional): Aktuální zanoření, kořen má hodnotu 0

        Returns
        -------
            List[float]: Skóre všech hráčů podle nejlepšího tahu aktuálního hráče
        """

        # vypočítat aktuální skóre všech hráčů
        scores = []
        for player in self.players_order:
            scores.append(player_heuristic(board, player))

        if depth >= self.depth_limit:
            return scores # Jsme na konci procházení, jen vrať aktuální skóre

        player = self.players_order[pl_index]

        attacks: List[Tuple[float, Area, Area]] = []

        # Vybrat vhodné útoky podle heuristiky a seřadit podle nejlepších
        for attacker, target in possible_attacks(board, player):
            bh = battle_heuristic(board, attacker, target)
            if bh > 0 or attacker.get_dice() == 8:
                attacks.append((bh, attacker, target))
        attacks = sorted(attacks, key = lambda x: x[0], reverse=True)

        # Z výkonnostních důvodů omezit počet akcí pro tah
        attacks = attacks[:self.spread_limit]
        attacks = sorted(attacks, key = lambda x: x[0])

        # Provést všechny tahy, rekurzivně pro ně provést protitahy a vybrat
        # tah s nejlepším skóre pro tohoto hráče
        for battle_coef, attacker, target in attacks:
            with simulate_battle(attacker, target):
                with add_dice_to_player(board, player):
                    new_scores = self.__make_turn(board, (pl_index+1) % self.players, depth+1)
                    # Pokud se skóre rovná, tah je dobrý, pokud ostatní hráči mají skóre nižší
                    #if (new_scores[pl_index] == scores[pl_index]) and (sum(new_scores) > sum(scores)):
                    #    continue

                    if new_scores[pl_index] >= scores[pl_index]:
                        scores = new_scores
                        if depth == 0:
                            self.best_move = (attacker, target)

        return scores


    def get_best_move(self, board: Board, player_name: int) -> Union[None, Tuple[Area, Area]]:
        """Metoda vypočítá a vrátí nejlepší možný tah v aktuálním kole

        Args
        ----
            board (Board): Aktuální stav herního pole
            player_name (int): Jméno aktuálního hráče

        Returns
        -------
            Union[None, Tuple[Area, Area]]: Dvojice značící útok odkud->kam nebo nic,
            pokud je výhodnější neprovádět žádný tah
        """

        self.best_move = None
        self.__make_turn(board, self.players_order.index(player_name))
        return self.best_move
