from pyrogram import Client, idle
from os.path import exists

if not exists("../database/allPic.csv"):
    open("../database/allPic.csv", 'w').write("name;id\n")

# crea accanto a main.py il file myClientParameters.py con dentro queste tre variabili, io l'ho messo in .gitignore
from myClientParameters import t_id, t_hash, test_token
from plugins.myParameters import TEST_GROUP_ID

plugins = dict(root="plugins")
title = "testbot"


async def main():
    bot = Client(
        name=title,
        api_id=t_id,
        api_hash=t_hash,
        bot_token=test_token,
        plugins=plugins
    )

    await bot.start()

    await bot.send_message(chat_id=TEST_GROUP_ID, text="Ready")
    print("READY")

    await idle()

    await bot.send_message(chat_id=TEST_GROUP_ID, text="Stop")
    # await bot.stop()
    print("Stop")

if __name__ == "__main__":
    # from asyncio import run
    # run(main())
    from platform import python_version_tuple
    if python_version_tuple() >= ("3", "11"):
        from asyncio import Runner
        with Runner() as runner:
            runner.get_loop().run_until_complete(main())
    else:
        from asyncio import new_event_loop
        loop = new_event_loop()
        loop.run_until_complete(main())
