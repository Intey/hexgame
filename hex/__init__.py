from typing import List
from enum import Enum
from dataclasses import dataclass, field
from random import randint

POSSIBLE_JOINS_MAP = [
        ('rc', 'lc'),
        ('lc', 'rc'),
        ('rd', 'lu'),
        ('ru', 'ld'),
        ('ld', 'ru'),
        ('lu', 'rd'),
        ]

def neighbors(p1):
    yield (p1[0], p1[1]-1)
    yield (p1[0], p1[1]+1)
    yield (p1[0]-1, p1[1])
    yield (p1[0]+1, p1[1])
    yield (p1[0]-1, p1[1]+1)
    yield (p1[0]+1, p1[1]+1)



def isneighbors(p1, p2):
    return p2 in neighbors(p1)

def has_join(h1, h2, biome=None):
    joins = []
    for h1_side, h2_side in POSSIBLE_JOINS_MAP:
        h1_biome = getattr(h1, h1_side)
        h2_biome = getattr(h2, h2_side)

        if h1_biome == biome:
            if not boime or biome and h2_biome == biome:
                joins.append((h1_side, h2_side))


@dataclass
class PlaceResult:
    joins: List = field(default_factory=list)


class Biome(Enum):
    ROAD = 1
    WATER = 2
    LAND = 3
    VILLAGE = 4
    FOREST = 5
    MOUNTAIN = 6


@dataclass
class Hex:
    lc: Biome
    lu: Biome
    ru: Biome
    rc: Biome
    rd: Biome
    ld: Biome

    def has_biome(self, biome):
        mapping = {
                'lc': self.lc,
                'lu': self.lu,
                'ru': self.ru,
                'rc': self.rc,
                'rd': self.rd,
                'ld': self.ld,
        }

        for k,v in mapping.items():
            if v == biome:
                return k

class Map:
    """
    x - from left to right
    y - from up to down

    / \ / \ / \ / \
   |0 0|0 1|0 2|0 3|
    \ / \ / \ / \ / \
     |1 0|1 1|1 2|1 3|
    / \ / \ / \ / \ /
   |2 0|2 1|2 2|2 3|
    \ / \ / \ / \ /


    """
    def __init__(self, generator):
        self.hxs = {}
        self.generator = generator.start()
        self.linkage = {}


    def place_next(self, y, x) -> PlaceResult:
        point = (y, x)
        # make meta map
        new_hex = next(self.generator)


        for neighbor_point in neighbors(point):
            neighbor = self.hxs.get(neighbor_point)
            if neighbor:
                self.calc_score(p1, p2)
                self.build_routes(p1, p2)
                # score points


        place_result = PlaceResult()
        return place_result

    def build_routes(self, p1, p2):
        # make route from p1, p2 if they has joined by road
        if has_join(p1, p2, Biome.ROAD):
            self.join_route(p1, p2)
            # optimize and merge duplicates
            p1_routes = find_route_for_point(self, p1)
            p2_routes = find_route_for_point(self, p2)


    def calc_score(self, p1, p2):
        pass


    def find_routes_for_point(self, point):
        return [route
            for route in self.routes
            if point in route]

    def join_route(self, *points):
        new_route_idx = len(self.routes)
        self.routes.append(points)
        for p in points:
            point_linkage = self.linkage.get(p, {})
            self.linkage[p] = point_linkage
            point_linkage.get("routes", {})

# / \ / \ / \ / \
#|0 0|0 1|0 2|0 3|
# \ / \ / \ / \ / \
#  |1 0|1 1|1 2|1 3|
# / \ / \ / \ / \ /
#|2 0|2 1|2 2|2 3|
# \ / \ / \ / \ /
#
# bidirectional routes
# 00->01->02->11
# 00->01->02->03
# 00->01->10
# 03

# example_linkage = {
#         (0,0): {
#             "routes": {
#                 "a": (0,1),
#                 "b": (0,1),
#                 }
#             },
#         (0,1): {
#             "routes": {
#                 }
#             }
#         (0,1): {
#             "routes": {
#                 }
#             }
#
#         }
#
# villages = {
#         (0,0): "A",
#         (2,3): "C"
#         }
