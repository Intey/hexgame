# from random import randint
from typing import List, Tuple, Dict, Optional
from enum import Enum
from dataclasses import dataclass, field

from cells.utils import side_to_pos, neighbors, has_join


class Biome(Enum):
    ROAD = 1
    WATER = 2
    LAND = 3
    VILLAGE = 4
    FOREST = 5
    MOUNTAIN = 6


@dataclass
class Cell:
    lc: Biome
    lu: Biome
    ru: Biome
    rc: Biome
    rd: Biome
    ld: Biome
    # list of routes
    trade_routes: Dict = field(default_factory=dict)

    def has_biome(self, biome) -> List[str]:
        """ return sides with this biome
        """
        mapping = {
                'lc': self.lc,
                'lu': self.lu,
                'ru': self.ru,
                'rc': self.rc,
                'rd': self.rd,
                'ld': self.ld,
        }

        return [k for k, v in mapping.items() if v == biome]

    def add_to_route(self, route_id, side):
        route = self.trade_routes.get(route_id)
        if not route:
            self.trade_routes[route_id] = set()

        self.trade_routes[route_id].add(side)

    def get_route_sides(self, route_id):
        """
        return sides, on which route belongs
        """
        sides = self.trade_routes[route_id]
        return sides


class Map:
    """
    x - from left to right
    y - from up to down

    """
    #  / \ / \ / \ / \
    # |0 0|0 1|0 2|0 3|
    #  \ / \ / \ / \ / \
    #   |1 0|1 1|1 2|1 3|
    #  / \ / \ / \ / \ /
    # |2 0|2 1|2 2|2 3|
    #  \ / \ / \ / \ /

    def __init__(self, generator):
        self.cells = {}
        self.generator = generator.start()
        self.last_trade_route = 1
        self.last_road = 1
        self.villages = {}

    @property
    def trade_routes(self):
        result = {}
        for point, cell in self.villages.items():
            # make routes init villages
            for route in cell.trade_routes:
                if result.get(route) is None:
                    result[route] = set()
                result[route].add(point)


    def place_next(self, y, x) -> dict:
        point = (y, x)
        # make meta map
        new_cell = next(self.generator)
        self.cells[point] = new_cell

        # collect vvillages
        has_village = new_cell.has_biome(Biome.VILLAGE)
        if has_village:
            self.villages[point] = new_cell

        for side, neighbor_point in neighbors(point):
            neighbor = self.cells.get(neighbor_point)
            if neighbor:
                self.calc_score(point, neighbor_point)
        self.build_routes(point)

        # make trade route

        return {}

    def build_routes(self, new_point: Tuple[int, int]):
        new_cell = self.cells[new_point]
        if not new_cell.has_biome(Biome.VILLAGE):
            return

        neighbor = None
        neighbor_side = None

        for side, neighbor_point in neighbors(point):
            neighbor = self.cells.get(neighbor_point)
            if neighbor:
                neighbor_side = side
                break

        if not neighbor:
            return

        path = [new_point, neighbor]

        exist_cell = self.cells[neighbor]
        new_cell_join_side = has_join(new_cell, exist_cell, Biome.ROAD)
        if new_cell_join_side:



    def calc_score(self, p1, p2):
        pass

    def join_route(self, p1, p2):
        pass

    def __getitem__(self, point):
        return self.cells[point]


class Route:
    def __init__(self, name, start_village_point, map_: Map):
        self.name = name
        self.start_village = start_village_point
        self.map = map_
        # self.path = path

    def traverse(self):
        # where i know next?
        current_point = self.start_village
        sides = self.map[current_point].get_route_sides(self.name)
        # route should has only 1 way
        # start village should has only 1 side for route
        assert len(sides) == 1
        # start village
        current_point = side_to_pos(current_point, sides[0])
        yield self.map[current_point]

        backward_side = POSSIBLE_JOINS_MAP[sides[0]]
        sides = [1,2]
        while len(sides) > 1:
            sides = self.map[current_point].get_route_sides(self.name)
            # intermediate cell should has only 2 sides with route, because route should has only 1 way
            assert len(sides) <= 2
            # check that we didn't go backward
            # for new point we should check only sides, that not linked with previous cell
            for side in sides:
                if side != backward_side:
                    current_point = self.map(side_to_pos(current_point, side))
                    yield self.map[current_point]
            # on route
            # throw out from side



