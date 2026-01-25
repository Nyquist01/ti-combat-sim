from abc import ABC


class Ship(ABC):
    def __init__(
        self,
        hp: int,
        combat: int,
        rolls: int,
        priority: int,
        name: str,
        cost: int,
        has_antifighter_barrage: bool = False,
    ):
        self.hp = hp
        self.combat = combat
        self.rolls = rolls
        self.priority = priority
        self.name = name
        self.cost = cost
        self.has_antifighter_barrage = has_antifighter_barrage

    def take_damage(self):
        self.hp -= 1

    def __repr__(self):
        return f"<name={self.name} hp={self.hp}>"


class Dreadnought(Ship):
    def __init__(self):
        super().__init__(
            name="dreadnought", hp=2, combat=5, rolls=1, priority=2, cost=4
        )


class Fighter(Ship):
    def __init__(self):
        super().__init__(name="fighter", hp=1, combat=9, rolls=1, priority=4, cost=0.5)


class Carrier(Ship):
    def __init__(self):
        super().__init__(name="carrier", hp=1, combat=9, rolls=1, priority=5, cost=3)


class Destroyer(Ship):
    def __init__(self):
        super().__init__(
            name="destroyer",
            hp=1,
            combat=1,
            rolls=1,
            priority=3,
            cost=1,
            has_antifighter_barrage=True,
        )


class Warsun(Ship):
    def __init__(self):
        super().__init__(name="warsun", hp=2, combat=3, rolls=3, cost=12, priority=1)
