import json
import requests
import tkinter


def get_data():
    with open('service_key.json', 'r') as f:
        service_key = json.load(f)
    
    url = "https://api.odcloud.kr/api/EvInfoServiceV2/v1/getEvSearchList"
    queryParams = {
        "serviceKey": service_key["decoding"],
        "cond[addr::LIKE]": "서울특별시",
    }

    return requests.get(url, params=queryParams).json()


data = get_data()

print(data)

