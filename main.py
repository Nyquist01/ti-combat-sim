"""
Calculate the outcome of this space combat:

2 dreadnaughts vs 1 dreadnaught + 1 carrier + 4 fighters vs 2 dreadnaughts

Dreadnaught:
2 HP
5 Combat roll (60% chance of producing a hit)

Fighter:
1 HP
9 Combat roll (80% chance of producing a hit)

Carrier:
1 HP
9 Combat roll (80% chance of producing a hit)

Pseudo:

1. First player rolls for each of their ships - count the number of hits produced
2. Second player rolls for each of their ships - count the number of hits produced
3. First player assigns hits
4. Second player assigns hits
"""


import random


class Ship:
    def __init__(self):
        self.hp = 0
    
    def take_damage(self):
        self.hp -= 1


class Dreadnaught(Ship):
    def __init__(self):
        self.hp = 2
        self.combat = 5
        self.name = "dreadnaught"


class Fighter(Ship):
    def __init__(self):
        self.hp = 1
        self.combat = 9
        self.name = "fighter"


class Carrier(Ship):
    def __init__(self):
        self.hp = 1
        self.combat = 9
        self.name = "carrier"


def roll_d10() -> int:
    return random.randint(1, 10)


def main():
    fleet_1: list[Ship] = [Dreadnaught(), Dreadnaught()]
    fleet_2: list[Ship] = [Dreadnaught(), Fighter(), Fighter(), Fighter(), Fighter(), Carrier()]
    fleet_1_wins = 0
    fleet_2_wins = 0

    for _ in range(10000):
        active_combat = True
        while active_combat:
            fleet_1_hits = 0
            for ship in fleet_1:
                res = roll_d10()
                if res >= ship.combat:
                    fleet_1_hits += 1
            

            fleet_2_hits = 0
            for ship in fleet_2:
                res = roll_d10()
                if res >= ship.combat:
                    fleet_2_hits += 1
                    
            for _ in range(fleet_1_hits):
                if len(fleet_2) == 1:
                    break
                i = random.choice(range(len(fleet_2)))
                ship_to_hit = fleet_2[i]
                ship_to_hit.take_damage()
                if ship_to_hit.hp <= 0:
                    fleet_2.pop(i)
            
            for _ in range(fleet_2_hits):
                if len(fleet_1) == 0:
                    break
                i = random.choice(range(len(fleet_1)))
                ship_to_hit = fleet_1[i]
                ship_to_hit.take_damage()
                if ship_to_hit.hp <= 0:
                    fleet_1.pop(i)
            
            if len(fleet_1) == 0 and len(fleet_2) == 0:
                print("Both fleets destroyed in the same round! DRAW")
                active_combat = False
            elif len(fleet_1) == 0:
                # print(f"fleet_1={fleet_1}, fleet_2={fleet_2}")
                print("Fleet 2 wins!")
                fleet_2_wins += 1
                active_combat = False
            elif len(fleet_2) == 0:
                print("Fleet 1 wins!")
                fleet_1_wins += 1
                active_combat = False
    
    print(f"Fleet 1 won {fleet_1_wins} times")
    print(f"Fleet 2 won {fleet_2_wins} times")

if __name__ == "__main__":
    main()
