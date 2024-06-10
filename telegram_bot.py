import telepot

with open("telegram_bot_id.txt", "r") as file:
    bot_id = file.read().strip()

bot = telepot.Bot(bot_id)
# print(bot.getMe())

# bot.sendMessage(6262946548, "Hello World!")

def send_message(chat_id, message):
    bot.sendMessage(chat_id, message, "HTML")


def send_image(chat_id, image):
    bot.sendPhoto(chat_id, image)


# send_message(6262946548, "<b>sjfkds;</b>")
# send_image(6262946548, open("img/charger_types.png", "rb"))