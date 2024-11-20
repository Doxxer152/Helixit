# Manual
'''
.manual</code> <code>.add_manual</code>:: Выводит мануалы. \nИспользование <code>.manual - выводит список мануалов</code> \n<code>.manual (название мануала)</code> <i>- Выводит содержимое выбранного мануала</i> \n<code>.add_manual + ответ на сообщение с документом</code> - добавляет новый мануал в утилиту
'''
from asyncio import sleep
from telethon import events
import asyncio
import os


def a(client):
	@client.on(events.NewMessage(pattern=r"\.manual", outgoing=True))
	async def manual(event):
		args = event.text.split(' ')

		if len(args) == 1:
			manuals = '\n'.join(f"·<code>{file.replace('.txt','')}</code>" for file in os.listdir('manuals'))

			text_to_send = f"<b>🛜 Список доступных мануалов:</b>\n{manuals}\n\n<b>👁‍🗨Чтобы посмотреть содержимое каждого мануала, введите команду:</b>\n<code>.manual названиемануала</code>"
			await event.edit(text_to_send, parse_mode='html')
		else:
			filename = args[-1]+".txt"

			if not filename in os.listdir("manuals"):
				await event.edit("<b>❌Файл с таким названием не найден. \nИспользуйте команду </b><code>.manuals</code><b> чтобы получить список мануалов</b>")
				return
			else:
				content = open(f"manuals/{filename}",'r',encoding='utf-8').read()
				if len(content) > 4000:
					await event.delete()
					await client.send_file(
						event.to_id,
						file=f'manuals/{filename}',
						caption=f"<b>📦Текст мануала слишком длинный для отправки текстом и был отправлен файлом \n\n📧Для просмотра содержимого, откройте этот файл в любом редакторе текста!</b>",
						parse_mode='html')
				else:
					await event.edit(f"<b>📦Содержимое мануала:</b>\n\n<code>{content}</code>",parse_mode='html')

	@client.on(events.NewMessage(pattern=r"\.add_manual", outgoing=True))
	async def add_manual(event):
		reply = await event.get_reply_message()
		if reply.media.document:
			await client.download_media(reply.media.document, 'manuals/')
			await event.edit("<b>📥 Файл сохранен успешно!</b>", parse_mode='html')
		else:
			await event.edit("<b>❌ Использовать в ответ на документ!</b>")
			return



if __name__ == '__main__':
	try:
		a(client)
	except:
		pass