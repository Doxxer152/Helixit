# Swat
'''
.swat:: Генерирует текст для сват-письма. \n Использование: <code>.swat</code> <code>"текст"</code> или  <ответ на сообщение> - <i>Заменит буквы на похожие в написанном вами сообщении</i>
'''
from telethon import events
import asyncio
from telethon import types
from random import choice

shablons = [
	"Я {NAME}. Б0ЛЬШЕ Я ЭT0Г0 TЕPПЕTЬ HЕ БYДY, $YKu. MHЕ П0ЕБATЬ HA П0$ЛЕД$TBuЯ u Я П0ЙДY HA ЭT0 ЧT0БЫ Д0KA3ATЬ, ЧT0 Я Х0TЬ HA ЧT0-T0 $П0$0БЕH. B MБ0Y $0Ш 1 П0 AДPЕ$Y YЛuЦA BЛAДuMuP0B$KAЯ 15 Я 3AЛ0ЖuЛ 3APЯДЫ ПЕP0K$uДA AЦЕT0HA, ГЕK$0ГЕHA A TAKЖЕ AMM0HAЛA! Я TPЕБYЮ Y BA$, ПuД0PA$0B, 100000$ HA H0MЕP {NUMBER} uHAЧЕ B$Е ДЕTKu ЭT0Й ХYЙHu B3ЛЕTЯT HA B03ДYХ.",
	"Я {NAME} 3AMuHuP0BAЛ BAШ T0PГ0BЫЙ ЦЕHTP 6 CAM0ДЕЛЬHЫMu Б0MБAMu BЕC0M 10KГ!!!! 3ABTPA 0Hu BCЕ HAХYЙ B30PBYTCЯ, ЕCЛu BЫ HЕ ПЕPЕШЛЕTЕ П0 M0ЕMY H0MЕPY TЕЛЕФ0HA 2 MuЛЛu0HA PYБЛЕЙ, T0 B HuЖHЕM H0BГ0P0ДЕ БYДЕT TPAYP, CYKu {NUMBER}",
	"3ДРABCTBYЙTЕ, Я {NAME} 3AMИHИР0BAЛ 3ДAHИЕ РAЙ0HH0Г0 CYДA Г0Р0ДA CAРAT0B CAM0ДЕЛЬHЫM B3РЫBHЫM YCTР0ЙCTB0M HA 0CH0BЕ AMM0HAЛA И ДЕT0HAT0Р0M И3 A3ИДA РTYTИ A TAКЖЕ ЧAC0BЫM MЕХAHИ3M0M C РAДИ0YПРABЛЕHИЕM. ЕCЛИ ЧЕРЕ3 2 ЧACA BЫ HЕ ПЕРЕBЕДЕTЕ HA M0Й H0MЕР TЕЛЕФ0HA {NUMBER} 5 MИЛЛИ0H0B РYБЛЕЙ, 3ДAHИЕ B3ЛЕTИT HA B03ДYХ, БYДЕT 0ЧЕHЬ MH0Г0 ЖЕРTB И BЫ HAК0HЕЦ TAКИ П0Д0ХHЕTЕ!",
	'Я АНОНИМ, МОЙ НОМЕР: {NUMBER} Я ТЗРРОРСТ ИЗ ГРУППИРОВКИ "УЖАС" И Я ЗАМUНи₽0Ва/\ ВСЗ ТЦ ГОРОДА ВОРОНЕЖ, Я ХОЧУ ЧТОБЫ ВЫ МНЗ ПЗРЗВЗЛИ 55 МИЛЛИОНОВ РУБЛЭЙ, ЗСЛИ ЖЗ Я НЗ УВЖУ ПЗРЗВОД В Т3Ч3HUИ 4@C@, то можетз Распр0щатbся CO CBOUMU БЛИЗКUМИ, Я 3@ БИ0МАССОВЫЗ И РУТUНЫЗ ВОМБЫ, Я ЖДУ ПЗРЗВОДА ПО НОМЗРУ {NUMBER}, У ВОС РОВНО 4@С, Д@ЖЗ НЗ ДУМАЙТЗ ПРИЕЗЖ@ТЬ КО МНЗ ДОмой, я ВaС РaСТРЭЛЯЮ НaХYЙ, 3СЛИ МНЗ П0ЗВОНИТ ПЗРЗГОВ0РЩИК Я С РaЗY @КТUВИРУЮ ВЗ₽ЫВАТЕЛU, Я НЗНАВИЖУ ВАШУ ВЛАCTb, МНЗ ТЗРЯТЬ Н3Ч3ГО.',
	'Я PYCCKUŪ ПCUXOПAT, U Я ХOЧY COOБЩUTЬ ВАМ К0Е ЧТО. CEГOДNЯ CДETOHUPYET CAМOДEЛЬNAЯ Б0M6A, A TAКЖE ВЗ0РВETCЯ 15 КГ ГEКC0ГENA ПO ГOРOДY ОМСК V T0РГ0ВOМ ЦENTРE "ТЦ". ВСЕ ЧACTU TOРГOВOГO ЦENTРA 3AMUHUPOBAHbl. ECЛИ Bbl ХOTUTE ИЗБEЖATЬ CMEPTU U РA3NOCA BCEГO BAШEГO EБAHH0Г0 ЦENTРA, TO OT3BOHUTECЬ МNE, И Я BAМ ПРЕДОСТАВЛЮ ВСЁ, ЧTO МNE NYЖNO. ЛИЧНОЙ ВCTРEЧU CO МHOŪ HE БYДET. МOŪ NOМEР TEЛЕФONA: {NUMBER}',
	'ЗДРАВСТВУЙТЕ, Я {NAME} ОС0ЗНАЛ ЧТО МЕНЯ HАХYЙ ЗА3БАЛa ЭТА ЖИЗНb, И Я Х0ЧУ УЙТИ КРАСИВ0 В ТОРГ0ВОМ ЦЕНТ₽Е "ТЦ" ЗaЛОЖЕН0 В ТУАЛЕТАХ БОЛЕЕ 230 САМОДЕЛЬНЫХ Б0Мb U ВАC ЕСТЬ РОВН0 30 МИНУТ ЧТОБЫ СКИНУТЬ НА МОЙ СЧЕТ 30.000.000 РУБЛЕЙ ИЛИ ВСЕ ВЗЛЕТИТ НАХУЙ {NUMBER} ВРЕМЯ ПОШЛО',
	'Я {NAME} Был терпилoū на улице, Я решил устроить возмездие. Я za mi/ni-r0\va-l шк0лy НОМЕР 6 города Воронеж. Если вы хотите избежать t/e\r-ak,ta то я жду 100000₽ на мой мобильный номер: {NUMBER}',
]

replacements = {
    "А": "@",
    "О": "0",
    "Е": "3",
    "Т": "T",
    "Н": "H",
    "К": "K",
    "Х": "X",
    "У": "Y",
    "В": "B",
    "М": "M",
    "С": "C",
    "Р": "P",
    "а": "a",
    "е": "e",
    "о": "o",
    "р": "p",
    "с": "$",
    "у": "y",
    "х": "x",
    "к": "k",
    "м": "m",
    "т": "T",
    "н": "H",
    "в": "B",
    "р": "p",
    "е": "e",
    "а": "a",
    "х": "x",
    "у": "y",
    "и": "u",
    "И": "U",
	"ж": "}|{", 
	"Ж": "}|{", 
}

def a(client):

	@client.on(events.NewMessage(pattern=r"\.swat", outgoing=True))
	async def _(event):
		reply = await event.get_reply_message()
		if reply:
			input_text = reply.message
			replaced = "".join(replacements[i] if i in replacements else i for i in input_text)
			await event.edit(f"<b>✉️Текст письма✉️:</b>\n<code>{replaced}</code>",parse_mode='html')
			return
		args =	event.text.split(' ')
		if len(args)<3 or not args[-1].isdigit():
			await event.edit('<b>❌ Использовать с именем и номером! Пример:</b>\n<code>.swat uванов uван 7999999999</code>', parse_mode='html')
			return
		else:
			phone = args[-1]
			name = ' '.join(args[1: -1])
	
			formatted = choice(shablons).format(NAME=name, NUMBER=phone)

			await event.edit(f"<b>✉️Текст письма✉️:</b>\n<code>{formatted}</code>",parse_mode='html')



if __name__ == '__main__':
	try:
		a(client)
	except:
		pass
