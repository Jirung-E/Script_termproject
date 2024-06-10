import sidekick
from charger import GeoCoord
from apis import distance2_between, furthest_marker

import random
from time import time


print(sidekick.hello())

sidekick.pass_GeoCoord(GeoCoord(37.123, 127.123))



coord_list = [GeoCoord(random.uniform(37.0, 38.0), random.uniform(127.0, 128.0)) for _ in range(1000000)]


def test1():
    start = time()

    d = 0
    o = GeoCoord(37.5, 127.5)
    for coord in coord_list:
        d += distance2_between(coord, o) ** 0.5
    d = d / len(coord_list)

    end = time()

    print(end - start)
    print(d)


    start = time()

    d = 0
    o = GeoCoord(37.5, 127.5)
    for coord in coord_list:
        d += sidekick.distance2_between(coord, o) ** 0.5
    d = d / len(coord_list)
        
    end = time()

    print(end - start)
    print(d)


def test2():
    start = time()
    f = furthest_marker(coord_list, GeoCoord(37.5, 127.5))[1]
    print(f.lat, f.lng)
    end = time()
    print(end - start)

    start = time()
    f = sidekick.furthest_marker(GeoCoord(37.5, 127.5), coord_list)
    print(f.lat, f.lng)
    end = time()
    print(end - start)


test2()