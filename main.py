from ships import *
from player import Player

def main():
    new_build_orders = [[get_random_ship() for _ in range(5)]] * 20
    for i in range(10):
        for j in range(100):
            random.shuffle(new_build_orders)
            build_orders = run_iteration(new_build_orders)
        print(build_orders[-1])
        new_build_orders = [build_orders[-1]] * 20
    for build_order in build_orders:
        print(build_order)

def run_iteration(build_orders):
    points = [{'score': 0} for _ in build_orders]
    for i, build_order in enumerate(build_orders):
        for j, other in enumerate(build_orders):
            if i == j:
                continue
            total_points_i, total_points_j = 0, 0
            # print('starting best of three between')
            # print(build_order)
            # print(other)
            for k in range(3):
                players = [Player(build_order), Player(other)]
                players = determine_winner(players)
                for index, player in zip([i, j], players):
                    actual_build = [ship.name for ship in player.ship_log] + player.build_order[player.build_step:]
                    end_ship = actual_build[-1]
                    n = 0
                    for n in range(len(actual_build) - 1, -1, -1):
                        if actual_build[n] != end_ship:
                            break
                    build_orders[index] = actual_build[:min(n + 2, 20)]
                points_i, points_j = players[0].points, players[1].points
                total_points_i += points_i
                total_points_j += points_j
            if total_points_i == total_points_j:
                final_score_i, final_score_j = 1, 1
            elif total_points_i > total_points_j:
                final_score_i, final_score_j = 3, 0
            else:
                final_score_i, final_score_j = 0, 3
            # print(final_score_i, final_score_j)
            points[i]['score'] += final_score_i
            points[j]['score'] += final_score_j
    for i, record in enumerate(points):
        record['build'] = build_orders[i]
    points = sorted(points, key=lambda point: point['score'])
    build_orders = [record['build'] for record in points[(len(points) // 2):]]
    print('champion:', build_orders[-1])
    mutant_build_orders = []
    for i, build_order in enumerate(build_orders):
        copies = i - 5
        if copies < 1:
            continue
        for j in range(copies):
            mutant_build_order = create_mutant(build_order)
            # print('origin:', build_order)
            # print('mutant:', mutant_build_order)
            mutant_build_orders.append(mutant_build_order)
    build_orders = mutant_build_orders + build_orders
    return build_orders


def create_mutant(build_order):
    mutant_build_order = []
    for ship in build_order:
        choice = random.randint(1, 10)
        if choice <= 1:
            mutant_build_order.append(get_random_ship())
        elif choice <= 2:
            continue
        elif choice <= 3:
            mutant_build_order.append(ship)
            mutant_build_order.append(ship)
        else:
            mutant_build_order.append(ship)
    match (random.choice(['add', 'remove'])):
        case 'add':
            mutant_build_order.insert(random.randint(1, len(mutant_build_order)) - 1, get_random_ship())
        case 'remove':
            if len(mutant_build_order) > 1:
                mutant_build_order.pop(random.randint(0, len(mutant_build_order) - 1))
    return mutant_build_order


def get_random_ship():
    return random.choice(ships).make(roll=0).name


def determine_winner(players):
    total_roll = 0
    while all(player.hp > 0 for player in players):
        roll = random.randint(1, 6)
        total_roll += roll
        if total_roll > 500:
            players[0].points, players[1].points = 1, 1
            return players
        for player in players:
            if player.count_ship(Leviathan) > 0:
                player.roll = 6
            else:
                player.roll = roll
            player.lines += player.roll
            player.lines += player.count_ship(Orbital) + player.count_ship(Battlecruiser) * 2
            for ship in player.ships:
                if isinstance(ship, Carrier):
                    ship.ready = True
            player.buy_ship()
        # print(roll)
        # for player in players:
        #     print(player.hp, player.lines, player.display_ships())
        for i, player in enumerate(players):
            damage, healing = 0, 0
            for ship in player.ships:
                damage += ship.get_damage(player)
                healing += ship.healing
            player.hp += healing
            if player.count_ship(ScienceVessel) > 0:
                player.hp += healing
            # print('heal', healing)
            # print('damage', damage)
            players[(i + 1) % 2].hp -= damage
        for player in players:
            player.hp = min(player.hp, 35)
        # input()
    if players[0].hp == players[1].hp:
        players[0].points, players[1].points = 1, 1
    elif players[0].hp > players[1].hp:
        players[0].points, players[1].points = 3, 0
    else:
        players[0].points, players[1].points = 0, 3
    return players


if __name__ == '__main__':
    main()
