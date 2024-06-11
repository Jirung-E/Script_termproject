import telepot
import time
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
    
    text: str = msg['text']

    if text.startswith('도움'):
        send_message(chat_id, "도움!!!")
    elif text.startswith('검색'):
        send_image(chat_id, "temp/map.png")
    else:
        send_message(chat_id, "뭐라는거야..")



bot.message_loop(handle)
