import random


class Ship:
    damage: int
    healing: int
    cost: int
    name: str

    def get_damage(self, player):
        return self.damage

    def display(self):
        return self.name

    @classmethod
    def make(cls, roll):
        return cls()

class BasicShip(Ship):
    @classmethod
    def can_draw(cls, player):
        return player.lines >= cls.cost

    @classmethod
    def pay_cost(cls, player):
        player.lines -= cls.cost


class Defender(BasicShip):
    name = 'Defender'
    cost = 2
    damage = 0
    healing = 1

class Fighter(BasicShip):
    name = 'Fighter'
    cost = 3
    damage = 1
    healing = 0

class Commander(BasicShip):
    name = 'Commander'
    cost = 4
    healing = 0

    def get_damage(self, player):
        return player.count_ship(Fighter) // 3

class Interceptor(BasicShip):
    name = 'Interceptor'
    cost = 4
    healing = 0

    def __init__(self):
        self.charges = 1

    def get_damage(self, player):
        if self.charges == 0:
            return 0
        self.charges = 0
        return 5

class Orbital(BasicShip):
    name = 'Orbital'
    cost = 6
    damage = 0
    healing = 0

class Carrier(BasicShip):
    name = 'Carrier'
    cost = 6
    damage = 0
    healing = 0

    def __init__(self, preference):
        self.charges = 6
        self.ready = False
        self.preference = preference

    def can_spawn(self, ship):
        if not self.ready:
            return False
        if ship.name == Defender.name and self.charges >= Defender.cost:
            return True
        if ship.name == Fighter.name and self.charges >= Fighter.cost:
            return True
        return False

    def spawn(self, ship, player):
        if not self.ready:
            return
        if ship.name == Defender.name:
            self.charges -= Defender.cost
        if ship.name == Fighter.name:
            self.charges -= Fighter.cost
        player.add_ship(ship.make(player.roll))
        self.ready = False

    def display(self):
        return f'{self.name}<{self.charges}>'

    @classmethod
    def make(cls, roll):
        return random.choice([CarrierFighter, CarrierDefender])()

class CarrierDefender(Carrier):
    name = 'Carrier - Defender'

    def __init__(self):
        super().__init__(Defender)

class CarrierFighter(Carrier):
    name = 'Carrier - Fighter'

    def __init__(self):
        super().__init__(Fighter)

class Starship(BasicShip):
    name = 'Starship'
    cost = 8
    healing = 0

    def __init__(self):
        self.dealt_damage = False

    def get_damage(self, player):
        if self.dealt_damage:
            return 0
        self.dealt_damage = True
        return 8

class UpgradedShip(Ship):
    prerequisites: dict

    @classmethod
    def can_upgrade(cls, player):
        for ship, required in cls.prerequisites.items():
            if ship.name == Carrier.name:
                count = player.count_used_carriers()
            else:
                count = player.count_ship(ship)
            if count < required:
                return ship
        return player.lines >= cls.cost

    @classmethod
    def pay_cost(cls, player):
        for ship, quantity in cls.prerequisites.items():
            for i in range(quantity):
                player.remove_ship(ship)
        player.lines -= cls.cost

class Battlecruiser(UpgradedShip):
    name = 'Battlecruiser'
    healing = 3
    damage = 2
    cost = 6
    prerequisites = {
        Orbital: 1,
        Fighter: 2,
        Defender: 1,
    }

class Tactical(UpgradedShip):
    name = 'Tactical Cruiser'
    healing = 0
    cost = 3
    prerequisites = {
        Fighter: 1,
        Defender: 2,
    }

    def get_damage(self, player):
        return player.types()

class Frigate(UpgradedShip):
    name = 'Frigate'
    healing = 2
    cost = 3
    prerequisites = {
        Fighter: 1,
        Defender: 1,
    }

    def __init__(self, number):
        self.number = number

    def get_damage(self, player):
        return 6 if self.number == player.roll else 0

    @classmethod
    def make(cls, roll):
        return Frigate(roll)


class ScienceVessel(UpgradedShip):
    name = 'Science Vessel'
    damage = 0
    healing = 0
    cost = 4
    prerequisites = {
        Fighter: 1,
        Defender: 1,
        Starship: 1,
    }

class Dreadnought(UpgradedShip):
    name = 'Dreadnought'
    healing = 0
    damage = 10
    cost = 10
    prerequisites = {
        Fighter: 3,
        Defender: 2,
        Commander: 1,
    }

class Leviathan(UpgradedShip):
    name = 'Leviathan'
    healing = 12
    damage = 12
    cost = 12
    prerequisites = {
        Carrier: 2,
        Starship: 2,
        Defender: 2,
    }


def find_ship(name):
    if name == CarrierDefender.name:
        return CarrierDefender
    if name == CarrierFighter.name:
        return CarrierFighter
    return next(ship for ship in ships if ship.name == name)

ships = [Defender, Fighter, Commander, Interceptor, Orbital, Carrier, Starship, Battlecruiser, Frigate, Tactical, ScienceVessel, Dreadnought, Leviathan]
