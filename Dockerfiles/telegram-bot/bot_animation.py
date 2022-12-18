import yaml
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import asyncio
from aiogram.dispatcher.filters import Text


# WEBAPP_PORT = 3005

with open("config.yaml") as f:
    config_data = yaml.safe_load(f)
bot = Bot(token=config_data["token"])
dp = Dispatcher(bot)


@dp.message_handler()
async def animation_handler(message: 'dfssdfds'):
    data_input = message.text

    upload_message = await bot.send_message(chat_id=message.chat.id, text="Начинаем загрузку...")
    await asyncio.sleep(0.1)
    for i in range(0, 101, 10):
        await upload_message.edit_text(text=f"{i}%")
        await asyncio.sleep(0.2)

    await message.answer("Загрузка заверешена")
    await message.answer("Начинается обработка данных")

    await message.answer("Данные обработаны")


    data_output = data_input
    await message.answer(data_output)
    print('1')


"""
@dp.message_handler()
async def echo_send(message : types.Message):
    data_input = message.text
    data_output = data_input

    await message.answer(data_output)
"""

executor.start_polling(dp, skip_updates=True)
