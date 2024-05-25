import requests
import io
from PIL import Image, ImageTk
from googlemaps import Client
from typing import List

from charger_config import *


def get_location():
    url = "http://ip-api.com/json"
    response = requests.get(url)
    return response.json()

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

def get_chargers_in_region(key, region_code):
    url = "http://apis.data.go.kr/B552584/EvCharger/getChargerInfo"
    queryParams = {
        "serviceKey": key,
        "numOfRows": 100,
        "pageNo": 1,
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
        ))

    return chargers

def get_data(key, addr):
    url = "https://api.odcloud.kr/api/EvInfoServiceV2/v1/getEvSearchList"
    queryParams = {
        "serviceKey": key,
        "cond[addr::LIKE]": addr,
    }

    return requests.get(url, params=queryParams).json()

def get_ro(key, dong):
    url = 'http://openapi.epost.go.kr/postal/retrieveNewAdressAreaCdService/retrieveNewAdressAreaCdService/getNewAddressListAreaCd'
    params = {'serviceKey' : key, 'searchSe' : 'dong', 'srchwrd' : dong, 'countPerPage' : '10', 'currentPage' : '1'}

    response = requests.get(url, params=params)
    return response.content.decode('utf-8')

def get_googlemap(key, addr, size: str, markers: List[GeoCoord]=[], zoom=13):
    gmaps = Client(key=key)
    center = gmaps.geocode(addr)[0]['geometry']['location']

    map_url = "https://maps.googleapis.com/maps/api/staticmap"
    map_url += "?key=" + key
    map_url += f"&center={center['lat']},{center['lng']}"
    map_url += "&zoom=" + str(zoom)
    map_url += "&size=1440x1440"
    map_url += "&maptype=roadmap"

    for marker in markers:
        if marker.lat and marker.lng:
            map_url += f"&markers=color:red%7C{marker.lat},{marker.lng}"

    response = requests.get(map_url)
    image = Image.open(io.BytesIO(response.content)).resize(map(int, size.split('x')))
    photo = ImageTk.PhotoImage(image)

    return photo
