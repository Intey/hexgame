from cells.entities import Map, Cell, Biome
from random import choice


class DumpGenerator:
    def __init__(self, config=None):
        if config is None:
            config = []
        self.config = config
        self.mapping = {
                'R': Biome.ROAD,
                'L': Biome.LAND,
                'W': Biome.WATER,
                'V': Biome.VILLAGE
        }

    def start(self):
        for conf in self.config:
            yield Cell(*[self.mapping[ch] for ch in conf])
        while True:
            yield Cell(*[choice(list(self.mapping.values())) for i in range(6)])


def test_map_get_item():
    gen = DumpGenerator()
    cell_map = Map(gen)
    cell_map.place_next(0, 0)
    cell_map.place_next(0, 1)
    cell_map.place_next(0, 2)
    cell_map.place_next(0, 3)
    assert cell_map[(0,0)]
    assert cell_map[(0,1)]
    assert cell_map[(0,2)]
    assert cell_map[(0,3)]


def test_create_trade_route():
    """check that when we link 2 villages, we get trade route
    """
    gen = DumpGenerator([
        'VLLRLL',
        'RLLRRL',
        'RLLVLL',
        'LRLVLL',
        ])

    cell_map = Map(gen)


    # 01:
    #   1: lc: 00, rc: 02
    #   2: lc: 00, rd: 11
    #   3: rc: 02, rd: 11
    #
    # 00:
    #   1: rc: 01
    #   2: rc: 01
    #
    #  /  \    /  \    /  \
    # V-00-R--R-01-R--R-02-V
    #  \  /    \  /    \  /
    #      /  \    /  \    /  \
    #     | 10 |  | 11 |  | 12 |
    #      \  /    \  /    \  /

    cell_map.place_next(0,0)
    cell_map.place_next(0,1)
    cell_map.place_next(0,2)
    # all points should has route
    assert cell_map[(0,0)].trade_routes['1']
    assert cell_map[(0,1)].trade_routes['1']
    assert cell_map[(0,2)].trade_routes['1']


def test_traverse_route():
    gen = DumpGenerator([
        'VLLRLL',
        'RLLRLL',
        'RLLVLL',
        ])
    cell_map = Map(gen)
    cell_map.place_next(0,0)
    cell_map.place_next(0,1)
    cell_map.place_next(0,2)
    cell = cell_map[(0,0)]
    route = cell.trade_routes['1']
    route_walker = route.traverse()
    assert next(route_walker) == cell_map[(0,1)]
    assert next(route_walker) == cell_map[(0,2)]

    # backward
    cell = cell_map[(0,2)]
    route = cell.trade_routes['1']
    route_walker = route.traverse()
    assert next(route_walker) == cell_map[(0,1)]
    assert next(route_walker) == cell_map[(0,0)]


def test_traverse_route_overlapping():

    #  /  \    /  \    /  \
    # V-00-R--R-01-R--R-02-V
    #  \  /    \  R    \  /
    #      /  \    R  \    /  \
    #     | 10 |  | 11-V  | 12 |
    #      \  /    \  /    \  /

    gen = DumpGenerator([
        'VLLRLL',
        'RLLRRL',
        'RLLVLL',
        'LRLVLL',
        ])
    cell_map = Map(gen)
    cell_map.place_next(0,0)
    cell_map.place_next(0,1)
    cell_map.place_next(0,2)
    cell_map.place_next(1,1)
    cell = cell_map[(0,0)]
    assert len(cell.trade_routes) == 2

    route = cell.trade_routes['2']
    route_walker = route.traverse()
    assert next(route_walker) == cell_map[(0,1)]
    assert next(route_walker) == cell_map[(1,1)]

    assert len(cell_map[(0,1)].trade_routes) == 3
