import sidekick
from charger import GeoCoord
from apis import distance2_between, furthest_marker, zoom_path

import random
from time import time


coord_list = [GeoCoord(random.uniform(37.0, 38.0), random.uniform(127.0, 128.0)) for _ in range(1_000_000)]


def test2():
    start = time()
    f = sidekick.furthest_marker(GeoCoord(37.5, 127.5), coord_list)
    # print(f.lat, f.lng)
    end = time()
    print(end - start)

    start = time()
    f = furthest_marker(coord_list, GeoCoord(37.5, 127.5))[1]
    # print(f.lat, f.lng)
    end = time()
    print(end - start)


def test3():
    start = time()
    sorted_list1 = sidekick.sort_by_distance(coord_list, GeoCoord(37.5, 127.5))
    end = time()
    print(end - start)
    
    start = time()
    sorted_list2 = sorted(coord_list, key=lambda coord: distance2_between(coord, GeoCoord(37.5, 127.5)))
    end = time()
    print(end - start)         # 이게 더 빠르네........  

    for i in range(len(sorted_list1)):
        assert sorted_list1[i].lat == sorted_list2[i].lat
        assert sorted_list1[i].lng == sorted_list2[i].lng


def test4():
    zoom = 13

    start = time()
    zoomed_path1 = sidekick.zoom_path(coord_list, (0.055 * (2 ** (13 - zoom))) / 20)
    end = time()
    print(end - start)

    start = time()
    zoomed_path2 = zoom_path(coord_list, zoom)
    end = time()
    print(end - start)

    for i in range(len(zoomed_path1)):
        assert zoomed_path1[i].lat == zoomed_path2[i].lat
        assert zoomed_path1[i].lng == zoomed_path2[i].lng



test2()
test2()
test2()
test2()
test2()

print()
print()

test3()
test3()
test3()
test3()

print()

test4()
test4()
test4()
test4()
test4()

print("Done!")