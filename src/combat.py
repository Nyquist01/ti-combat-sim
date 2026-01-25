"""
Calculate the outcome of this space combat:

2 dreadnoughts vs 1 dreadnought + 1 carrier + 4 fighters

Dreadnought:
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

import random
from copy import deepcopy

from tabulate import tabulate

from .ships import Carrier, Destroyer, Dreadnought, Fighter, Ship, Warsun


def roll_d10() -> int:
    return random.randint(1, 10)


def roll_fleet_hits(fleet: list[Ship]) -> int:
    """Returns the number of hits a fleet produced"""
    hits = 0
    for ship in fleet:
        for _ in range(ship.rolls):
            res = roll_d10()
            if res >= ship.combat:
                hits += 1
    return hits


def assign_fleet_hits(hits: int, target_fleet: list[Ship]):
    """
    Assigns hits to the target fleet.

    Assume hit strategy where we want to keep our 'best' ships alive
    for as long as possible (i.e. dreadnoughts) - this is determined
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


def prompt_int(label: str) -> int:
    min_value = 0
    while True:
        try:
            value = int(input(f"{label}: "))
            if value < min_value:
                print(f"Please enter a greater than {min_value}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid integer.")
        except KeyboardInterrupt:
            print("Input cancelled. Please try again.")


def build_fleet(fleet_num: int | str) -> list[Ship]:
    fleet = []
    print(f"\n--- Building fleet {fleet_num} ---")
    ship_types = {
        "Fighter": Fighter,
        "Carrier": Carrier,
        "Dreadnoughts": Dreadnought,
        "Destroyers": Destroyer,
        "Waruns": Warsun
    }

    for ship_type, cls in ship_types.items():
        n_ships = prompt_int(ship_type)
        fleet += [cls() for _ in range(n_ships)]
    
    return fleet


def get_fleet_cost(fleet: list[Ship]) -> int:
    total = 0
    for ship in fleet:
        total += ship.cost
    return total


def build_table(
    fleet_1_wins: int, fleet_2_wins: int, draws: int, simulations: int, fleet_1_cost: int, fleet_2_cost: int
) -> None:
    headers = ["Fleet", "Wins", "% Winrate", "Cost"]
    data = [
        ["Fleet 1", fleet_1_wins, round((fleet_1_wins / simulations) * 100), fleet_1_cost],
        ["Fleet 2", fleet_2_wins, round((fleet_2_wins / simulations) * 100), fleet_2_cost],
        ["Draws", draws, round((draws / simulations) * 100), "-"],
    ]
    print("\n")
    print(tabulate(data, headers=headers, tablefmt="grid"))


def antifighter_barrage(fleet: list[Ship], enemy_fleet: list[Ship]) -> None:
    barrage_count = 0
    for ship in fleet:
        if ship.has_antifighter_barrage:
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
        return  # no fighters in enemy fleet so return early


def run_simulation():
    """Classic Monte Carlo simulation"""
    simulations = 10000
    fleet_1_wins = 0
    fleet_2_wins = 0
    draws = 0
    rounds = 0
    _fleet_1: list[Ship] = build_fleet(1)
    fleet_1_cost = get_fleet_cost(_fleet_1)
    _fleet_2: list[Ship] = build_fleet(2)
    fleet_2_cost = get_fleet_cost(_fleet_2)

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

    build_table(fleet_1_wins, fleet_2_wins, draws, simulations, fleet_1_cost, fleet_2_cost)
