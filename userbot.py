import asyncio
from telethon import TelegramClient, events
from googletrans import Translator
import json

API_ID = 'введите API ID'
API_HASH = 'введите API HASH'
PHONE_NUMBER = 'введите номер телефона'

client = TelegramClient('userbot_session', API_ID, API_HASH)
translator = Translator()

@client.on(events.NewMessage(outgoing=True, pattern=r'/help'))
async def handler(event):
    help_text = (
        '/te <язык> <текст> - перевести текст на указанный язык и изменить сообщение\n'
        '/td <язык> <текст> - перевести текст на указанный язык, удалить прошлое сообщение и отправить новое\n'
        '/set - показать текущие настройки\n'
        '/set <номер параметра> <значение> - установить параметр\n'
        '/help - показать это сообщение\n'
        '/langs - показать доступные языковые коды'
    )
    await event.edit(help_text)

@client.on(events.NewMessage(outgoing=True, pattern=r'/langs'))
async def handler(event):
    languages = {
        'af': 'Африкаанс',
        'sq': 'Албанский',
        'ar': 'Арабский',
        'hy': 'Армянский',
        'bn': 'Бенгальский',
        'bs': 'Боснийский',
        'ca': 'Каталонский',
        'hr': 'Хорватский',
        'cs': 'Чешский',
        'da': 'Датский',
        'nl': 'Нидерландский',
        'en': 'Английский',
        'eo': 'Эсперанто',
        'et': 'Эстонский',
        'tl': 'Филиппинский',
        'fi': 'Финский',
        'fr': 'Французский',
        'de': 'Немецкий',
        'el': 'Греческий',
        'gu': 'Гуджарати',
        'ht': 'Гаитянский',
        'ha': 'Хауса',
        'haw': 'Гавайский',
        'hi': 'Хинди',
        'hu': 'Венгерский',
        'is': 'Исландский',
        'ig': 'Игбо',
        'id': 'Индонезийский',
        'ga': 'Ирландский',
        'it': 'Итальянский',
        'ja': 'Японский',
        'jw': 'Яванский',
        'kn': 'Каннада',
        'kk': 'Казахский',
        'km': 'Кхмерский',
        'ko': 'Корейский',
        'la': 'Латинский',
        'lv': 'Латышский',
        'lt': 'Литовский',
        'lb': 'Люксембургский',
        'mk': 'Македонский',
        'ml': 'Малаялам',
        'mn': 'Монгольский',
        'mr': 'Маратхи',
        'my': 'Бирманский',
        'ne': 'Непальский',
        'no': 'Норвежский',
        'pl': 'Польский',
        'pt': 'Португальский',
        'pa': 'Панджаби',
        'ro': 'Румынский',
        'ru': 'Русский',
        'sr': 'Сербский',
        'si': 'Сингальский',
        'sk': 'Словацкий',
        'sl': 'Словенский',
        'es': 'Испанский',
        'su': 'Сунданский',
        'sw': 'Суахили',
        'sv': 'Шведский',
        'ta': 'Тамильский',
        'te': 'Телугу',
        'th': 'Тайский',
        'tr': 'Турецкий',
        'uk': 'Украинский',
        'ur': 'Урду',
        'vi': 'Вьетнамский',
        'cy': 'Валлийский',
        'xh': 'Ксоса',
        'yi': 'Идиш',
        'yo': 'Йоруба',
        'zu': 'Зулу'
    }
    
    lang_list = "\n".join([f"{code}: {name}" for code, name in languages.items()])
    await event.edit(f"Доступные языковые коды:\n{lang_list}")

with open('settings.json', 'r', encoding='utf-8') as f:
    settings = json.load(f)

@client.on(events.NewMessage(outgoing=True, pattern=r'/set'))
async def handler(event):
    message_parts = event.message.message.split(' ', 2)
    
    if len(message_parts) == 1:
        await event.edit(f'Текущие настройки:\n1. Добавлять оригинальное сообщение: {settings["add_original_message"]}\n2. Капитализация первой буквы: {settings["capitalize_first_letter"]}\n3. Язык оригинального сообщения: {settings["original_language"]}')
        return

    name = message_parts[1]
    param = message_parts[2]

    if name == '1':
        settings['add_original_message'] = param == 'true'
    elif name == '2':
        settings['capitalize_first_letter'] = param == 'true'
    elif name == '3':
        settings['original_language'] = param

    with open('settings.json', 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=4)

    await event.edit(f'Настройки сохранены:\n1. Добавлять оригинальное сообщение: {settings["add_original_message"]}\n2. Капитализация первой буквы: {settings["capitalize_first_letter"]}\n3. Язык оригинального сообщения: {settings["original_language"]}')

@client.on(events.NewMessage(outgoing=True, pattern=r'/te (\w{2})'))
async def handler(event):
    message_parts = event.message.message.split(' ', 2)
    dest_lang = message_parts[1]
    original_text = message_parts[2]

    translation = translator.translate(original_text, src=settings['original_language'], dest=dest_lang).text

    if settings['capitalize_first_letter']:
        original_text = original_text.capitalize()
        translation = translation.capitalize()
        
    new_text = original_text
    if settings['add_original_message']:
        new_text += f"\n\n{translation}"
    else:
        new_text = translation

    await event.edit(new_text)

@client.on(events.NewMessage(outgoing=True, pattern=r'/td (\w{2})'))
async def handler(event):
    message_parts = event.message.message.split(' ', 2)
    dest_lang = message_parts[1]
    original_text = message_parts[2]

    translation = translator.translate(original_text, src=settings['original_language'], dest=dest_lang).text

    if settings['capitalize_first_letter']:
        original_text = original_text.capitalize()
        translation = translation.capitalize()

    new_text = original_text
    if settings['add_original_message']:
        new_text += f"\n\n{translation}"
    else:
        new_text = translation

    await event.delete()
    await event.respond(new_text)

async def main():
    await client.start(phone=PHONE_NUMBER)
    print("Userbot запущен...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
