import json
from tkinter import *
from tkinter.ttk import Progressbar, Combobox
from typing import List

from apis import *
from charger_config import *
from placeholder import *


button_font = ("맑은 고딕", 24)
default_font = ("맑은 고딕", 20)
info_font = ("맑은 고딕", 16)
combobox_font = ("맑은 고딕", 18)

favorites_list = []
recent_list = []

region_code = {}


class SearchWidgets:
    def __init__(self, master):
        self.master = master

        self.star_empty_img = PhotoImage(file="img/star_empty.png")
        self.star_filled_img = PhotoImage(file="img/star_filled.png")
        
        self.master.window.option_add('*TCombobox*Listbox.font', combobox_font)

        self.dosi_combobox = Combobox(master.interaction_frame, font=combobox_font)
        self.dosi_combobox['values'] = list(region_code.keys())
        self.dosi_combobox.bind("<<ComboboxSelected>>", self.select_dosi)

        self.sigungu_combobox = Combobox(master.interaction_frame, font=combobox_font)
        self.sigungu_combobox['values'] = None
        self.sigungu_combobox.bind("<<ComboboxSelected>>", self.select_sigungu)
        
        self.search_input = PlaceholderEntry(master.interaction_frame, 
                                             placeholder="상세주소", 
                                             font=default_font)
        self.search_input.bind("<KeyPress>", self.press_enter)
        self.search_input.bind("<KeyRelease>", self.update_favorites)
        
        self.search_icon = PhotoImage(file="img/search_icon.png")
        self.search_button = Button(master.interaction_frame, 
                                    image=self.search_icon,
                                    command=lambda: self.search(self.make_address()))
        
        self.add_to_favorites_button = Button(master.interaction_frame, 
                                              image=self.star_empty_img,
                                              font=default_font, 
                                              command=self.add_to_favorites)

        
        self.result_listbox = Listbox(master.interaction_frame, font=info_font)
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
            self.chargers: List[Charger] = get_chargers_in_region(service_key["decoding"], code)
            # self.data = get_data(service_key["decoding"], addr)['data']

            if addr in recent_list:
                recent_list.remove(addr)
            recent_list.insert(0, addr)

            for charger in self.chargers:
                self.result_listbox.insert(END, charger.name)
        
        charger_coords = [charger.coord for charger in self.chargers]
        self.master.update_map(addr, charger_coords)
        self.master.info_widgets.set_graph(self.chargers)

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
        charger_coords = [charger.coord for charger in self.chargers]
        self.master.update_map(
            self.chargers[self.result_listbox.curselection()[0]].addr, 
            charger_coords
        )
        
        self.master.info_widgets.details_listbox.delete(0, END)
        self.master.info_widgets.details_listbox.insert(
            END, self.chargers[self.result_listbox.curselection()[0]].addr)
        self.master.info_widgets.details_listbox.insert(
            END, self.chargers[self.result_listbox.curselection()[0]].getState())
        self.master.info_widgets.details_listbox.insert(
            END, self.chargers[self.result_listbox.curselection()[0]].getType())
        self.master.info_widgets.details_listbox.insert(
            END, "주차: " + self.chargers[self.result_listbox.curselection()[0]].getParking())
        self.master.info_widgets.details_listbox.insert(
            END, self.chargers[self.result_listbox.curselection()[0]].getLimit())
        self.master.info_widgets.details_listbox.insert(
            END, self.chargers[self.result_listbox.curselection()[0]].note)
        self.master.info_widgets.details_listbox.insert(
            END, "출력: " + self.chargers[self.result_listbox.curselection()[0]].getOutput())
        self.master.info_widgets.details_listbox.insert(
            END, "충전방식: " + self.chargers[self.result_listbox.curselection()[0]].method)


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
        self.master.search_widgets.search_input.delete(0, END)
        self.master.search_widgets.search_input.foc_in(None)
        self.master.search_widgets.search_input.insert(0, self.listbox.get(self.listbox.curselection()))
        self.master.search_widgets.update_favorites(None)
        self.master.search_widgets.search(self.listbox.get(self.listbox.curselection()))
        self.master.search_widgets.dosi_combobox.set('')
        self.master.search_widgets.sigungu_combobox.set('')


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
        self.master.search_widgets.search_input.delete(0, END)
        self.master.search_widgets.search_input.foc_in(None)
        self.master.search_widgets.search_input.insert(0, self.listbox.get(self.listbox.curselection()))
        self.master.search_widgets.update_favorites(None)
        self.master.search_widgets.search(self.listbox.get(self.listbox.curselection()))
        self.master.search_widgets.dosi_combobox.set('')
        self.master.search_widgets.sigungu_combobox.set('')


class InfoWidgets:
    def __init__(self, master):
        self.master = master

        self.details_listbox = Listbox(master.info_frame, font=info_font)

        self.available_label =  Label(
                                    master.info_frame, 
                                    text="사용가능", 
                                    font=default_font
                                )
        self.available_progress = Progressbar(
                                    master.info_frame, 
                                    orient=HORIZONTAL, 
                                    length=180, 
                                    mode='determinate', 
                                    maximum=0, 
                                    value=0
                                )
        self.available_count_label = Label(
                                    master.info_frame, 
                                    text="0개", 
                                    font=default_font
                                )

        self.occupied_label =   Label(
                                    master.info_frame, 
                                    text="사용중", 
                                    font=default_font
                                )
        self.occupied_progress = Progressbar(
                                    master.info_frame, 
                                    orient=HORIZONTAL, 
                                    length=180, 
                                    mode='determinate', 
                                    maximum=0, 
                                    value=0
                                )
        self.occupied_count_label = Label(
                                    master.info_frame, 
                                    text="0개", 
                                    font=default_font
                                )

        self.disabled_label =   Label(
                                    master.info_frame, 
                                    text="사용불가", 
                                    font=default_font
                                )
        self.disabled_progress = Progressbar(
                                    master.info_frame, 
                                    orient=HORIZONTAL, 
                                    length=180, 
                                    mode='determinate', 
                                    maximum=0, 
                                    value=0
                                )
        self.disabled_count_label = Label(
                                    master.info_frame, 
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

    def set_graph(self, chargers: List[Charger]):
        available = 0
        occupied = 0
        disabled = 0

        for charger in chargers:
            if charger.getState() == "사용가능":
                available += 1
            elif charger.getState() == "사용중":
                occupied += 1
            else:
                disabled += 1

        total = available + occupied + disabled
        self.available_progress.configure(value=available, maximum=total)
        self.available_count_label.configure(text=f"{available}개")
        self.occupied_progress.configure(value=occupied, maximum=total)
        self.occupied_count_label.configure(text=f"{occupied}개")
        self.disabled_progress.configure(value=disabled, maximum=total)
        self.disabled_count_label.configure(text=f"{disabled}개")


class MapWidgets:
    def __init__(self, master):
        self.master = master

        self.zoom = 13
        self.size = "900x900"
        self.address = "서울특별시 중구 을지로2가"
        self.markers = []
        self.path = []

        self.map = Canvas(self.master.map_frame, width=900, height=900, bg="white")        # 테스트시 api호출 막기 위해 캔버스로 대체
        
        # self.map_img = get_googlemap(service_key["google"], self.address, self.size)
        # self.map = Label(self.master.map_frame, image=self.map_img)

        self.zoom_in_button = Button(self.master.map_frame, text="+", font=("Consolas", 40), command=self.zoom_in)
        self.zoom_out_button = Button(self.master.map_frame, text="-", font=("Consolas", 48), command=self.zoom_out)

    def update_map(self, addr, markers=[]):
        self.address = addr
        self.markers = markers
        self.show_map()

    def show_map(self):
        self.map_img = get_googlemap(service_key["google"], self.address, self.size, self.zoom, self.markers, self.path)
        self.map.configure(image=self.map_img)

    def place(self):
        self.map.pack()
        self.zoom_in_button.place(x=900-60, y=900-60, width=50, height=50)
        self.zoom_out_button.place(x=900-60-60, y=900-60, width=50, height=50)

    def zoom_in(self):
        self.zoom += 1
        if self.zoom > 20:
            self.zoom = 20
        self.show_map()

    def zoom_out(self):
        self.zoom -= 1
        if self.zoom < 5:
            self.zoom = 5
        self.show_map()


class GUI:
    def __init__(self):
        self.window = Tk()
        self.window.title("전기차 충전소 검색")

        self.interaction_frame = Frame(self.window)
        self.interaction_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # -- INTERACTION WIDGETS --
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

        # -- INTERACTION WIDGETS --
        self.search_widgets = SearchWidgets(self)
        self.search_widgets.place()
        self.favorites_widgets = FavoritesWidgets(self)
        self.recent_widgets = RecentWidgets(self)

        self.info_frame = Frame(self.interaction_frame, width=400, height=480)
        self.info_frame.pack(side=BOTTOM)

        self.info_widgets = InfoWidgets(self)
        self.info_widgets.place()
        
        # -- MAP WIDGETS --
        self.map_frame = Frame(self.window, padx=10, pady=10)
        self.map_frame.pack(side=LEFT, fill=BOTH, expand=True)
        
        self.map_widgets = MapWidgets(self)
        self.map_widgets.place()

        self.window.mainloop()

    def update_map(self, addr, markers=[]):
        self.map_widgets.update_map(addr, markers)

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
        self.share_window = Toplevel(self.window)
        self.share_window.resizable(0, 0)
        self.share_window.geometry("600x70")
        self.share_window.title('공유')
        self.share_window.attributes('-topmost', 'true')
        self.share_window.grab_set()
        self.share_window.focus_set()

        share_label = Label(self.share_window, text="email", font=default_font)
        share_label.place(x=10, y=10, width=100, height=50)

        share_entry = Entry(self.share_window, font=default_font, width=30)
        share_entry.place(x=120, y=10, width=400, height=50)

        self.img = PhotoImage(file="img/send.png")
        share_button = Button(self.share_window, image=self.img,
                              command=lambda: self.send_email(share_entry.get()))
        share_button.place(x=530, y=10, width=50, height=50)

    def send_email(self, email):
        self.share_window.destroy()


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