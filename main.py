import json
from tkinter import *
from tkinter.ttk import Progressbar, Combobox, Notebook
from typing import List
from PIL import ImageTk
from io import BytesIO

from apis import *
from charger import *
from placeholder import *
from gmail import *






button_font = ("맑은 고딕", 24)
default_font = ("맑은 고딕", 20)
info_font = ("맑은 고딕", 16)
combobox_font = ("맑은 고딕", 18)

favorites_list = []
recent_list = []

region_code = {}













class SearchWidgets:
    def __init__(self, master, frame):
        self.master = master
        self.frame = frame

        self.star_empty_img = PhotoImage(file="img/star_empty.png")
        self.star_filled_img = PhotoImage(file="img/star_filled.png")
        
        self.master.window.option_add('*TCombobox*Listbox.font', combobox_font)

        self.dosi_combobox = Combobox(self.frame, font=combobox_font)
        self.dosi_combobox['values'] = list(region_code.keys())
        self.dosi_combobox.bind("<<ComboboxSelected>>", self.select_dosi)

        self.sigungu_combobox = Combobox(self.frame, font=combobox_font)
        self.sigungu_combobox['values'] = None
        self.sigungu_combobox.bind("<<ComboboxSelected>>", self.select_sigungu)
        
        self.search_input = PlaceholderEntry(self.frame, 
                                             placeholder="상세주소", 
                                             font=default_font)
        self.search_input.bind("<KeyPress>", self.press_enter)
        self.search_input.bind("<KeyRelease>", self.update_favorites)
        
        self.search_icon = PhotoImage(file="img/search_icon.png")
        self.search_button = Button(self.frame, 
                                    image=self.search_icon,
                                    command=lambda: self.search(self.make_address()))
        
        self.add_to_favorites_button = Button(self.frame, 
                                              image=self.star_empty_img,
                                              font=default_font, 
                                              command=self.add_to_favorites)

        
        self.result_listbox = Listbox(self.frame, font=info_font)
        self.result_listbox.bind("<Double-Button-1>", self.select_charger)

        self.widgets: List[Widget] = [
            self.dosi_combobox,
            self.sigungu_combobox,
            self.search_input, 
            self.search_button, 
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
        self.dosi_combobox.place(x=10, y=110, width=190, height=50)
        self.sigungu_combobox.place(x=210, y=110, width=190, height=50)
        self.search_input.place(x=10, y=170, width=270, height=50)
        self.search_button.place(x=290, y=170, width=50, height=50)
        self.add_to_favorites_button.place(x=350, y=170, width=50, height=50)
        self.result_listbox.place(x=10, y=230, width=390, height=200)
        self.dosi_combobox['state'] = 'readonly'
        self.sigungu_combobox['state'] = 'readonly'

    def select_dosi(self, event):
        dosi = self.dosi_combobox.get()
        self.sigungu_combobox['values'] = list(region_code[dosi]["sigungu"].keys())
        self.sigungu_combobox.current(0)
        self.update_favorites(None)

    def select_sigungu(self, event):
        dosi = self.dosi_combobox.get()
        sigungu = self.sigungu_combobox.get()
        self.region_code = region_code[dosi]["sigungu"][sigungu]
        self.update_favorites(None)

    def make_address(self):
        s = ""
        s += self.dosi_combobox.get() + " "
        s += self.sigungu_combobox.get() + " "

        addr = self.search_input.get()
        if addr != "상세주소" and addr != "":
            s += addr
        return s

    def search(self, addr: str):
        self.result_listbox.delete(0, END)

        addr = addr.strip()
        if addr == "":
            return
        
        code = None
        address = addr.split(" ")
        while code is None and len(address) > 0:
            code = get_region_code(service_key["encoding"], str(' '.join(address)))
            address.pop()

        if code is not None:
            self.chargers: List[ChargerGroup] = get_chargers_in_region(service_key["decoding"], code)

            if addr in recent_list:
                recent_list.remove(addr)
            recent_list.insert(0, addr)

            gmaps = Client(key=service_key["google"])
            center = gmaps.geocode(addr)[0]['geometry']['location']
            center = GeoCoord(center['lat'], center['lng'])
            self.chargers.sort(key=lambda x: distance2_between(x.getAverageCoord(), center))
            for chargers in self.chargers:
                self.result_listbox.insert(END, chargers.getNames())
        
        charger_coords = [chargers.getAverageCoord() for chargers in self.chargers]
        self.master.info_widgets.set_graph(self.chargers)
        self.master.update_map(addr, charger_coords)

    def update_favorites(self, event):
        addr = self.make_address().strip()
        
        if addr in favorites_list:
            self.add_to_favorites_button.configure(image=self.star_filled_img)
        else:
            self.add_to_favorites_button.configure(image=self.star_empty_img)

    def press_enter(self, event):
        if event.keysym == "Return":
            self.search(self.make_address())

    def add_to_favorites(self):
        addr = self.make_address().strip()

        if addr not in favorites_list:
            favorites_list.append(addr)
            self.add_to_favorites_button.configure(image=self.star_filled_img)
        else:
            favorites_list.remove(addr)
            self.add_to_favorites_button.configure(image=self.star_empty_img)

    def select_charger(self, event):
        selected_charger_group: ChargerGroup = self.chargers[self.result_listbox.curselection()[0]]

        charger_coords = [chargers.getAverageCoord() for chargers in self.chargers]
        self.master.update_map(
            selected_charger_group.addr, 
            charger_coords,
            self.make_address().strip(),
            selected_charger_group.addr
        )
        
        self.master.info_widgets.details_listbox.delete(0, END)

        self.master.info_widgets.details_listbox.insert(END, 
            selected_charger_group.addr)

        for charger in selected_charger_group.chargers:
            self.master.info_widgets.details_listbox.insert(END, "- - - - - - - - - - - -")

            self.master.info_widgets.details_listbox.insert(END, 
                "상태: " + charger.getState())
            self.master.info_widgets.details_listbox.insert(END, 
                "충전기 타입: " + charger.getType())
            self.master.info_widgets.details_listbox.insert(END, 
                "출력: " + charger.getOutput())
            self.master.info_widgets.details_listbox.insert(END, 
                "충전방식: " + charger.method)
            self.master.info_widgets.details_listbox.insert(END, 
                "주차: " + charger.getParking())
            
            limit = charger.getLimit()
            self.master.info_widgets.details_listbox.insert(END, 
                "제한사항: " + (limit if limit != "무제한" else "없음"))
            
            if charger.note != "":
                self.master.info_widgets.details_listbox.insert(END, 
                "비고: " + charger.note)
        















class FavoritesWidgets:
    def __init__(self, master, frame):
        self.master = master
        self.frame = frame

        self.listbox = Listbox(self.frame, font=default_font)
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
        self.master.search_widgets.search_input.delete(0, END)
        self.master.search_widgets.search_input.foc_in(None)
        self.master.search_widgets.search_input.insert(0, self.listbox.get(self.listbox.curselection()))
        self.master.search_widgets.update_favorites(None)
        self.master.search_widgets.search(self.listbox.get(self.listbox.curselection()))
        self.master.search_widgets.dosi_combobox.set('')
        self.master.search_widgets.sigungu_combobox.set('')


















class RecentWidgets:
    def __init__(self, master, frame):
        self.master = master
        self.frame = frame

        self.listbox = Listbox(self.frame, font=default_font)
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
        self.master.search_widgets.search_input.delete(0, END)
        self.master.search_widgets.search_input.foc_in(None)
        self.master.search_widgets.search_input.insert(0, self.listbox.get(self.listbox.curselection()))
        self.master.search_widgets.update_favorites(None)
        self.master.search_widgets.search(self.listbox.get(self.listbox.curselection()))
        self.master.search_widgets.dosi_combobox.set('')
        self.master.search_widgets.sigungu_combobox.set('')

















class InfoWidgets:
    def __init__(self, master, frame):
        self.master = master
        self.frame = frame

        self.details_listbox = Listbox(self.frame, font=info_font)

        self.available_label =  Label(
                                    self.frame, 
                                    text="사용가능", 
                                    font=default_font
                                )
        self.available_progress = Progressbar(
                                    self.frame, 
                                    orient=HORIZONTAL, 
                                    length=180, 
                                    mode='determinate', 
                                    maximum=0, 
                                    value=0
                                )
        self.available_count_label = Label(
                                    self.frame, 
                                    text="0개", 
                                    font=default_font
                                )

        self.occupied_label =   Label(
                                    self.frame, 
                                    text="사용중", 
                                    font=default_font
                                )
        self.occupied_progress = Progressbar(
                                    self.frame, 
                                    orient=HORIZONTAL, 
                                    length=180, 
                                    mode='determinate', 
                                    maximum=0, 
                                    value=0
                                )
        self.occupied_count_label = Label(
                                    self.frame, 
                                    text="0개", 
                                    font=default_font
                                )

        self.disabled_label =   Label(
                                    self.frame, 
                                    text="사용불가", 
                                    font=default_font
                                )
        self.disabled_progress = Progressbar(
                                    self.frame, 
                                    orient=HORIZONTAL, 
                                    length=180, 
                                    mode='determinate', 
                                    maximum=0, 
                                    value=0
                                )
        self.disabled_count_label = Label(
                                    self.frame, 
                                    text="0개", 
                                    font=default_font
                                )

        self.widgets: List[Widget] = [
            self.details_listbox,
            self.available_label, 
            self.available_progress, 
            self.available_count_label,
            self.occupied_label, 
            self.occupied_progress, 
            self.occupied_count_label,
            self.disabled_label, 
            self.disabled_progress, 
            self.disabled_count_label,
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

    def place(self):
        self.details_listbox.place(x=10, y=10, width=390, height=300)
        self.available_label.place(x=10, y=320)
        self.available_progress.place(x=130, y=325, height=40)
        self.available_count_label.place(x=320, y=320)
        self.occupied_label.place(x=10, y=370)
        self.occupied_progress.place(x=130, y=375, height=40)
        self.occupied_count_label.place(x=320, y=370)
        self.disabled_label.place(x=10, y=420)
        self.disabled_progress.place(x=130, y=425, height=40)
        self.disabled_count_label.place(x=320, y=420)

    def set_graph(self, chargers: List[ChargerGroup]):
        available = 0
        occupied = 0
        total = 0

        for charger in chargers:
            available += charger.available
            occupied += charger.occupied
            total += len(charger.chargers)

        disabled = total - available - occupied

        self.available_progress.configure(value=available, maximum=total)
        self.available_count_label.configure(text=f"{available}개")
        self.occupied_progress.configure(value=occupied, maximum=total)
        self.occupied_count_label.configure(text=f"{occupied}개")
        self.disabled_progress.configure(value=disabled, maximum=total)
        self.disabled_count_label.configure(text=f"{disabled}개")













class MapWidgets:
    def __init__(self, master, frame):
        self.master = master
        self.frame = frame

        self.zoom = 13
        self.size = "900x900"
        self.address = "서울특별시 중구 을지로2가"
        self.markers = []
        self.path = []

        # self.map = Canvas(self.frame, width=900, height=900, bg="white")        # 테스트시 api호출 막기 위해 캔버스로 대체
        
        gmaps = Client(key=service_key["google"])
        center = gmaps.geocode(self.address)[0]['geometry']['location']
        center = GeoCoord(center['lat'], center['lng'])

        self.map_img = get_googlemap(service_key["google"], center, self.size)
        self.map_tkimg = ImageTk.PhotoImage(self.map_img)
        self.map = Label(self.frame, image=self.map_tkimg)

        self.zoom_in_button = Button(self.frame, text="+", font=("Consolas", 40), command=self.zoom_in)
        self.zoom_out_button = Button(self.frame, text="-", font=("Consolas", 48), command=self.zoom_out)

    def update_map(self, addr, markers=[], origin=None, destination=None):
        self.address = addr
        self.markers = markers
        if origin is not None and destination is not None:
            try:
                self.path = get_path(service_key["naver"], origin, destination)
            except:
                self.path = []
                print("경로를 찾을 수 없습니다.")
        else:
            self.path = []
        self.show_map()

    def show_map(self):
        if self.path:
            x_distance = abs(self.path[0].lat - self.path[-1].lat) / 2
            y_distance = abs(self.path[0].lng - self.path[-1].lng) / 2
            distance = x_distance if x_distance > y_distance else y_distance
            while distance > 0.055 * (2 ** (13 - self.zoom)):
                self.zoom -= 1

            center = GeoCoord((self.path[0].lat + self.path[-1].lat) / 2, (self.path[0].lng + self.path[-1].lng) / 2)
        else:
            gmaps = Client(key=service_key["google"])
            center = gmaps.geocode(self.address)[0]['geometry']['location']
            center = GeoCoord(center['lat'], center['lng'])
            
        self.map_img = get_googlemap(service_key["google"], center, self.size, self.zoom, self.markers, self.path)
        self.map_tkimg = ImageTk.PhotoImage(self.map_img)
        self.map.configure(image=self.map_tkimg)

    def place(self):
        self.map.pack()
        self.zoom_in_button.place(x=900-60, y=900-60, width=50, height=50)
        self.zoom_out_button.place(x=900-60-60, y=900-60, width=50, height=50)

    def zoom_in(self):
        self.zoom += 1
        if self.zoom > 18:
            self.zoom = 18
        self.show_map()

    def zoom_out(self):
        self.zoom -= 1
        if self.zoom < 7:
            self.zoom = 7
        self.show_map()













class ShareWindow:
    def __init__(self, master):
        self.master = master
        
        self.share_window = Toplevel(self.master.window)
        self.share_window.resizable(0, 0)
        self.share_window.geometry("600x450")
        self.share_window.title('공유')
        self.share_window.attributes('-topmost', 'true')
        self.share_window.grab_set()
        self.share_window.focus_set()

        bold_font = ("맑은 고딕", 24, "bold")

        self.email_frame = Frame(self.share_window, width=600, height=450)
        self.email_frame.pack()

        Label(self.email_frame, text="From:", font=bold_font
              ).place(x=10, y=10, height=50)

        y = 70
        Label(self.email_frame, text="email", font=default_font
              ).place(x=10, y=y, height=50)
        self.from_mail_address = StringVar()
        Entry(self.email_frame, font=default_font, width=30, 
              textvariable=self.from_mail_address
              ).place(x=140, y=y, width=200, height=50)
        Label(self.email_frame, text="@", font=default_font
              ).place(x=340, y=y, width=30, height=50)
        self.from_mails = ["gmail.com", "tukorea.ac.kr"]
        self.from_mail_address_combobox = Combobox(
            self.email_frame, values=self.from_mails,
            font=default_font, width=30, state="readonly"
        )
        self.from_mail_address_combobox.place(x=370, y=y, width=200, height=50)
        
        y += 60
        Label(self.email_frame, text="password", font=default_font
              ).place(x=10, y=y, height=50)
        self.from_mail_password = StringVar()
        Entry(self.email_frame, font=default_font, width=30, 
              textvariable=self.from_mail_password, show="*"
              ).place(x=140, y=y, width=200, height=50)
        caution_font = ("맑은 고딕", 12)
        Label(self.email_frame, text="구글 앱 비밀번호를 입력하세요", 
              fg="gray", font=caution_font
              ).place(x=340, y=y, width=250, height=50)
        
        y += 90
        Label(self.email_frame, text="To:", font=bold_font
              ).place(x=10, y=y, height=50)
        
        y += 60
        Label(self.email_frame, text="email", font=default_font
              ).place(x=10, y=y, height=50)
        self.to_mail_address_1 = StringVar()
        Entry(self.email_frame, font=default_font, width=30, 
              textvariable=self.to_mail_address_1
              ).place(x=140, y=y, width=200, height=50)
        Label(self.email_frame, text="@", font=default_font
              ).place(x=340, y=y, width=30, height=50)
        self.to_mail_address_2 = StringVar()
        Entry(self.email_frame, font=default_font, width=30,
              textvariable=self.to_mail_address_2
              ).place(x=370, y=y, width=200, height=50)

        y += 90
        Button(self.email_frame, text="전송", font=default_font,
               command=lambda: self.send_email()
               ).place(x=480, y=y, width=90, height=50)
    
    def send_email(self):
        from_addr = self.from_mail_address.get() + "@" + self.from_mail_address_combobox.get()
        passwd = self.from_mail_password.get()
        to_addr = self.to_mail_address_1.get() + "@" + self.to_mail_address_2.get()
        title = "전기차 충전소 정보"
        msgtext = "<h4>" + self.master.map_widgets.address + "</h4>"
        msgtext += "\n\n"
        for charger in self.master.search_widgets.chargers:
            msgtext += "<p>" + charger.name + "(" +charger.addr + ") </p>\n"
        msgtext += "\n"
        msgtext += "<img src='cid:image1'>"
        img = self.master.map_widgets.map_img
        byte_buffer = BytesIO()
        img.save(byte_buffer, "PNG")
        sendMain(from_addr, passwd, to_addr, title, msgtext, byte_buffer.getvalue())

        self.share_window.destroy()
















class ButtonWidgets:
    def __init__(self, master, frame):
        self.master = master
        self.frame = frame

        self.search_button = Button(self.frame, text="검색", 
                                    font=button_font, 
                                    command=self.master.switch_to_search_mode)
        self.favorites_button = Button(self.frame, text="즐겨\n찾기", 
                                       font=button_font, 
                                       command=self.master.switch_to_favorites_mode)
        self.recent_button = Button(self.frame, text="최근\n기록", 
                                    font=button_font, 
                                    command=self.master.switch_to_recent_mode)
        self.share_button = Button(self.frame, text="공유", 
                                   font=button_font, 
                                   command=self.master.share)

    def place(self):
        self.search_button.place(width=90, height=90)
        self.favorites_button.place(x=100, width=90, height=90)
        self.recent_button.place(x=200, width=90, height=90)
        self.share_button.place(x=300, width=90, height=90)
















class GUI:
    def __init__(self):
        self.window = Tk()
        self.window.title("전기차 충전소 검색")

        notebook = Notebook(self.window)
        notebook.pack()

        self.main_page = Frame(self.window)
        self.charger_info_page = Frame(self.window)
        notebook.add(self.main_page, text="메인")
        notebook.add(self.charger_info_page, text="충전기 정보")

        # -- INTERACTION FRAMES --
        self.interaction_frame = Frame(self.main_page)
        self.interaction_frame.pack(side=LEFT, fill=BOTH, expand=True)

        button_frame = Frame(self.interaction_frame, 
                             width=400, height=100, padx=10, pady=10)
        button_frame.pack(side=TOP)

        self.info_frame = Frame(self.interaction_frame, width=400, height=480)
        self.info_frame.pack(side=BOTTOM)

        # -- INTERACTION WIDGETS --
        self.button_widgets = ButtonWidgets(self, button_frame)
        self.button_widgets.place()

        self.search_widgets = SearchWidgets(self, self.interaction_frame)
        self.favorites_widgets = FavoritesWidgets(self, self.interaction_frame)
        self.recent_widgets = RecentWidgets(self, self.interaction_frame)
        self.search_widgets.place()

        self.info_widgets = InfoWidgets(self, self.info_frame)
        self.info_widgets.place()
        
        # -- MAP WIDGETS --
        self.map_frame = Frame(self.main_page, padx=10, pady=10)
        self.map_frame.pack(side=LEFT, fill=BOTH, expand=True)
        
        self.map_widgets = MapWidgets(self, self.map_frame)
        self.map_widgets.place()


        # -- CHARGER INFO WIDGETS --
        self.charger_info_img = PhotoImage(file="img/charger_types.png")
        self.charger_info_widgets = Label(self.charger_info_page, image=self.charger_info_img)
        self.charger_info_widgets.pack()


        self.window.mainloop()


    def update_map(self, addr, markers=[], origin=None, destination=None):
        self.map_widgets.update_map(addr, markers, origin, destination)

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
        ShareWindow(self)



















if __name__ == "__main__":
    with open('service_key.json', 'r') as f:
        service_key = json.load(f)

    with open("recent.txt", "r", encoding="utf-8") as f:
        recent_list = [s for s in f.read().split("\n") if s != ""]

    with open("favorites.txt", "r", encoding="utf-8") as f:
        favorites_list = [s for s in f.read().split("\n") if s != ""]

    with open("region_code.json", "r", encoding="utf-8") as f:
        region_code = json.load(f)

    GUI()

    with open("recent.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(recent_list))
    
    with open("favorites.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(favorites_list))