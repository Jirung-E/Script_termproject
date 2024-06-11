import sidekick
from charger import GeoCoord
from apis import distance2_between, zoom_path

import random
from time import time


coord_list = [GeoCoord(random.uniform(37.0, 38.0), random.uniform(127.0, 128.0)) for _ in range(1_000_000)]


def test2():
    center = GeoCoord(random.uniform(37.0, 38.0), random.uniform(127.0, 128.0))
    start = time()
    idx, f = sidekick.furthest_marker(center, coord_list)
    print(idx)
    print(f.lat, f.lng)
    end = time()
    print(end - start)

    # start = time()
    # f = furthest_marker(coord_list, GeoCoord(37.5, 127.5))[1]
    # # print(f.lat, f.lng)
    # end = time()
    # print(end - start)


def test5():
    zoom = 13

    start = time()
    in_map1 = sidekick.only_in_map(coord_list, GeoCoord(37.5, 127.5), 0.055 * (2 ** (13 - zoom)))
    end = time()
    print(end - start)

    # start = time()
    # in_map2 = only_in_map(coord_list, GeoCoord(37.5, 127.5), zoom)
    # end = time()
    # print(end - start)

    # print(len(in_map1), len(in_map2))
    # assert len(in_map1) == len(in_map2)
    # for i in range(len(in_map1)):
    #     assert in_map1[i].lat == in_map2[i].lat
    #     assert in_map1[i].lng == in_map2[i].lng





# test1()
# test1()
# test1()
# test1()
# test1()
# test1()
# test1()
# test1()

test2()
test2()
test2()
test2()
test2()
test2()
test2()
test2()
test2()
test2()
test2()
test2()
test2()
test2()

# print()
# print()

# test3()
# test3()
# test3()
# test3()

# print()

# test4()
# test4()
# test4()
# test4()
# test4()

# print()

# test5()
# test5()
# test5()
# test5()
# test5()
# test5()
# test5()
# test5()
# test5()
# test5()
# test5()
# test5()
# test5()

print("Done!")