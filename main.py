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

from copy import deepcopy
from abc import ABC
import random
from tabulate import tabulate


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
    def __init__(self):
        self.hp = 2
        self.combat = 5
        self.priority = 1
        self.name = "dreadnaught"


class Fighter(Ship):
    def __init__(self):
        self.hp = 1
        self.combat = 9
        self.priority = 3
        self.name = "fighter"


class Carrier(Ship):
    def __init__(self):
        self.hp = 1
        self.combat = 9
        self.priority = 4
        self.name = "carrier"


class Destroyer(Ship):
    def __init__(self):
        self.hp = 1
        self.combat = 1
        self.priority = 2
        self.name = "destroyer"


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
        target_fleet.sort(key=lambda ship: (-ship.hp, -ship.priority))
        ship_to_hit = target_fleet[0]
        ship_to_hit.take_damage()
        if ship_to_hit.hp <= 0:
            target_fleet.remove(ship_to_hit)


def build_fleets(fleet_num: int | str) -> list[Ship]:
    print(f"\n--- Building fleet {fleet_num} ---")
    n_fighters = int(input("Fighters: "))
    n_carriers = int(input("Carriers: "))
    n_dreadnaughts = int(input("Dreadnaughts: "))
    n_destroyers = int(input("Destroyers: "))
    return [Fighter() for _ in range(n_fighters)] + [Carrier() for _ in range(n_carriers)] + [Dreadnaught() for _ in range(n_dreadnaughts)] + [Destroyer() for _ in range(n_destroyers)]


def build_table(fleet_1_wins: int, fleet_2_wins: int, draws: int, simulations: int) -> None:
    headers = ["Fleet", "Wins", "% Winrate"]
    data = [
        ["Fleet 1", fleet_1_wins, round((fleet_1_wins/simulations) * 100)],
        ["Fleet 2", fleet_2_wins, round((fleet_2_wins/simulations) * 100)],
        ["Draws", draws, round((draws/simulations) * 100)]
    ]
    print("\n")
    print(tabulate(data, headers=headers, tablefmt="grid"))


def antifighter_barrage(fleet: list[Ship], enemy_fleet: list[Ship]) -> int:
    barrage_count = 0
    for ship in fleet:
        if isinstance(ship, Destroyer):
            barrage_count += 1
    
    hits = 0
    for _ in range(barrage_count):
        res = roll_d10()
        if res >= 9:
            hits += 1
    
    for _ in range(hits):
        for ship in enemy_fleet:
            if isinstance(ship, Fighter):
                enemy_fleet.remove(ship)
                break


def main():
    """Classic Monte Carlo simulation"""
    simulations = 10000
    fleet_1_wins = 0
    fleet_2_wins = 0
    draws = 0
    rounds = 0
    _fleet_1: list[Ship] = build_fleets(1)
    _fleet_2: list[Ship] = build_fleets(2)

    for _ in range(simulations):
        fleet_1 = deepcopy(_fleet_1)
        fleet_2 = deepcopy(_fleet_2)
        active_combat = True
        round_num = 1
        antifighter_barrage(fleet_1, fleet_2)
        antifighter_barrage(fleet_2, fleet_1)
        while active_combat:
            fleet_1_hits = roll_fleet_hits(fleet_1)
            fleet_2_hits = roll_fleet_hits(fleet_2)
            assign_fleet_hits(fleet_1_hits, fleet_2)
            assign_fleet_hits(fleet_2_hits, fleet_1)
            
            if len(fleet_1) == 0 and len(fleet_2) == 0:
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
    
    build_table(fleet_1_wins, fleet_2_wins, draws, simulations)


if __name__ == "__main__":
    main()
