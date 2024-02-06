"""
questo file è l'event handler, evito di usare i filter per evitare certi strani bug
"""
from pyrogram import Client
from pyrogram.types import Message as Msg
from pyrogram.enums import ChatMemberStatus, ChatType
from asyncio import create_task


def check_cmd(cmd: str, comandi: dict[str, int]) -> bool:
    """
    Controlla se l'input dell'utente corrisponde a uno dei comandi specificati.

    Fa una corrispondenza key sensitive.

    :param cmd: Testo di input.
    :type cmd: str
    :param comandi: Dizionario contenente coppie key-value, dove:
        - Key (str): il testo del comando da cercare.
        - Value (int): il tipo di check da effettuare sul comando.
          - 1 '^$': 'only' cerca una corrispondenza esatta.
          - 2 '/': 'command' cerca se la stringa inizia con il testo del comando.
          - 3 '': 'within' cerca se è presente
    :type comandi: dict[str, int]
    :return: True se c'è una corrispondenza, False altrimenti.
    :rtype: bool
    :raises ValueError: Se il dizionario contiene un valore non valido per il tipo di check.
    """
    for key, value in comandi.items():
        key = key.lower()
        cmd = cmd.lower()
        match value:
            case 1:
                if cmd == key:
                    return True
            case 2:
                if cmd.startswith(key):
                    return True
            case 3:
                if key in cmd:
                    return True
            case _:
                raise ValueError(f"Il dizionario contiene un valore non valido per il tipo di check: {value}\n"
                                 f"per i valori validi leggi la documentazione")
    return False


@Client.on_message()
async def event_handler(client: Client, m: Msg):
    if not (m.chat.type == ChatType.GROUP or m.chat.type == ChatType.SUPERGROUP):
        await m.reply("work only in group")
        return
    ch = m.chat.id
    from pyrogram.errors.exceptions.bad_request_400 import ChannelPrivate
    try:
        # member: ChatMember = await client.get_chat_member(ch, m.from_user.id)
        if (
            (await client.get_chat_member(ch, m.from_user.id)).status not in
            [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
        ):
            return
    except ChannelPrivate:
        return

    from .myParameters import TEST_GROUP_ID, GROUP_ID

    if ch not in [TEST_GROUP_ID, GROUP_ID]:
        await m.reply(f"questa chat non è abilitata, contatta @Ill_Magnus")
        return

    if m.text:
        import chardet
        result = chardet.detect(m.text.encode())
        if str(result['encoding']) != 'None':
            if m.text.startswith('/'):
                _ = create_task(handle_commands(client, m))


async def handle_commands(client: Client, msg: Msg):
    # Estrai il testo del messaggio dopo "/"
    cmd_txt = msg.text[1:]

    if not check_cmd(
        cmd_txt,
        {
            'h': 1, 'help': 1, '?': 1, 'commands': 1, 'c': 1,
            'help@MeteoATbot': 2,
            'add_pic': 2, 'addpic': 2, 'add': 2,
            'show_pic': 2, 'showpic': 2, 'show': 2,
            'edit_pic': 2, 'editpic': 2, 'edit': 2,
            'delete_pic': 2, 'deletepic': 2, 'delete': 2,
            'set_pic': 2, 'setpic': 2, 'set': 2
        }
    ) or await admin(client, msg.chat.id, msg.chat.is_admin):
        return

    # TODO parametri
    if check_cmd(cmd_txt, {'h': 1, 'help': 1, '?': 1, 'commands': 1, 'c': 1, 'help@MeteoATbot': 2}):
        id_ = msg.chat.id
        await msg.delete()
        await client.send_message(id_, "questo bot imposta pic semiautomaticamente nel gruppo.\n"
                                       "per vedere come aggiungere una pic vedere '`/add h`'\n"
                                       "per visualizzare le pic già inserite fare '`/show h`'\n"
                                       "per modificare una pic già inserita '`/edit h`'\n"
                                       "per eliminare una pic '`/delete h`'\n"
                                       "per impostare una pic '`/set h`'\n"
                                       "\n per evitare problemi fare attenzione al numero di spazi")

        '''
    elif cmd_txt == "test":
        phid = msg.reply_to_message.photo.file_id
        await client.download_media(phid, f"../database/pics/{phid}.jpg")
        await client.send_photo(GROUP_ID, phid, phid)
        # # #
        await client.send_photo("me", phid, "caption test")
        async for message in client.get_chat_history("me"):
            await client.send_message(GROUP_ID, str(vars(message)))

    elif cmd_txt == "test":
        from .myParameters import TEST_GROUP_ID
        ###
        from pyrogram.raw.functions.bots import GetBotInfo
        from pyrogram.raw.types import InputUser
        from pyrogram.raw.functions.users import GetUsers
        # bot.send_message(chat_id=TEST_GROUP_ID, text=str(bot.get_me()))
        inp = InputUser(user_id=6724866148, access_hash=1952675726081265999)
        # bot.send_message(chat_id=TEST_GROUP_ID, text=str(bot.invoke(GetUsers(id=[inp]))))
        bot.send_message(chat_id=TEST_GROUP_ID, text=str(bot.invoke(
            GetBotInfo(lang_code="en", bot=inp)
        )))
        from pyrogram.raw.types import InputUser
        from pyrogram.raw.functions.users import GetFullUser
        from pyrogram.enums import ParseMode
        from asyncio import sleep
        ps = ParseMode.DISABLED
        result = await client.invoke(GetFullUser(id=InputUser(user_id=6724866148, access_hash=1952675726081265999)))
        txt = str(result)
        chunk_s = 4096
        chunks = [txt[i:i + chunk_s] for i in range(0, len(txt), chunk_s)]

        for chunk in chunks:
            uncomplet = True
            while uncomplet:
                try:
                    await client.send_message(chat_id=TEST_GROUP_ID, text=str(chunk), parse_mode=ps)
                    uncomplet = False
                except:
                    await sleep(20)
            # end while
        # end for
        ###
        from pyrogram.raw.functions.bots import GetBotInfo, SetBotInfo
        from pyrogram.raw.types.bots import BotInfo
        from pyrogram.enums import ParseMode
        peer = await client.resolve_peer("MeteoATbot")
        await client.send_message(chat_id=TEST_GROUP_ID, text=str(peer), parse_mode=ParseMode.DISABLED)
        # r = await client.invoke(GetBotInfo(lang_code="", bot=peer))
        r: BotInfo = await client.invoke(GetBotInfo(lang_code=""))
        await client.send_message(chat_id=TEST_GROUP_ID, text=str(r), parse_mode=ParseMode.DISABLED)
        await client.invoke(SetBotInfo(lang_code="", name=r.name, description="contatta @ill_magnus", about="about"))
        '''

    elif check_cmd(cmd_txt, {'add_pic': 2, 'addpic': 2, 'add': 2}):
        split = cmd_txt.split(" ")
        rmsg = msg.reply_to_message
        if (
            (len(split) > 1 and split[1] in ['h', 'help', '?']) or
            not rmsg or not rmsg.photo or not rmsg.caption or
            rmsg.caption in ['h', 'help', '?']
        ):
            await client.send_message(
                msg.chat.id,
                "Quando vuoi aggiungere una pic devi innanzitutto inviare l'immagine, e nella sua descrizione "
                "dargli il nome di identificazione (univoco)\n"
                "dopodiché rispondere a quel messaggio con `/add`\n"
                "per semplicità consiglio di non usare simboli, "
                "solo caratteri alfanumerici semplici minuscoli [a-z][0-9]")
            return
        from .commands import add_pic
        await add_pic(client, rmsg.photo.file_id, rmsg.caption, rmsg.chat.id)

    elif check_cmd(cmd_txt, {'show_pic': 2, 'showpic': 2, 'show': 2}):
        split = cmd_txt.split(" ")
        if len(split) > 1 and split[1] in ['h', 'help', '?']:
            await client.send_message(
                msg.chat.id,
                "Per visualizzare la lista di tutte le pic semplicemente '/show', per vedere una specifica "
                "pic fare '/show {nome pic}'")
            return
        from .commands import show_pic
        name = cmd_txt[len(cmd_txt.split(" ")[0]) + 1:]
        await show_pic(client, msg, name)

    elif check_cmd(cmd_txt, {'edit_pic': 2, 'editpic': 2, 'edit': 2}):
        split = cmd_txt.split(" ")
        rmsg = msg.reply_to_message
        if (
            (len(split) > 1 and split[1] in ['h', 'help', '?']) or
            not rmsg or not rmsg.photo or not rmsg.caption or
            rmsg.caption in ['h', 'help', '?']
        ):
            await client.send_message(
                msg.chat.id,
                "Per modificare si intende cambiare pic per lo stesso nome, usare '/edit' come fosse '/add'\n"
                "per eliminare il nome e la pic usare '/delete {nome pic}'")
            return
        from .commands import add_pic
        await add_pic(client, rmsg.photo.file_id, rmsg.caption, rmsg.chat.id, True)

    elif check_cmd(cmd_txt, {'delete_pic': 2, 'deletepic': 2, 'delete': 2}):
        split = cmd_txt.split(" ")
        name = cmd_txt[len(cmd_txt.split(" ")[0]) + 1:]
        if (len(split) > 1 and split[1] in ['h', 'help', '?']) or name == '':
            await client.send_message(
                msg.chat.id,
                "Per eliminare una specifica pic fare '/delete {nome pic}'")
            return
        from .commands import delete_pic
        await delete_pic(client, name, msg.chat.id)

    elif check_cmd(cmd_txt, {'set_pic': 2, 'setpic': 2, 'set': 2}):
        split = cmd_txt.split(" ")
        name = cmd_txt[len(cmd_txt.split(" ")[0]) + 1:]
        if (len(split) > 1 and split[1] in ['h', 'help', '?']) or name == '':
            await client.send_message(
                msg.chat.id,
                "Per impostare una specifica pic fare '/set {nome pic}'")
            return
        from .commands import set_pic
        try:
            await set_pic(client, name, msg.chat.id)
        except Exception as e:
            await client.send_message(msg.chat.id, text=f"error in set_pic:\n\n{e}")


async def admin(client: Client, chat_id: int, is_admin):
    """
    is_admin può essere sia bool che None
    :return: is_admin invertito
    """
    if not is_admin:
        await client.send_message(chat_id, "il bot non è admin")
    return not is_admin
