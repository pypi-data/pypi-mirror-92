from multipolygon.inpolygon import isinpolygon
from multipolygon.inpolygon import isintersect

def isin_multipolygon(poi, vertex_lst, contain_boundary=True):
    if not isinpolygon(poi, vertex_lst, contain_boundary):
        return False
    sinsc = 0
    for spoi, epoi in zip(vertex_lst[:-1], vertex_lst[1::]):
        intersect = isintersect(poi, spoi, epoi)
        if intersect is None:
            return (False, True)[contain_boundary]
        elif intersect:
            sinsc += 1
    return sinsc % 2 == 1

