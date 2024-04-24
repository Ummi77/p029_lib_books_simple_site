
## ~ https://www.pythonanywhere.com/forums/topic/33464/


# from telebot import apihelper
# apihelper.API_URL = 'http://0.0.0.0:8081/bot'
# apihelper.FILE_URL = 'http://0.0.0.0:8081'



# def log_out_function():
#     return bot.log_out()




import asyncio
import logging
import sys
from os import getenv

import os

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from aiogram.types import FSInputFile

os.environ["BOT_TOKEN"] = '6982698935:AAFQQdz8uApzejMak2ily8azWVKytfIeuNQ'

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("BOT_TOKEN")

print(f"PR_A600 --> TOKEN = {TOKEN}")

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")
        
        
        
# async def send_file() -> None:
#     """
#     This handler receives messages with `/start` command
#     """
#     # Most event objects have aliases for API methods that can be called in events' context
#     # For example if you want to answer to incoming message you can use `message.answer(...)` alias
#     # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
#     # method automatically or call API method directly via
#     # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
#     await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")
        
        
        


async def main() -> None:
    """ 
    Отправка файла mp3 из локального директория в ТГ чат
    """
    
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN,parse_mode=ParseMode.HTML)
    # And the run events dispatching
    # await dp.start_polling(bot)
    
    fileRoot = '/media/ak/Transcend1/GENERAL_ARCHIVE_EXTERNAL_DISC_FROM_01_02_2024_CURRENT_MAIN/TELEGRAM_AUDIO_LIBRARIES/CHANNEL_ID_1'

    # fileName = '19. ждем книгу.mp3'
    fileName = '3. Эндшпиль.mp3' # > 50Mb
    
    bot.log_out()
    
    
    fileFullPath = f"{fileRoot}/{fileName}"
    
    chatid = -1001811098741
    
    
    
    # await bot.send_document(user_id, open(fileFullPath, 'rb'))
    
    # Отправка файла mp3 из локального директория в ТГ чат
    document = FSInputFile(fileFullPath)
    await bot.send_document(chatid, document)
    
    
    
    
    
    
    
    
    
    
async def send_document_file_message_by_file_id() -> None:
    """ 
    Отправка файла mp3 из локального директория в ТГ чат
    """
    
    
    
    # # ПРОРАБОТКА: Отправка файла mp3 из локального директория в ТГ чат
    
    # # Initialize Bot instance with a default parse mode which will be passed to all API calls
    # bot = Bot(TOKEN,  parse_mode=ParseMode.HTML)
    # # And the run events dispatching
    # # await dp.start_polling(bot)
    
    
    
    
    # fileRoot = '/media/ak/Transcend1/GENERAL_ARCHIVE_EXTERNAL_DISC_FROM_01_02_2024_CURRENT_MAIN/TELEGRAM_AUDIO_LIBRARIES/CHANNEL_ID_1'

    # # fileName = '19. ждем книгу.mp3'
    # fileName = '3. Endshpil.mp3' # > 50Mb
    
    
    
    
    # fileFullPath = f"{fileRoot}/{fileName}"
    
    # chatid = -1001811098741
    
    
    
    # # await bot.send_document(user_id, open(fileFullPath, 'rb'))
    
    # # Отправка файла mp3 из локального директория в ТГ чат
    # document = FSInputFile(fileFullPath)
    # await bot.send_document(chatid, document)
    
    
    
    
    
    
    
    # ПРОРАБОТКА: Отправка файла mp3 из уже загруженного на 'me' в чат Аудиокниг
    
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    # await dp.start_polling(bot)
    
    
    # await bot.log_out()
    
    chatid = -1001811098741
    
    file_id ="BQADAgAD3EIAAqEh-UpvjOwAAdL--_8C"
    
    f = await bot.get_file('BQADAgAD3EIAAqEh-UpvjOwAAdL--_8C')
    
    
    # await bot.api.sendAudio(chatid, file_id)

    # await bot.send_document(user_id, open(fileFullPath, 'rb'))
    
    # result: Message = await bot.send_audio(chatid, file_id)
    
    print(f"PR_A602 --> result = {f}")
            
            
            


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(send_document_file_message_by_file_id())










