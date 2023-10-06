import datetime
import re

def get_blueprints(input_path):
    with open(input_path) as input:
        lines = input.read().split('\n')

        blueprints = []

        for l in lines:
            numbers = [int(m) for m in re.findall(r'\d+', l)]

            blueprints.append(
                Blueprint(numbers[0], numbers[1], numbers[2], numbers[3:5], numbers[5:])
            )
        
        return blueprints


ORE = 'ore'
CLAY = 'clay'
OBSIDIAN = 'obs'
GEODE = 'geo'

ORE_BOT = 'ore_r'
CLAY_BOT = 'clay_r'
OBSIDIAN_BOT = 'obs_r'
GEODE_BOT = 'geo_r'

ORE_IDX = 0
CLAY_IDX = 1
OBS_IDX = 2
GEO_IDX = 3

ORE_R_IDX = 4
CLAY_R_IDX = 5
OBS_R_IDX = 6
GEO_R_IDX = 7

BUILD_IDX = 8


class Blueprint():
    def __init__(self, id, ore_r, clay_r, obs_r, geo_r):
        self.id = id
        self.ore_r = ore_r
        self.clay_r = clay_r
        self.obs_r = obs_r
        self.geo_r = geo_r


def get_available_builds(inventory, b: Blueprint):
    available = []

    if inventory[ORE_IDX] >= b.geo_r[0] and inventory[OBS_IDX] >= b.geo_r[1]:
        available.append(GEO_R_IDX)

    if inventory[ORE_IDX] >= b.obs_r[0] and inventory[CLAY_IDX] >= b.obs_r[1]:
        available.append(OBS_R_IDX)

    if inventory[ORE_IDX] >= b.clay_r:
        available.append(CLAY_R_IDX)

    if inventory[ORE_IDX] >= b.ore_r:
        available.append(ORE_R_IDX)

    return available


def get_best_geode_return(b: Blueprint, minutes = 24) -> int:
    initial_inventory = [
        0,0,0,0,
        1,0,0,0,
        None
    ]

    highest_ore_cost = max(b.ore_r, b.clay_r, b.obs_r[0], b.geo_r[0])

    current_minute_inventory_branches = [initial_inventory]
    start = datetime.datetime.now()
        
    for _ in range(minutes):
        if _ > 20:
            # print(f'Blueprint ID: {b.id} - Minute {_} - Branches {len(current_minute_inventory_branches)} ({datetime.datetime.now() - start})')
            pass
        next_minute_inventory_branches = []

        while len(current_minute_inventory_branches) > 0:
            inv = current_minute_inventory_branches.pop()
            current_inventories = []

            # only further the gathering branch if there's something unaffordable and we are currently collecting it
            if (inv[ORE_IDX] < highest_ore_cost or
                (inv[CLAY_IDX] < b.obs_r[1] and inv[CLAY_R_IDX] > 0) or
                inv[OBS_IDX] < b.geo_r[1] and inv[OBS_R_IDX] > 0):
                current_inventories.append(inv)

            available_builds = get_available_builds(inv, b)

            # create new inventories for each build choice
            for build in available_builds:
                new_inv = inv[:]
                new_inv[BUILD_IDX] = build

                # always build
                if build is GEO_R_IDX:
                    new_inv[ORE_IDX] -= b.geo_r[0]
                    new_inv[OBS_IDX] -= b.geo_r[1]
                    current_inventories.append(new_inv)

                # only build if fewer than obs cost of geode bot
                elif build is OBS_R_IDX and new_inv[OBS_R_IDX] < b.geo_r[1]:
                    new_inv[ORE_IDX] -= b.obs_r[0]
                    new_inv[CLAY_IDX] -= b.obs_r[1]
                    current_inventories.append(new_inv)

                # only build if fewer than clay cost of obs bot
                elif build is CLAY_R_IDX and new_inv[CLAY_R_IDX] < b.obs_r[1]:
                    new_inv[ORE_IDX] -= b.clay_r
                    current_inventories.append(new_inv)

                # only build if fewer than highest ore cost of blueprint
                elif build is ORE_R_IDX and new_inv[ORE_R_IDX] < highest_ore_cost:
                    new_inv[ORE_IDX] -= b.ore_r
                    current_inventories.append(new_inv)

            for c_inv in current_inventories:
                c_inv[ORE_IDX] += c_inv[ORE_R_IDX]
                c_inv[CLAY_IDX] += c_inv[CLAY_R_IDX]
                c_inv[OBS_IDX] += c_inv[OBS_R_IDX]
                c_inv[GEO_IDX] += c_inv[GEO_R_IDX]

                if c_inv[BUILD_IDX] is not None:
                    c_inv[c_inv[BUILD_IDX]] += 1
                    c_inv[BUILD_IDX] = None

            next_minute_inventory_branches.extend(current_inventories)
        

        # Only keep the inventories with the most high-tier robots (super not happy with this...)
        # No longer works for part 1, real input
        most_geode_robots = 0
        most_obsidian_robots = 0

        for i in next_minute_inventory_branches:
            most_geode_robots = max(most_geode_robots, i[GEO_R_IDX])
            most_obsidian_robots = max(most_obsidian_robots, i[OBS_R_IDX])

        current_minute_inventory_branches = [
            i for i in next_minute_inventory_branches
            if i[GEO_R_IDX] >= most_geode_robots - 1 and i[OBS_R_IDX] >= most_obsidian_robots - 3]

    highest_geode_return = max([i[GEO_IDX] for i in current_minute_inventory_branches])

    return highest_geode_return


def part_1(input_path="input/day_19.txt"):
    blueprints = get_blueprints(input_path)
    geode_returns = [get_best_geode_return(b) for b in blueprints]

    # print(geode_returns)

    return sum([g * (i + 1) for i, g in enumerate(geode_returns)])


def part_2(input_path="input/day_19.txt"):
    blueprints = get_blueprints(input_path)

    n_blueprints = len(blueprints)
    last_bluprint = n_blueprints if n_blueprints < 3 else 3

    geode_returns = [get_best_geode_return(b, 32) for b in blueprints[0:last_bluprint]]

    # print(geode_returns)

    product = 1

    for g in geode_returns:
        product *= g

    return product