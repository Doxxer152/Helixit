# Delme
'''
.delme</code>:: Удаляет все ваши сообщения в чате, где была выполнена команда \n\n<b>Использование</b>: \n<code>.delme <secret></code> <i>- Нужно будет подтвердить действие</i>
'''
from telethon import events
from telethon.tl.types import *

def a(client):
    @client.on(events.NewMessage(pattern=r"\.delme", outgoing=True))
    async def delme(message):
        chat = message.chat
        if chat:
            args = message.text.split(' ')
            secret = args[-1]
            if secret != str(message.chat.id+message.sender_id):
                await message.edit(f"<b>Если ты точно хочешь это сделать, то напиши:</b>\n<code>.delme {message.chat.id+message.sender_id}</code>",parse_mode='html')
                return
            all = (await message.client.get_messages(chat, from_user="me")).total
            messages = [msg async for msg in message.client.iter_messages(chat, from_user="me")]
            await message.edit(f"<b>{all} сообщений будет удалено!</b>", parse_mode='html')
            _ = ""
            async for msg in message.client.iter_messages(chat, from_user="me"):
                if _:
                    await msg.delete()
                else:
                    _ = "_"
            await message.delete()
        else:
            await message.edit("<b>В лс не чищу!</b>", parse_mode='html')
        

if __name__ == '__main__':
    try:
        a(client)
    except Exception as e:
        print(e)
        pass