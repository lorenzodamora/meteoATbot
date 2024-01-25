from pyrogram import Client
from pyrogram.types import Message as Msg


async def add_pic(client: Client, photo_id: str, caption: str, chat_id: int, overwrite=False, done=True):
    """alcuni controlli già fatti"""
    from .newpic import update_all_pic
    if await update_all_pic(caption, photo_id, overwrite):
        await client.download_media(photo_id, f"../database/pics/{photo_id}.jpg")
    if done:
        await client.send_message(chat_id, "done")


async def show_pic(client: Client, msg: Msg, name: str):
    from .newpic import lock_allPic
    import csv
    async with lock_allPic:
        with open("../database/allPic.csv", mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            rows = list(reader)
        # end open
    # end lock
    if name == "":
        pri: str = "**Lista di pic inserite:**\n\n"
        for row in rows:
            pri += str(row['name']) + "\n"
        await msg.reply(pri)
    else:
        for row in rows:
            if name == str(row['name']):
                phid = str(row['id'])
                try:
                    await msg.reply_cached_media(file_id=phid, caption=name)
                except:
                    pmsg = await msg.reply_photo(f"../database/pics/{phid}.jpg")
                    phid2 = pmsg.photo.file_id
                    if phid2 == phid:
                        return
                    await add_pic(client, phid2, name, msg.chat.id, True, False)
                    from os import remove
                    remove(f"../database/pics/{phid}.jpg")
                return
        await msg.reply("nessuna pic ha questo nome. guarda '/show h'")


async def delete_pic(client: Client, name: str, chat_id: int):
    from .newpic import lock_allPic
    import csv
    async with lock_allPic:
        with open("../database/allPic.csv", mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            rows = list(reader)
        # end open
    # end lock
    nrows = []
    non_presente = True
    for row in rows:
        if name == str(row['name']):
            non_presente = False
            from os import remove
            remove(f"../database/pics/{row['id']}.jpg")
        else:
            nrows.append(row)

    if non_presente:
        await client.send_message(chat_id, "nessuna pic ha questo nome. guarda '/delete h'")
        return
    async with lock_allPic:
        # Scrivi nel file CSV aggiornato
        with open("../database/allPic.csv", mode='w', newline='', encoding='utf-8') as file:
            # Scrivi le righe aggiornate nel file
            writer = csv.DictWriter(file, fieldnames=['name', 'id'], delimiter=';')
            writer.writeheader()
            writer.writerows(nrows)
    await client.send_message(chat_id, "done")


async def set_pic(client: Client, name: str, chat_id: int):
    from .newpic import lock_allPic
    import csv
    async with lock_allPic:
        with open("../database/allPic.csv", mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            rows = list(reader)
        # end open
    # end lock
    for row in rows:
        if name == str(row['name']):
            phid = str(row['id'])
            try:
                if not await client.set_chat_photo(chat_id, photo=phid):
                    raise "error: pic not set"
            except:
                await client.set_chat_photo(chat_id, photo=f"../database/pics/{phid}.jpg")
                await client.send_message(chat_id, "probabilmente la pic non è più presente nei server di "
                                                   "telegram, per risolvere fare un /edit su questa pic")
            return
    await client.send_message(chat_id, "nessuna pic ha questo nome. guarda le disponibili in '/show'")
