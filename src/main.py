"""
Calculate the outcome of this space combat:

2 dreadnaughts vs 1 dreadnaught + 1 carrier + 4 fighters

Dreadnaught:
2 HP
5 Combat roll (60% chance of producing a hit)

Fighter:
1 HP
9 Combat roll (20% chance of producing a hit)

Carrier:
1 HP
9 Combat roll (20% chance of producing a hit)


1. First player rolls for each of their ships - count the number of hits produced
2. Second player rolls for each of their ships - count the number of hits produced
3. First player assigns hits
4. Second player assigns hits
"""

from abc import ABC
import random


class Ship(ABC):
    hp: int
    combat: int
    priority: int
    name: str
    
    def take_damage(self):
        self.hp -= 1
        
    def __repr__(self):
        return f"<name={self.name} hp={self.hp}>"


class Dreadnaught(Ship):
    def __init__(self, hp: int = 2):
        self.hp = hp
        self.combat = 5
        self.priority = 1
        self.name = "dreadnaught"


class Fighter(Ship):
    def __init__(self):
        self.hp = 1
        self.combat = 9
        self.priority = 2
        self.name = "fighter"


class Carrier(Ship):
    def __init__(self):
        self.hp = 1
        self.combat = 9
        self.priority = 3
        self.name = "carrier"


def roll_d10() -> int:
    return random.randint(1, 10)


def roll_fleet_hits(fleet: list[Ship]) -> int:
    """Returns the number of hits a fleet produced"""
    hits = 0
    for ship in fleet:
        res = roll_d10()
        if res >= ship.combat:
            hits += 1
    return hits


def sort_fleet(fleet: list[Ship]):
    fleet.sort(key=lambda ship: (-ship.priority, -ship.hp))


def assign_fleet_hits(hits: int, target_fleet: list[Ship]):
    """
    Assigns hits to the target fleet.
    
    Assume hit strategy where we want to keep our 'best' ships alive
    for as long as possible (i.e. dreadnaughts) - this is determined
    using a ship's priority.
    """
    for _ in range(hits):
        if len(target_fleet) == 0:
            break
        sort_fleet(target_fleet)
        ship_to_hit = target_fleet[0]
        ship_to_hit.take_damage()
        if ship_to_hit.hp <= 0:
            target_fleet.pop(0)


def main():
    """Classic Monte Carlo simulation"""
    simulations = 10000
    fleet_1_wins = 0
    fleet_2_wins = 0
    draws = 0
    rounds = 0

    for _ in range(simulations):
        fleet_1: list[Ship] = [Dreadnaught(), Dreadnaught()]
        fleet_2: list[Ship] = [Dreadnaught(), Fighter(), Fighter(), Fighter(), Fighter(), Carrier()]
        active_combat = True
        round_num = 1
        while active_combat:
            fleet_1_hits = roll_fleet_hits(fleet_1)
            fleet_2_hits = roll_fleet_hits(fleet_2)
            assign_fleet_hits(fleet_1_hits, fleet_2)
            assign_fleet_hits(fleet_2_hits, fleet_1)
            
            if len(fleet_1) == 0 and len(fleet_2) == 0:
                print("Both fleets destroyed in the same round! DRAW")
                draws += 1
                active_combat = False
            elif len(fleet_1) == 0:
                fleet_2_wins += 1
                active_combat = False
            elif len(fleet_2) == 0:
                fleet_1_wins += 1
                active_combat = False
            round_num += 1
        rounds += round_num
    
    print(f"Fleet 1 won {fleet_1_wins} times ({round((fleet_1_wins/simulations) * 100)}%)")
    print(f"Fleet 2 won {fleet_2_wins} times ({round((fleet_2_wins/simulations) * 100)}%)")
    print(f"Draws={draws} ({round((draws/simulations) * 100)})% with avg number of rounds={round(rounds/simulations)}")


if __name__ == "__main__":
    main()
