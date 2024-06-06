import requests
import io
from PIL import Image
from googlemaps import Client
from typing import List, Dict

from charger import *


def get_region_code(key, addr: str):
    url = "http://apis.data.go.kr/1741000/StanReginCd/getStanReginCdList"
    url += "?serviceKey=" + key
    url += "&type=json"
    url += "&locatadd_nm=" + addr

    data = requests.get(url).json()

    try:
        code = data["StanReginCd"][1]["row"][0]["region_cd"][:5]
    except:
        print(data)
        return None

    return code


def get_chargers_in_region(key, region_code, page=1) -> List[ChargerGroup]:
    url = "http://apis.data.go.kr/B552584/EvCharger/getChargerInfo"
    queryParams = {
        "serviceKey": key,
        "numOfRows": 9999,
        "pageNo": page,
        "zscode": region_code,
        "dataType": "JSON",
    }

    data = requests.get(url, params=queryParams).json()["items"]["item"]

    chargers: Dict[str, ChargerGroup] = {}
    for item in data:
        addr = item["addr"]

        if addr not in chargers.keys():
            chargers[addr] = ChargerGroup(addr)

        chargers[addr].addCharger(Charger(
            item["statNm"],
            addr,
            GeoCoord(item["lat"], item["lng"]),
            item["stat"],
            item["chgerType"],
            item["parkingFree"],
            item["limitYn"],
            item["limitDetail"],
            item["note"],
            item["output"],
            item["method"],
        ))

    return list(chargers.values())


def distance2_between(coord1: GeoCoord, coord2: GeoCoord) -> float:
    return (coord1.lat - coord2.lat) ** 2 + (coord1.lng - coord2.lng) ** 2


def furthest_marker(markers: List[GeoCoord], center: GeoCoord) -> tuple[int, GeoCoord]:
    far = markers[0]
    index = 0
    max_distance = distance2_between(far, center)
    for i, marker in enumerate(markers):
        distance = distance2_between(marker, center)
        if distance > max_distance:
            far = marker
            index = i
            max_distance = distance

    return index, far


def grouped_markers(markers: List[GeoCoord], zoom: int) -> List[GeoCoord]:
    if not markers:
        return []
    
    radius = (0.055 * (2 ** (13 - zoom))) / 20
    radius2 = radius ** 2

    groups = []
    pivot = markers[0]
    while markers:
        idx, pivot = furthest_marker(markers, pivot)        # 아무 점이나 잡은 다음, 그 점에서 가장 먼 점을 찾는다.
        cnt = 1
        markers.pop(idx)
        avg_lat = pivot.lat
        avg_lng = pivot.lng

        for i, marker in enumerate(markers):
            if distance2_between(marker, pivot) < radius2:
                markers.pop(i)
                cnt += 1
                avg_lat += marker.lat
                avg_lng += marker.lng

        groups.append(GeoCoord(avg_lat / cnt, avg_lng / cnt))

    return groups


def only_in_map(coords: List[GeoCoord], center: GeoCoord, zoom: int) -> List[GeoCoord]:
    limit = 0.055 * (2 ** (13 - zoom))
    return [*filter(lambda coord: abs(coord.lat - center.lat) < limit and abs(coord.lng - center.lng) < limit, coords)]


def zoom_path(path: List[GeoCoord], zoom: int) -> List[GeoCoord]:
    if not path:
        return []

    distance = (0.055 * (2 ** (13 - zoom))) / 20
    distance2 = distance ** 2

    zoomed_path = [path[0]]
    pivot = path[0]
    for i, coord in enumerate(path):
        if distance2_between(coord, pivot) > distance2:
            pivot = coord
            zoomed_path.append(coord)
    zoomed_path.append(path[-1])

    return zoomed_path


def get_googlemap(key, center: GeoCoord, size: str, zoom=13, markers: List[GeoCoord]=[], path: List[GeoCoord]=[]):
    map_url = "https://maps.googleapis.com/maps/api/staticmap"
    map_url += "?key=" + key
    map_url += f"&center={center.lat},{center.lng}"
    map_url += "&zoom=" + str(zoom)
    map_url += "&size=1440x1440"
    map_url += "&maptype=roadmap"

    if markers:
        markers = only_in_map(markers, center, zoom)
        markers = grouped_markers(markers, zoom)
        
        map_url += "&markers=color:red"
        if path:
            map_url += f"|{path[-1].lat},{path[-1].lng}"
            map_url += "&markers=color:blue"
            map_url += f"|{path[0].lat},{path[0].lng}"
            map_url += "&markers=color:gray|size:small"

        for marker in markers:
            if marker.lat and marker.lng:
                map_url += f"|{marker.lat},{marker.lng}"

    if path:        
        path = only_in_map(path, center, zoom)      # 구불구불한 경로의 경우 이상해질수 있으니 하지 않는게 좋겠지만 일단 이대로
        path = zoom_path(path, zoom)

        map_url += "&path=color:blue|weight:5"

        for p in path:
            if p.lat and p.lng:
                map_url += f"|{p.lat},{p.lng}"

    response = requests.get(map_url)
    dataBytesIO = io.BytesIO(response.content)
    dataBytesIO.seek(0)
    image = Image.open(dataBytesIO).resize(map(int, size.split('x')))

    return image


def get_path(key, origin, destination):
    headers = {
        "X-NCP-APIGW-API-KEY-ID": key["client_id"],
        "X-NCP-APIGW-API-KEY": key["client_secret"],
    }

    url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    url += "?query=" + origin
    data = requests.get(url, headers=headers).json()
    origin = GeoCoord(data["addresses"][0]["y"], data["addresses"][0]["x"])

    url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    url += "?query=" + destination
    data = requests.get(url, headers=headers).json()
    destination = GeoCoord(data["addresses"][0]["y"], data["addresses"][0]["x"])

    url = "https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving"
    url += "?start={},{}".format(origin.lng, origin.lat)
    url += "&goal={},{}".format(destination.lng, destination.lat)   # 구글이랑은 lat, lng 받는 순서가 다르다
    url += "&option=trafast"    # 빠른길

    data = requests.get(url, headers=headers).json()

    try:
        path = data["route"]["trafast"][0]["path"]
        path = [GeoCoord(p[1], p[0]) for p in path]
    except:
        path = [origin, destination]
    
    return path
