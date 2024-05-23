import json
import xmltodict
import requests
from tkinter import *
from tkinter.ttk import Progressbar
from typing import List

from placeholder import *


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
 
    # queryParams = {
    #     "serviceKey": key,
    #     "type": "json",
    #     "locatadd_nm": addr,
    # }

    # req = requests.get(url, params=queryParams)

    # print(req.url)
    # print(url)

    # return requests.get(url, params=queryParams).json()

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


button_font = ("맑은 고딕", 24)
default_font = ("맑은 고딕", 20)

favorites_list = set()
recent_list = []


class SearchWidgets:
    def __init__(self, master):
        self.master = master

        self.star_empty_img = PhotoImage(file="img/star_empty.png")
        self.star_filled_img = PhotoImage(file="img/star_filled.png")

        self.search_input = PlaceholderEntry(master.interaction_frame, 
                                            placeholder="주소를 입력하세요", 
                                            font=default_font)
        self.search_input.bind("<KeyPress>", self.press_enter)
        self.search_input.bind("<KeyRelease>", self.update_favorites)
        self.search_location_button = Button(master.interaction_frame, text="검색", 
                                             font=default_font, 
                                             command=lambda: self.search(self.search_input.get()))
        self.add_to_favorites_button = Button(master.interaction_frame, 
                                              image=self.star_empty_img,
                                              font=default_font, 
                                              command=self.add_to_favorites)
        
        self.result_listbox = Listbox(master.interaction_frame, font=default_font)
        self.result_listbox.bind("<Double-Button-1>", self.select)

        self.widgets: List[Widget] = [
            self.search_input, 
            self.search_location_button, 
            self.add_to_favorites_button,
            self.result_listbox
        ]

    def enable(self, enable):
        if enable:
            for widget in self.widgets:
                widget.configure(state=NORMAL)
                self.place()
        else:
            for widget in self.widgets:
                widget.configure(state=DISABLED)
                widget.place_forget()
            self.search_input.delete(0, END)
            
    def place(self):
        self.search_input.place(x=10, y=110, width=390, height=50)
        self.search_location_button.place(x=10, y=170, width=330, height=50)
        self.add_to_favorites_button.place(x=350, y=170, width=50, height=50)
        self.result_listbox.place(x=10, y=230, width=390, height=200)

    def search(self, addr):
        self.data = get_data(service_key["decoding"], addr)['data']

        if addr in recent_list:
            recent_list.remove(addr)
        recent_list.insert(0, addr)

        self.result_listbox.delete(0, END)
        self.result_listbox.insert(END, *self.data)

        print(self.data)

        # TODO: 지도에 출력

    def update_favorites(self, event):
        addr = self.search_input.get()

        if addr == "주소를 입력하세요" or addr == "":
            return
        
        if addr in favorites_list:
            self.add_to_favorites_button.configure(image=self.star_filled_img)
        else:
            self.add_to_favorites_button.configure(image=self.star_empty_img)

    def press_enter(self, event):
        if event.keysym == "Return":
            self.search(self.search_input.get())

    def add_to_favorites(self):
        addr = self.search_input.get()

        if addr not in favorites_list:
            favorites_list.add(addr)
            self.add_to_favorites_button.configure(image=self.star_filled_img)
        else:
            favorites_list.remove(addr)
            self.add_to_favorites_button.configure(image=self.star_empty_img)

    def select(self, event):
        # TODO: 지도에 출력
        pass


class FavoritesWidgets:
    def __init__(self, master):
        self.master = master

        self.listbox = Listbox(master.interaction_frame, font=default_font)
        self.listbox.bind("<Double-Button-1>", self.select)

    def enable(self, enable):
        if enable:
            self.listbox.configure(state=NORMAL)
            self.place()
            self.listbox.delete(0, END)
            self.listbox.insert(END, *favorites_list)
        else:
            self.listbox.configure(state=DISABLED)
            self.listbox.place_forget()

    def place(self):
        self.listbox.place(x=10, y=110, width=390, height=320)

    def select(self, event):
        self.master.switch_to_search_mode()
        self.master.search_widgets.search(self.listbox.get(self.listbox.curselection()))


class RecentWidgets:
    def __init__(self, master):
        self.master = master

        self.listbox = Listbox(master.interaction_frame, font=default_font)
        self.listbox.bind("<Double-Button-1>", self.select)

    def enable(self, enable):
        if enable:
            self.listbox.configure(state=NORMAL)
            self.place()
            self.listbox.delete(0, END)
            self.listbox.insert(END, *recent_list)
        else:
            self.listbox.configure(state=DISABLED)
            self.listbox.place_forget()

    def place(self):
        self.listbox.place(x=10, y=110, width=390, height=320)

    def select(self, event):
        self.master.switch_to_search_mode()
        self.master.search_widgets.search(self.listbox.get(self.listbox.curselection()))


class GUI:
    def __init__(self):
        self.window = Tk()
        self.window.title("전기차 충전소 검색")

        self.interaction_frame = Frame(self.window)
        self.interaction_frame.pack(side=LEFT, fill=BOTH, expand=True)

        map_frame = Frame(self.window, padx=10, pady=10)
        map_frame.pack(side=LEFT, fill=BOTH, expand=True)

        button_frame = Frame(self.interaction_frame, 
                             width=400, height=100, 
                             padx=10, pady=10)
        self.search_button = Button(button_frame, text="검색", 
                                    font=button_font, 
                                    command=self.switch_to_search_mode)
        self.favorites_button = Button(button_frame, text="즐겨\n찾기", 
                                       font=button_font, 
                                       command=self.switch_to_favorites_mode)
        self.recent_button = Button(button_frame, text="최근\n기록", 
                                    font=button_font, 
                                    command=self.switch_to_recent_mode)
        self.share_button = Button(button_frame, text="공유", 
                                   font=button_font, 
                                   command=self.share)
        button_frame.pack(side=TOP)
        self.search_button.place(width=90, height=90)
        self.favorites_button.place(x=100, width=90, height=90)
        self.recent_button.place(x=200, width=90, height=90)
        self.share_button.place(x=300, width=90, height=90)

        self.search_widgets = SearchWidgets(self)
        self.search_widgets.place()
        self.favorites_widgets = FavoritesWidgets(self)
        self.recent_widgets = RecentWidgets(self)

        info_frame = Frame(self.interaction_frame, width=400, height=330)
        info_frame.pack(side=BOTTOM)

        self.available_label = Label(info_frame, text="사용가능", 
                                     font=default_font)
        self.available_label.place(x=10, y=170)
        self.progress = Progressbar(info_frame, orient=HORIZONTAL, 
                                    length=180, mode='determinate', 
                                    maximum=100, value=10)
        self.progress.place(x=130, y=175, height=40)
        self.available_count_label = Label(info_frame, text="123개", 
                                           font=default_font)
        self.available_count_label.place(x=320, y=170)

        self.occupied_label = Label(info_frame, text="사용중", 
                                    font=default_font)
        self.occupied_label.place(x=10, y=220)
        self.progress = Progressbar(info_frame, orient=HORIZONTAL, 
                                    length=180, mode='determinate', 
                                    maximum=100, value=10)
        self.progress.place(x=130, y=225, height=40)
        self.occupied_count_label = Label(info_frame, text="70개", 
                                          font=default_font)
        self.occupied_count_label.place(x=320, y=220)

        self.disabled_label = Label(info_frame, text="사용불가", 
                                    font=default_font)
        self.disabled_label.place(x=10, y=270)
        self.progress = Progressbar(info_frame, orient=HORIZONTAL, 
                                    length=180, mode='determinate', 
                                    maximum=100, value=10)
        self.progress.place(x=130, y=275, height=40)
        self.disabled_count_label = Label(info_frame, text="2개", 
                                          font=default_font)
        self.disabled_count_label.place(x=320, y=270)

        self.map = Canvas(map_frame, width=900, height=900, bg="white")
        self.map.pack()

        self.window.mainloop()

    def switch_to_search_mode(self):
        self.search_widgets.enable(True)
        self.favorites_widgets.enable(False)
        self.recent_widgets.enable(False)

    def switch_to_favorites_mode(self):
        self.search_widgets.enable(False)
        self.favorites_widgets.enable(True)
        self.recent_widgets.enable(False)

    def switch_to_recent_mode(self):
        self.search_widgets.enable(False)
        self.favorites_widgets.enable(False)
        self.recent_widgets.enable(True)

    def share(self):
        pass


if __name__ == "__main__":
    with open('service_key.json', 'r') as f:
        service_key = json.load(f)

    rc = get_region_code(service_key["encoding"], "서울특별시_강남구_역삼동")
    print(rc)
    print(get_chargers_in_region(service_key["decoding"], rc))

    with open("recent.txt", "r", encoding="utf-8") as f:
        recent_list = [s for s in f.read().split("\n") if s != ""]

    with open("favorites.txt", "r", encoding="utf-8") as f:
        favorites_list = set([s for s in f.read().split("\n") if s != ""])

    GUI()

    with open("recent.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(recent_list))
    
    with open("favorites.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(favorites_list))

    # addr = get_ro(service_key["decoding"], "홍문동 111-15")
    # data = get_data(service_key["decoding"], "시흥시")

    # print(addr)
    # print(data) 

    # print(get_location())