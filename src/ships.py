from abc import ABC


class Ship(ABC):
    hp: int
    combat: int
    priority: int
    name: str
    rolls: int  # number of die this ship rolls in one combat turn
    has_antifighter_barrage: bool = False

    def take_damage(self):
        self.hp -= 1

    def __repr__(self):
        return f"<name={self.name} hp={self.hp}>"


class Dreadnought(Ship):
    def __init__(self):
        self.hp = 2
        self.combat = 5
        self.rolls = 1
        self.priority = 1
        self.name = "dreadnought"


class Fighter(Ship):
    def __init__(self):
        self.hp = 1
        self.combat = 9
        self.rolls = 1
        self.priority = 3
        self.name = "fighter"


class Carrier(Ship):
    def __init__(self):
        self.hp = 1
        self.combat = 9
        self.rolls = 1
        self.priority = 4
        self.name = "carrier"


class Destroyer(Ship):
    def __init__(self):
        self.hp = 1
        self.combat = 1
        self.rolls = 1
        self.priority = 2
        self.name = "destroyer"
        self.has_antifighter_barrage = True


class Warsun(Ship):
    def __init__(self):
        self.hp = 2
        self.combat = 3
        self.rolls = 3
        self.priority = 1
        self.name = "warsun"
