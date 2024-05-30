import requests
import io
from PIL import Image
from googlemaps import Client
from typing import List

from charger_config import *


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

def get_chargers_in_region(key, region_code, page=1):
    url = "http://apis.data.go.kr/B552584/EvCharger/getChargerInfo"
    queryParams = {
        "serviceKey": key,
        "numOfRows": 500,
        "pageNo": page,
        "zscode": region_code,
        "dataType": "JSON",
    }

    data = requests.get(url, params=queryParams).json()["items"]["item"]

    chargers = []
    for item in data:
        chargers.append(Charger(
            item["statNm"],
            item["addr"],
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

    return chargers

def get_googlemap(key, addr, size: str, zoom=13, markers: List[GeoCoord]=[], path: List[GeoCoord]=[]):
    gmaps = Client(key=key)
    center = gmaps.geocode(addr)[0]['geometry']['location']
    print(center)

    map_url = "https://maps.googleapis.com/maps/api/staticmap"
    map_url += "?key=" + key
    map_url += f"&center={center['lat']},{center['lng']}"
    map_url += "&zoom=" + str(zoom)
    map_url += "&size=1440x1440"
    map_url += "&maptype=roadmap"
    map_url += "&markers=color:red"
    for marker in markers:
        if marker.lat and marker.lng:
            map_url += f"|{marker.lat},{marker.lng}"
    map_url += "&path=color:0x0000ff80|weight:5"
    for p in path:
        if p.lat and p.lng:
            map_url += f"|{p.lat},{p.lng}"

    response = requests.get(map_url)
    dataBytesIO = io.BytesIO(response.content)
    dataBytesIO.seek(0)
    image = Image.open(dataBytesIO).resize(map(int, size.split('x')))

    return image
