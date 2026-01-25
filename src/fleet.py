from .ships import Ship
from .rng import roll_d10


class Fleet:
    def __init__(self, name: str, ships: list[Ship]):
        self.name = name
        self.ships = ships
    
    @property
    def cost(self):
        total = 0
        for ship in self.ships:
            total += ship.cost
        return total
    
    @property
    def hp(self):
        total = 0
        for ship in self.ships:
            total += ship.hp
        return total
    
    @property
    def is_dead(self):
        """Returns True if the fleet has no ships"""
        return not bool(self.ships)
    
    def roll_hits(self):
        """Returns the number of hits the fleet produced"""
        hits = 0
        for ship in self.ships:
            for _ in range(ship.rolls):
                res = roll_d10()
                if res >= ship.combat:
                    hits += 1
        return hits
