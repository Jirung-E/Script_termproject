import json
import requests
from tkinter import *


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
    params ={'serviceKey' : key, 'searchSe' : 'dong', 'srchwrd' : dong, 'countPerPage' : '10', 'currentPage' : '1'}

    response = requests.get(url, params=params)
    return response.content.decode('utf-8')


class GUI:
    def __init__(self):
        self.window = Tk()
        self.window.title("전기차 충전소 검색")
        
        button_font = ("맑은 고딕", 24)

        interaction_frame = Frame(self.window)
        interaction_frame.pack(side=LEFT, fill=BOTH, expand=True)
        
        map_frame = Frame(self.window, padx=10, pady=10)
        map_frame.pack(side=LEFT, fill=BOTH, expand=True)

        button_frame = Frame(interaction_frame, width=400, height=100, padx=10, pady=10)
        button_frame.pack(side=TOP)

        self.search_button = Button(button_frame, text="검색", font=button_font, command=self.search)
        self.search_button.place(width=90, height=90)

        self.favorites_button = Button(button_frame, text="즐겨\n찾기", font=button_font, command=self.search)
        self.favorites_button.place(x=100, width=90, height=90)

        self.recent_button = Button(button_frame, text="최근\n기록", font=button_font, command=self.search)
        self.recent_button.place(x=200, width=90, height=90)

        self.share_button = Button(button_frame, text="공유", font=button_font, command=self.search)
        self.share_button.place(x=300, width=90, height=90)

        self.map = Canvas(map_frame, width=660, height=660, bg="white")
        self.map.pack()

        self.window.mainloop()

    def search(self):
        pass


if __name__ == "__main__":
    with open('service_key.json', 'r') as f:
        service_key = json.load(f)

    GUI()

    # addr = get_ro(service_key["decoding"], "홍문동 111-15")
    # data = get_data(service_key["decoding"], "시흥시")

    # print(addr)
    # print(data)

    # print(get_location())