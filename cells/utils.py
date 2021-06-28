from typing import List, Tuple, Optional
import typing as t
if t.TYPE_CHECKING:
    from cells.entities import Biome, Cell


POSSIBLE_JOINS_MAP = {
        'rc': 'lc',
        'lc': 'rc',
        'rd': 'lu',
        'ru': 'ld',
        'ld': 'ru',
        'lu': 'rd',
        }


#  / \ / \ / \ / \
# |0 0|0 1|0 2|0 3|
#  \ / \ / \ / \ / \
#   |1 0|1 1|1 2|1 3|
#  / \ / \ / \ / \ /
# |2 0|2 1|2 2|2 3|
#  \ / \ / \ / \ /


def side_to_pos(point: Tuple[int, int], side: str) -> Tuple[int, int]:
    return {'lc': (point[0], point[1]-1),
            'rc': (point[0], point[1]+1),
            'lu': (point[0]-1, point[1]),
            'ld': (point[0]+1, point[1]),
            'ru': (point[0]-1, point[1]+1),
            'rd': (point[0]+1, point[1]+1),
            }[side]


def neighbors(p1) -> List[Tuple[str, Tuple[int, int]]]:
    return [('lc', (p1[0], p1[1]-1)),
            ('rc', (p1[0], p1[1]+1)),
            ('lu', (p1[0]-1, p1[1])),
            ('ld', (p1[0]+1, p1[1])),
            ('ru', (p1[0]-1, p1[1]+1)),
            ('rd', (p1[0]+1, p1[1]+1))]


def has_join(h1: "Cell", h2: "Cell", biome: "Biome"=None, h1_side: str=None) -> Optional[str]:
    if h1_side:
        h2_side = POSSIBLE_JOINS_MAP[h1_side]
        h1_biome: "Biome" = getattr(h1, h1_side)
        h2_biome: "Biome" = getattr(h2, h2_side)
        matched = __match(h1_biome, h2_biome, biome)
        if matched:
            return h1_side
        else:
            return None
    else:
        for h1_side, h2_side in POSSIBLE_JOINS_MAP.items():
            h1_biome = getattr(h1, h1_side)
            h2_biome = getattr(h2, h2_side)
            matched = __match(h1_biome, h2_biome, biome)
            if matched:
                return h1_side
    return None


def __match(h1_biome: "Biome", h2_biome: "Biome", biome: "Biome" = None):
    if biome:
        return h1_biome == h2_biome == biome
    return h1_biome == h2_biome


