from pyrogram import Client, idle
# from pyrogram.methods.utilities.idle import idle
from os.path import exists
# Crea il file se non esiste
if not exists("../database/allPic.csv"):
    open("../database/allPic.csv", 'w').write("name;id\n")

# crea accanto a main.py il file myClientParameters.py con dentro queste tre variabili, io l'ho messo in .gitignore
from myClientParameters import t_id, t_hash, t_token, pushbullet_API_KEY as pushKey
from plugins.myParameters import TEST_GROUP_ID
from pushbullet import Pushbullet
'''
t_id = "id numerico"
t_hash = "hash alfanumerico"
t_token = "token ottenuto con botFather"
'''

pb = Pushbullet(pushKey)
plugins = dict(root="plugins")
title = "MeteoATbot"


async def main():
    bot = Client(
        name=title,
        api_id=t_id,
        api_hash=t_hash,
        bot_token=t_token,
        plugins=plugins
    )

    await bot.start()

    async def set_status(status: str):
        from pyrogram.raw.functions.bots import GetBotInfo, SetBotInfo
        try:
            await bot.invoke(SetBotInfo(
                lang_code="",
                name=(await bot.invoke(GetBotInfo(lang_code=""))).name,
                description="contatta @ill_magnus",
                about=f"ℹ️ BOT STATUS:\n\n    {status}"
            ))
        except:
            await bot.send_message(TEST_GROUP_ID, f"probabilmente è in flood wait\nstatus:{status}")

    # end def
    await set_status("🟢 Online")

    await bot.send_message(chat_id=TEST_GROUP_ID, text="Ready")
    # print("READY")
    pb.push_note(title, "Ready")

    await idle()

    pb.push_note(title, "Stop")
    await bot.send_message(chat_id=TEST_GROUP_ID, text="Stop")
    await set_status("🔴 Offline")
    # await bot.stop()
    # print("Stop")

if __name__ == "__main__":
    # from asyncio import run
    # run(main())
    import uvloop
    uvloop.install()

    from platform import python_version_tuple
    if python_version_tuple() >= ("3", "11"):
        from asyncio import Runner
        with Runner() as runner:
            runner.get_loop().run_until_complete(main())
    else:
        from asyncio import new_event_loop
        loop = new_event_loop()
        loop.run_until_complete(main())
