import requests
import xml.etree.ElementTree as ET
import tkinter


def make_url():
    pass

def get_data():
    url = 'http://openapi.kepco.co.kr/service/EvInfoServiceV2'
    service_key_encoding = "AAwo2DlYdyt1drOL9r%2BRcp2s6ROwcIQ2iYJs%2FbGgKLYS25uMWxpubIWzUj89JO1DwytB%2FirDqJkK0JvE4YQ5hw%3D%3D"
    service_key_decoding = "AAwo2DlYdyt1drOL9r+Rcp2s6ROwcIQ2iYJs/bGgKLYS25uMWxpubIWzUj89JO1DwytB/irDqJkK0JvE4YQ5hw=="
    queryParams = {'serviceKey': service_key_encoding}

    response = requests.get(url, params=queryParams)
    print(response.text)


get_data()