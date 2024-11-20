# Фейк
'''
.fake_contact</code> <code>.fake_person</code>:: Фейк контакт. \n Использование: <code>.fake_contact</code> <имя> <номер без +>
'''
from telethon import events
import asyncio
from telethon import types
from faker import Faker
import random

fake = Faker(locale="RU-ru")

def a(client):

    @client.on(events.NewMessage(pattern=r"\.fake_contact", outgoing=True))
    async def _1(event):
        args = event.text.split(' ')
        if len(args)<3 or not args[-1].isdigit():
            await event.edit('<b>❌ Использовать с именем и номером! Пример:</b>\n<code>.fake_contact Иванов Иван 7999999999</code>', parse_mode='html')
            return
        else:
            phone = args[-1]
            name = ' '.join(args[1: -1])
            await event.delete()

            await client.send_file(event.to_id, types.InputMediaContact(
                phone_number=phone,
                first_name=name,
                last_name='',
                vcard=''
            ))

    @client.on(events.NewMessage(pattern=r"\.fake_person", outgoing=True))
    async def _2(event):
        if random.randint(0,3) >= 1:
            first_name=fake.first_name_male()
            middle_name=fake.middle_name_male()

        else:
            first_name=fake.first_name_female()
            middle_name=fake.middle_name_female()

        last_name=fake.last_name()
        full_name=f"{last_name} {first_name} {middle_name}"
        birthdate=fake.date_of_birth()
        age=fake.random_int(min=18,max=80)
        street_address=fake.street_address()
        city=fake.city()
        region=fake.region()
        postcode=fake.postcode()
        address=f"{street_address}, {city}, {region} {postcode}"
        email=fake.email();phone_number=fake.phone_number()
        inn=str(fake.random_number(digits=12,fix_len=True))
        snils=str(fake.random_number(digits=11,fix_len=True))
        passport_num=str(fake.random_number(digits=10,fix_len=True))
        passport_series=fake.random_int(min=1000,max=9999)
        await event.edit(
             "\n<b>🎭Новая фейковая личность:</b>"
             "\n<b>|</b>"
            f"\n<b>├👤 ФИО:</b> <code>{full_name}</code>"
            f"\n<b>├📅 Дата рождения:</b> <code>{birthdate.strftime('%d %B %Y')}</code>"
            f"\n<b>├⌛ Возраст:</b> <code>{age} лет</code>"
            f"\n<b>├🏠 Адрес:</b> <code>{address}</code>"
            f"\n<b>├📧 Email:</b> <code>{email}</code>"
            f"\n<b>├📞 Телефон:</b> <code>{phone_number}</code>"
            f"\n<b>├🔢 ИНН:</b> <code>{inn}</code>"
            f"\n<b>├🔢 СНИЛС:</b> <code>{snils}</code>"
            f"\n<b>└📑 Серия паспорта:</b> <code>{passport_series}</code> номер: <code>{passport_num}</code>",
            parse_mode='html'
            )
        
        


if __name__ == '__main__':
    try:
        a(client)
    except:
        pass