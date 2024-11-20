# Osint
'''
.ip</code> <code>.mail</code> <code>.phone</code>:: Пробив. \n\n<b>Использование</b>: \n<code>.phone 79xxxxxx</code> <i>Поиск по телефону</i>\n<code>.mail почта@почта.ххх</code> <i>поиск по почте</i>\n<code>.ip 123.255.123.123</code> <i>- поиск по айпи адресу</i>
'''

from telethon import events
import asyncio
import requests, json
import subprocess


def a(client):

    @client.on(events.NewMessage(pattern=r"\.ip", outgoing=True))
    async def _3(event):

        args = event.text.split(' ')
        if len(args) <2:
            await event.edit('<b>❌ Использовать с IP! \nПример:</b>\n<code>.ip 123.456.789.021</code>', parse_mode='html')
            return
        else:
            ip = args[-1]

        data = requests.get(f"http://ipwho.is/{ip}").json()

        if data['success']:
            await event.edit(
                f"<b>⚡️Цель:</b> <code>{ip}</code>"
                f"\n\n<b>├🗄 Провайдер (ISP):</b> <code>{data['connection']['isp']}</code>"
                f"\n<b>├⚙️ Тип:</b> <code>{data['type']}</code>"
                f"\n<b>├{data['flag']['emoji']} Страна:</b> <code>{data['country']}</code>"
                f"\n<b>├🌇 Город:</b> <code>{data['city']}</code>"
                f"\n<b>├📌 Регион:</b> <code>{data['region']}</code>"
                f"\n<b>├📮 Почтовый код:</b> <code>{data['postal']}</code>"
                f"\n<b>├📍 Широта:</b> <code>{data['latitude']}</code>"
                f"\n<b>└📍 Долгота:</b> <code>{data['longitude']}</code>"
                f'''\n\n└<b>🗺 Карты:</b> <a href="https://www.google.com/maps/place/{data['latitude']}+{data['longitude']}">ссылка</a>''',
                parse_mode='html')
        else:
            await event.edit("<b>❌ Неверный IP!</b>",parse_mode='html')

    @client.on(events.NewMessage(pattern=r"\.phone", outgoing=True))
    async def _4(event):

        args = event.text.split(' ')
        if len(args) <2:
            await event.edit('<b>❌ Использовать с номером телефона! \nПример:</b>\n<code>.phone +788005553535</code>', parse_mode='html')
            return
        else:
            phone = args[-1].replace(' ','')
            response = requests.get(f"https://htmlweb.ru/geo/api.php?json&telcod={phone}")
            data = json.loads(response.content)
            
            limit = data['limit']
                        
            if limit == 0:
                await event.edit("<b>❌ У вас закончился лимит на сервисе. Попробуйте включить VPN и повторить попытку!</b>",parse_mode='html')
            else:
                if 'message' in data:
                    text = "<code>Анонимный виртуальный номер, используется только в телеграм</code>"
                    await event.edit(
                        f"<b>⚡️ Цель:</b> <code>{phone}</code>"
                        f"\n\n<b>└Информация о номере:</b> <code>{text}</code>",
                        parse_mode='html'
                    )

                else:
                    operator = data['0']['oper']
                    operator_brand = data['0']['oper_brand']
                    country = data['country']['name']
                    location = data['country']['location']
                    iso = data['country']['iso']
                    capital = data['capital']['name']
                    latitude = data['capital']['latitude']
                    longitude = data['capital']['longitude']
                    timezone = data['capital']['tz']

                    await event.edit(
                        f"<b>⚡️Цель:</b> <code>{phone}</code>"
                        f"\n\n<b>├📞 Оператор:</b> <code>{operator}</code>"
                        f"\n<b>├🏷 Бренд оператора:</b> <code>{operator_brand}</code>"
                        f"\n<b>├🧿ISO:</b> <code>{iso}</code>"
                        f"\n<b>├🏴‍☠️Страна</b>:<code>{country}</code>"
                        f"\n<b>├🌍 Местоположение:</b> <code>{location}</code>"
                        f"\n<b>├🏙 Столица:</b> <code>{capital}</code>"
                        f"\n<b>├🌐 Широта:</b> <code>{latitude}</code>"
                        f"\n<b>├🌐 Долгота:</b> <code>{longitude}</code>"
                        f"\n<b>├🗺 Карты:</b> <a href=\"https://www.google.com/maps/place/{latitude}+{longitude}\">ссылка</a>"
                        f"\n└<b>⏰ Часовой пояс:</b> <code>{timezone}</code>"
                        f"\n\n<b>🚫 Осталось запросов</b>:<code>{limit}</code>"
                        f"\n🛜:<code>Если закончились лимиты, просто включите VPN</code>",
                        parse_mode='html'
                    )



    @client.on(events.NewMessage(pattern=r"\.mail", outgoing=True))
    async def _5(event):

        args = event.text.split(' ')
        if len(args) <2:
            await event.edit('<b>❌ Использовать с электронной почтой! \nПример:</b>\n<code>.phone example@mail.ru <used></code>', parse_mode='html')
            return
        else:
            mail = args[1]
            used = '--only-used' if len(args) == 3 and args[2] == 'used' else ''
            await event.edit("<b>🔎 Ищу информацию о почте...</b>", parse_mode='html')

            result = subprocess.run(f"holehe {mail} {used}", capture_output=True, text=True, check=True)
            result.stdout = "\n".join(result.stdout.split("\n")[4:])
            result.stdout = "\n".join(result.stdout.split("\n")[:-4])
            result.stdout = "\n".join([f"{line}" if "[+]" in line else line for line in result.stdout.split("\n")])
            result.stdout = "\n".join([f"{line}" if "[-]" in line else line for line in result.stdout.split("\n")])
            result.stdout = "\n".join([f"{line}" if "[x]" in line else line for line in result.stdout.split("\n")])

            message = str(result.stdout)

            message = message.replace(",",'')
            message = message.replace("[x]",'📛')
            message = message.replace("[-]","❌")
            message = message.replace("[+]","✅")
            message = message.replace("Email used","<b>- Почта зарегистрирована</b>\n")
            message = message.replace("Email not used","<b>- Почта не зарегистрирована</b>\n")
            message = message.replace("Rate limit","<b>- Рейт лимит на сервере</b>\n\n")
            message = message.replace("websites checked in","вебсайтов проверено за")
            message = message.replace("seconds","сек")


            await event.edit(message, parse_mode='html')



if __name__ == '__main__':
    try:
        a(client)
    except Exception as e:
        print(e)
        pass
