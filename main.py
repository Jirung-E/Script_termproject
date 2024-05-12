import json
import requests
import tkinter


def get_location():
    url = "http://ip-api.com/json"
    response = requests.get(url)
    return response.json()


def get_data(key, addr):    
    url = "https://api.odcloud.kr/api/EvInfoServiceV2/v1/getEvSearchList"
    queryParams = {
        "serviceKey": key,
        "cond[addr::LIKE]": addr,
    }

    return requests.get(url, params=queryParams).json()

def get_ro(key, dong):
    url = 'http://openapi.epost.go.kr/postal/retrieveNewAdressAreaCdService/retrieveNewAdressAreaCdService/getNewAddressListAreaCd'
    params ={'serviceKey' : key, 'searchSe' : 'dong', 'srchwrd' : dong, 'countPerPage' : '10', 'currentPage' : '1' }

    response = requests.get(url, params=params)
    return response.content.decode('utf-8')


if __name__ == "__main__":
    with open('service_key.json', 'r') as f:
        service_key = json.load(f)

    addr = get_ro(service_key["decoding"], "홍문동 111-15")
    data = get_data(service_key["decoding"], addr)

    print(addr)
    print(data)

    print(get_location())