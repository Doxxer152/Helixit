# HIDE
import asyncio
from io import BytesIO
import re
import requests
from telethon import TelegramClient, events
from telethon.tl import functions
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from concurrent.futures import ThreadPoolExecutor
from config import *

code_regex = re.compile(r"t\.me/(CryptoBot|send|tonRocketBot|CryptoTestnetBot|wallet|xrocket|xJetSwapBot)\?start=(CQ[A-Za-z0-9]{10}|C-[A-Za-z0-9]{10}|t_[A-Za-z0-9]{15}|mci_[A-Za-z0-9]{15}|c_[a-z0-9]{24})", re.IGNORECASE)
url_regex = re.compile(r"https:\/\/t\.me\/\+(\w{12,})")
public_regex = re.compile(r"https:\/\/t\.me\/(\w{4,})")

replace_chars = ''' @#&+()*"'…;,!№•—–·±<{>}†★‡„“”«»‚‘’‹›¡¿‽~`|√π÷×§∆\\°^%©®™✓₤$₼€₸₾₶฿₳₥₦₫₿¤₲₩₮¥₽₻₷₱₧£₨¢₠₣₢₺₵₡₹₴₯₰₪'''
translation = str.maketrans('', '', replace_chars)

executor = ThreadPoolExecutor(max_workers=5)

crypto_black_list = [1622808649, 1559501630, 1985737506, 5014831088, 6014729293, 5794061503]

global checks
global checks_count
global wallet
checks = []
wallet = []
channels = []
captches = []
checks_count = 0

def ocr_space_sync(file: bytes, overlay=False, language='eng', scale=True, OCREngine=2):
    payload = {
        'isOverlayRequired': overlay,
        'apikey': "K88121615288957",
        'language': language,
        'scale': scale,
        'OCREngine': OCREngine
    }
    response = requests.post(
        'https://api.ocr.space/parse/image',
        data=payload,
        files={'filename': ('image.png', file, 'image/png')}
    )
    result = response.json()
    return result.get('ParsedResults')[0].get('ParsedText').replace(" ", "")

async def ocr_space(file: bytes, overlay=False, language='eng'):
    loop = asyncio.get_running_loop()
    recognized_text = await loop.run_in_executor(
        executor, ocr_space_sync, file, overlay, language
    )
    return recognized_text

def a(client):

    @client.on(events.NewMessage(chats=[1985737506], pattern="⚠️ Вы не можете активировать этот чек, так как вы не являетесь подписчиком канала"))
    async def handle_new_message(event):
        global wallet
        code = None
        try:
            for row in event.message.reply_markup.rows:
                for button in row.buttons:
                    try:
                        try:
                            check = code_regex.search(button.url)
                            if check:
                                code = check.group(2)
                        except:
                            pass
                        channel = url_regex.search(button.url)
                        public_channel = public_regex.search(button.url)
                        if channel:
                            await client(ImportChatInviteRequest(channel.group(1)))
                        if public_channel:
                            await client(JoinChannelRequest(public_channel.group(1)))
                    except:
                        pass
        except AttributeError:
            pass
        if code not in wallet:
            await client.send_message('wallet', message=f'/start {code}')
            wallet.append(code)

    @client.on(events.NewMessage(chats=[1559501630,1622808649], pattern="Чтобы"))
    async def handle_new_message(event):
        try:
            for row in event.message.reply_markup.rows:
                for button in row.buttons:
                    try:
                        channel = url_regex.search(button.url)
                        if channel:
                            try:
                                await client(functions.channels.JoinChannelRequest(
                                    channel=channel.group(1)
                                ))
                            except:
                                await client(ImportChatInviteRequest(channel.group(1)))
                    except:
                        pass
        except AttributeError:
            pass
        await event.message.click(data=b'check-subscribe')

    @client.on(events.NewMessage(chats=[5014831088], pattern="Для активации чека"))
    async def handle_new_message(event):
        try:
            for row in event.message.reply_markup.rows:
                for button in row.buttons:
                    try:
                        channel = url_regex.search(button.url)
                        public_channel = public_regex.search(button.url)
                        if channel:
                            await client(ImportChatInviteRequest(channel.group(1)))
                        if public_channel:
                            await client(JoinChannelRequest(public_channel.group(1)))
                    except:
                        pass
        except AttributeError:
            pass
        await event.message.click(data=b'Check')

    @client.on(events.NewMessage(chats=[5794061503]))
    async def handle_new_message(event):
        try:
            for row in event.message.reply_markup.rows:
                for button in row.buttons:
                    try:
                        try:
                            if (button.data.decode()).startswith(('showCheque_', 'activateCheque_')):
                                await event.message.click(data=button.data)
                        except:
                            pass
                        channel = url_regex.search(button.url)
                        public_channel = public_regex.search(button.url)
                        if channel:
                            await client(ImportChatInviteRequest(channel.group(1)))
                        if public_channel:
                            await client(JoinChannelRequest(public_channel.group(1)))
                    except:
                        pass
        except AttributeError:
            pass

    async def filter(event):
        for word in ['Вы получили', 'Вы обналичили чек на сумму:', '✅ Вы получили:', '💰 Вы получили']:
            if word in event.message.text:
                return True
        return False

    @client.on(events.MessageEdited(chats=crypto_black_list, func=filter))
    @client.on(events.NewMessage(chats=crypto_black_list, func=filter))
    async def handle_new_message(event):
        try:
            bot = (await client.get_entity(event.message.peer_id.user_id)).usernames[0].username
        except:
            bot = (await client.get_entity(event.message.peer_id.user_id)).username
        summ = event.raw_text.split('\n')[0].replace('Вы получили ', '').replace('✅ Вы получили: ', '').replace('💰 Вы получили ', '').replace('Вы обналичили чек на сумму: ', '')
        global checks_count
        checks_count += 1

    @client.on(events.MessageEdited(outgoing=False, chats=crypto_black_list, blacklist_chats=True))
    @client.on(events.NewMessage(outgoing=False, chats=crypto_black_list, blacklist_chats=True))
    async def handle_new_message(event):
        global checks
        message_text = event.message.text.translate(translation)
        codes = code_regex.findall(message_text)
        if codes:
            for bot_name, code in codes:
                if code not in checks:
                    await client.send_message(bot_name, message=f'/start {code}')
                    checks.append(code)
        try:
            for row in event.message.reply_markup.rows:
                for button in row.buttons:
                    try:
                        match = code_regex.search(button.url)
                        if match:
                            if match.group(2) not in checks:
                                await client.send_message(match.group(1), message=f'/start {match.group(2)}')
                                checks.append(match.group(2))
                    except AttributeError:
                        pass
        except AttributeError:
            pass


    @client.on(events.NewMessage(chats=[1559501630], func=lambda e: e.photo))
    async def handle_photo_message(event):
        photo = await event.download_media(bytes)
        recognized_text = await ocr_space(file=photo)
        if recognized_text and recognized_text not in captches:
            await client.send_message('CryptoBot', message=recognized_text)
            await asyncio.sleep(0.1)
            message = (await client.get_messages('CryptoBot', limit=1))[0].message
            if 'Incorrect answer.' in message or 'Неверный ответ.' in message:
                print(f'[!] Ошибка антикаптчи > Не удалось разгадать каптчу, решите ее сами.')
                captches.append(recognized_text)

if __name__ == '__main__':
	try:
		a(client)
	except Exception as e:
		print(e)
		pass