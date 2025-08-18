from ships import *

class Player:
    def __init__(self, build_order):
        self.build_order = build_order
        self.hp = 25
        self.lines = 0
        self.ships = []
        self.build_step = 0
        self.points = 0
        self.ship_log = []
        self.roll = 0

    def add_ship(self, ship):
        for i in range(self.count_ship(Dreadnought)):
            self.ships.append(Fighter.make(self.roll))
        self.ships.append(ship)

    def display_build(self):
        return ', '.join(name for name in self.build_order)

    def display_ships(self):
        return ', '.join(ship.display() for ship in self.ships)

    def remove_ship(self, ship_type):
        for i, ship in enumerate(self.ships):
            if isinstance(ship, ship_type):
                self.ships.pop(i)
                break

    def buy_ship(self):
        buying = True
        while buying:
            desired_ship_name = self.build_order[self.build_step]
            desired_ship = find_ship(desired_ship_name)
            could_build = self.attempt_to_draw(desired_ship)
            if could_build:
                self.next_build()
            else:
                buying = False
        for ship in self.ships:
            if isinstance(ship, Carrier) and ship.ready:
                if ship.can_spawn(ship.preference):
                    ship.spawn(ship.preference, self)
                elif ship.can_spawn(Defender):
                    ship.spawn(Defender, self)

    def attempt_to_draw(self, desired_ship):
        if desired_ship.name == Orbital.name and self.count_ship(Orbital) >= 6:
            return False # skip
        for ship in self.ships:
            if isinstance(ship, Carrier) and ship.can_spawn(desired_ship):
                ship.spawn(desired_ship, self)
                return True
        if issubclass(desired_ship, UpgradedShip):
            result = desired_ship.can_upgrade(self)
            if result is False:
                return False
            if result is True:
                desired_ship.pay_cost(self)
                self.add_ship(desired_ship.make(self.roll))
                self.ship_log.append(desired_ship)
                return True
            self.attempt_to_draw(result)
            return False
        if desired_ship.can_draw(self):
            desired_ship.pay_cost(self)
            ship = desired_ship.make(self.roll)
            self.add_ship(ship)
            self.ship_log.append(ship)
            return True
        else:
            return False

    def next_build(self):
        if self.build_step < len(self.build_order) - 1:
            self.build_step += 1

    def count_ship(self, ship_to_count):
        return sum(1 if ship.name == ship_to_count.name else 0 for ship in self.ships)

    def count_used_carriers(self):
        return sum(1 if isinstance(ship, Carrier) and ship.charges == 0 else 0 for ship in self.ships)

    def types(self):
        types_found = []
        for ship in self.ships:
            name = Carrier.name if isinstance(ship, Carrier) else ship.name
            if name not in types_found:
                types_found.append(name)
        return len(types_found)
