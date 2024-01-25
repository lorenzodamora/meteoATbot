from pyrogram import Client
from os.path import exists
# Crea il file se non esiste
if not exists("../database/allPic.csv"):
    open("../database/allPic.csv", 'w').write("name;id\n")

# crea accanto a main.py il file myClientParameters.py con dentro queste tre variabili, io l'ho messo in .gitignore
from myClientParameters import t_id, t_hash, t_token, pushbullet_API_KEY as pushKey
from plugins.myParameters import TEST_GROUP_ID
'''
from pushbullet import Pushbullet
t_id = "id numerico"
t_hash = "hash alfanumerico"
t_token = "token ottenuto con botFather"
'''

# pb = Pushbullet(pushKey)
plugins = dict(root="plugins")
title = "MeteoATbot"
bot = Client(
    name=title,
    api_id=t_id,
    api_hash=t_hash,
    bot_token=t_token,
    plugins=plugins
)

with bot:
    try:
        bot.send_message(chat_id=TEST_GROUP_ID, text="Ready")
        # bot.edit_message_text(chat_id=channel_id, message_id=2, text="ℹ️ BOT STATUS:\n\n    🟢 Online")
    except Exception as e:
        # print("probabilmente il messaggio era già settato su \"online\"")
        print(e)
    finally:
        print("READY")
        # pb.push_note(title, "Ready")

try:
    bot.run()
finally:
    print("Stop")
    # pb.push_note(title, "Stop")
    bot.start()
    bot.send_message(chat_id=TEST_GROUP_ID, text="Stop")
    # bot.edit_message_text(chat_id=channel_id, message_id=2, text="ℹ️ BOT STATUS:\n\n    🔴 Offline")
    bot.stop()
