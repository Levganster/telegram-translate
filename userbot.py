import asyncio
from telethon import TelegramClient, events
from googletrans import Translator

API_ID = 'your_api_id'
API_HASH = 'your_api_hash'
PHONE_NUMBER = 'your_phone_number'

client = TelegramClient('userbot_session', API_ID, API_HASH)
translator = Translator()

@client.on(events.NewMessage(outgoing=True, pattern='/translate'))
async def handler(event):

    original_text = event.message.message[len('/translate '):]

    translation = translator.translate(original_text, src='ru', dest='en').text

    new_text = f"{original_text}\n\n{translation}"

    await event.delete()
    await event.respond(new_text)

async def main():
    await client.start(phone=PHONE_NUMBER)
    print("Userbot запущен...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())