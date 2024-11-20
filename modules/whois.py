# Whois
'''
.whois:: Показывает информацию о вебсайте. \nИспользование <code>.whois (вебсайт) - выводит информацию о вебсайте</code>\n\n<b>Пример:</b>\n\n<code>.whois google.com</code>
'''
from asyncio import sleep
from telethon import events, types
import whois


def a(client):
    @client.on(events.NewMessage(pattern=r"\.whois",outgoing=True))
    async def whois_check(event: types.Message) -> None:
        args = event.text.split(' ')
        if len(args) != 2:
            await event.edit(
                 "<b>❌Вводить команду с ccылкой на сайт!\nПример:</b><code>.whois google.com</code>",
                 parse_mode='html'
                             )
            return
        url = args[-1]
        await event.edit("<b>⏳ Проверка...</b>",parse_mode='html')
        try:
            domain_info=whois.whois(url)

            await event.edit(
                text=f"<b>Информация о сайте:"
                f"\n├<b>🎯Цель: </b><code>{url}</code>"
                f"\n|"
                f"\n├<b>🌐Домен:</b> <code>{domain_info.domain_name}</code>"
                f"\n├<b>🛃Зарегистрирован:</b> <code>{domain_info.creation_date}</code>"
                f"\n├<b>⌛️Истекает:</b> <code>{domain_info.expiration_date}</code>"
                f"\n├<b>👤Владелец:</b> <code>{domain_info.registrant_name}</code>"
                f"\n├<b>🏣Организация:</b> <code>{domain_info.registrant_organization}</code>"
                f"\n├<b>📌Адрес:</b> <code>{domain_info.registrant_address}</code>"
                f"\n├<b>🌇Город:</b> <code>{domain_info.registrant_city}</code>"
                f"\n├<b>🌇Штат:</b> <code>{domain_info.registrant_state}</code>"
                f"\n├<b>📬Почтовый индекс:</b> <code>{domain_info.registrant_postal_code}</code>"
                f"\n├<b>🏴Страна:</b> <code>{domain_info.registrant_country}</code>"
                f"\n└<b>IP-адрес:</b> <code>{domain_info.name_servers}</code>",
                parse_mode='html'
                )
        except Exception as e:
            await event.edit(f"<b>❌При проверке произошла ошибка:</b>\n<code>{e}</code",parse_mode='html')
    	        
          


if __name__ == '__main__':
	try:
		a(client)
	except:
		pass