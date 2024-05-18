import json
import requests
from tkinter import *
from tkinter.ttk import Progressbar

from placeholder import *


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
        default_font = ("맑은 고딕", 20)

        interaction_frame = Frame(self.window)
        interaction_frame.pack(side=LEFT, fill=BOTH, expand=True)

        map_frame = Frame(self.window, padx=10, pady=10)
        map_frame.pack(side=LEFT, fill=BOTH, expand=True)

        button_frame = Frame(interaction_frame, width=400, height=100, padx=10, pady=10)
        button_frame.pack(side=TOP)

        self.search_button = Button(button_frame, text="검색", font=button_font, command=self.switch_to_search_mode)
        self.search_button.place(width=90, height=90)

        self.favorites_button = Button(button_frame, text="즐겨\n찾기", font=button_font, command=self.switch_to_favorites_mode)
        self.favorites_button.place(x=100, width=90, height=90)

        self.recent_button = Button(button_frame, text="최근\n기록", font=button_font, command=self.switch_to_recent_mode)
        self.recent_button.place(x=200, width=90, height=90)

        self.share_button = Button(button_frame, text="공유", font=button_font, command=self.share)
        self.share_button.place(x=300, width=90, height=90)

        self.search_input = PlaceholderText(interaction_frame, placeholder="주소를 입력하세요", font=default_font)
        self.search_input.place(x=10, y=110, width=390, height=90)

        self.add_to_favorites_button = Button(interaction_frame, text="즐겨찾기에 추가", font=default_font, command=self.search)
        self.add_to_favorites_button.place(x=10, y=210, width=390, height=50)

        info_frame = Frame(interaction_frame, width=400, height=330)
        info_frame.pack(side=BOTTOM)

        self.available_label = Label(info_frame, text="사용가능", font=default_font)
        self.available_label.place(x=10, y=170)
        self.progress = Progressbar(info_frame, orient=HORIZONTAL, length=180, mode='determinate', maximum=100, value=10)
        self.progress.place(x=130, y=175, height=40)
        self.available_count_label = Label(info_frame, text="123개", font=default_font)
        self.available_count_label.place(x=320, y=170)

        self.occupied_label = Label(info_frame, text="사용중", font=default_font)
        self.occupied_label.place(x=10, y=220)
        self.progress = Progressbar(info_frame, orient=HORIZONTAL, length=180, mode='determinate', maximum=100, value=10)
        self.progress.place(x=130, y=225, height=40)
        self.occupied_count_label = Label(info_frame, text="70개", font=default_font)
        self.occupied_count_label.place(x=320, y=220)

        self.disabled_label = Label(info_frame, text="사용불가", font=default_font)
        self.disabled_label.place(x=10, y=270)
        self.progress = Progressbar(info_frame, orient=HORIZONTAL, length=180, mode='determinate', maximum=100, value=10)
        self.progress.place(x=130, y=275, height=40)
        self.disabled_count_label = Label(info_frame, text="2개", font=default_font)
        self.disabled_count_label.place(x=320, y=270)

        self.map = Canvas(map_frame, width=660, height=660, bg="white")
        self.map.pack()

        self.window.mainloop()

    def switch_to_search_mode(self):
        pass

    def switch_to_favorites_mode(self):
        pass

    def switch_to_recent_mode(self):
        pass

    def share(self):
        pass

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