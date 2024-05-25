import xmltodict
import requests


def get_location():
    url = "http://ip-api.com/json"
    response = requests.get(url)
    return response.json()

def get_region_code(key, addr: str):
    url = "http://apis.data.go.kr/1741000/StanReginCd/getStanReginCdList"
    url += "?serviceKey=" + key
    url += "&type=json"
    url += "&locatadd_nm=" + addr

    return requests.get(url).json()["StanReginCd"][1]["row"][0]["region_cd"][:5]

def get_chargers_in_region(key, region_code):
    url = "http://apis.data.go.kr/B552584/EvCharger/getChargerInfo"
    queryParams = {
        "serviceKey": key,
        "numOfRows": 10,
        "pageNo": 1,
        "zscode": region_code,
    }

    response = requests.get(url, params=queryParams)
    data = xmltodict.parse(response.content)["response"]["body"]["items"]["item"]

    chargers = []
    for item in data:
        charger = {
            "name": item["statNm"],
            "address": item["addr"],
            "lat": item["lat"],  # 위도
            "lng": item["lng"],  # 경도
            "doctors": item["chgerType"],
        }
        chargers.append(charger)

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