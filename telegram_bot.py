import telepot
import random
from apis import *









with open("telegram_bot_id.txt", "r") as file:
    bot_id = file.read().strip()

bot = telepot.Bot(bot_id)









def send_message(chat_id, message):
    bot.sendMessage(chat_id, message, "HTML")


def send_image(chat_id, path):
    bot.sendPhoto(chat_id, open(path, "rb"))


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type != 'text':
        send_message(chat_id, '텍스트만 지원합니다.')
        return
    
    text: str = msg['text'].strip()

    if text.startswith('도움'):
        m = "명령어 리스트\n"
        m += "검색 [지역] : [지역]의 충전소를 검색합니다.\n"
        send_message(chat_id, m)
    elif text.startswith('검색'):
        gmap = Client(key=service_key["google"])
        search = text[len('검색'):].strip()
        ss = search.split()

        while ss:
            s = ' '.join(ss)
            region_code = get_region_code(s)
            if region_code is None:
                ss.pop()
                continue
            break

        location = gmap.geocode(s)[0]['geometry']['location']
        location = GeoCoord(location['lat'], location['lng'])
        charger_groups = get_chargers_in_region(region_code)

        if region_code is None:
            m = "검색에 실패했습니다.\n"
            m += "'검색 [지역]' 의 형식으로 입력해주세요."
            send_message(chat_id, m)
            return
        
        send_message(chat_id, f"{search}에서 가장 가까워보이는 충전소 몇개를 보여드릴게요.")
        
        charger_groups.sort(key=lambda charger_group: distance2_between(charger_group.getAverageCoord(), location))
        markers = [chargers.getAverageCoord() for chargers in charger_groups]
        _ = get_googlemap(location, "1440x1440", 13, markers)

        for chargers in charger_groups[:5]:
            send_message(chat_id, chargers.addr)
            for charger in chargers.chargers:
                msgtext = "<b>" + charger.name + "</b>"
                msgtext += "\n"
                msgtext += "상태: " + charger.getState()
                msgtext += "\n"
                msgtext += "충전기 타입: " + charger.getType()
                msgtext += "\n"
                msgtext += "출력: " + charger.getOutput()
                msgtext += "\n"
                msgtext += "충전방식: " + charger.method
                msgtext += "\n"
                msgtext += "주차: " + charger.getParking()
                msgtext += "\n"
                
                limit = charger.getLimit()
                msgtext += "제한사항: " + (limit if limit != "무제한" else "없음")
                msgtext += "\n"
                
                if charger.note != "":
                    msgtext += "비고: " + charger.note
                    msgtext += "\n"
                send_message(chat_id, msgtext)
        send_image(chat_id, "temp/map.png")
    else:
        m = random.choice(["뭐라는거야..", "알아듣게말해", "...뭐?"])
        send_message(chat_id, m)



bot.message_loop(handle)

if __name__ == "__main__":
    while True:
        pass