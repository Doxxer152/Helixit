# Short
'''
.short</code>:: Сократитель ссылок. \n\n<b>Использование</b>: \n<code>.short <ссылка></code> <i>Сократит ссылку</i>\n\n<b>Пример:</b>\n<code>.short google.com</code>
'''

from telethon import events
import asyncio
import requests, json
import subprocess


def a(client):

    @client.on(events.NewMessage(pattern=r"\.short", outgoing=True))
    async def _1(event):

        args = event.text.split(' ')
        if len(args) <2:
            await event.edit('<b>❌ Использовать с URL! \n\nПример:</b>\n<code>.short google.com</code>', parse_mode='html')
            return
        else:
            url = args[-1]

        data = requests.get(f"https://is.gd/create.php?format=simple&url={url}").text
        if 'is.gd' in data:
            await event.edit(f"<b>🗯 Короткая ссылка:</b>\n\n➤ <code>{data}</code>", parse_mode='html')
        elif "block" in data:
            await event.edit('<b>❌ URL Заблокирован, используйте другую ссылку</b>', parse_mode='html')

        else:
            await event.edit('<b>❌ Использовать с URL! \n\nПример:</b>\n<code>.short google.com</code>', parse_mode='html')


if __name__ == '__main__':
    try:
        a(client)
    except Exception as e:
        print(e)
        pass