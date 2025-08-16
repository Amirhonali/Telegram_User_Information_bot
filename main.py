from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
TOKEN = ""

bot = Bot(token=TOKEN)
dp = Dispatcher()
chanal = ""

user_data = {}

@dp.message()
async def handle_message(message: types.Message):
    print("Handle_message")
    user_id = message.from_user.id
    if message.text == "/start":
        await start(message)
    elif 'name' not in user_data[user_id]:
        await phone(message)
    elif 'phone' not in user_data[user_id]:
        await age(message)
    elif 'age' not in user_data[user_id]:
        await send(message)
    elif 'age' in user_data[user_id]:
        await check_user(message)


async def start(message: types.Message):
    print("start")
    user_id = message.from_user.id
    user_data[user_id] = {}
    await message.answer("Assalomu alekum! Ismingizni kriting: ")


async def phone(message: types.Message):
    print("phone")
    user_id = message.from_user.id
    name = message.text
    user_data[user_id]['name'] = name
    print("Name: ", name)
    button = [
        [types.KeyboardButton(text="Share Contact", request_contact=True)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True, one_time_keyboard=True)
    await message.answer("Telefon raqamingizni kriting: ", reply_markup=keyboard)

async def age(message: types.Message):
    print("age")
    user_id = message.from_user.id
    if message.contact is not None:
        phone = message.contact.phone_number
        user_data[user_id]['phone'] = phone
        print("Phone: ", phone)
        await message.answer("Yoshingizni kriting: ")
    else:
        await message.answer("Tugmani bosib kontaktingizni jonatishingizni soraymiz!!!")


async def send(message: types.Message):
    print("send")
    user_id = message.from_user.id
    age = message.text
    user_data[user_id]['age'] = age
    print("Age: ", age)
    total = (f"Ism: {user_data[user_id]['name']}\n"
             f"Phone: +{user_data[user_id]['phone']}\n"
             f"Age: {user_data[user_id]['age']}\n")

    buttons = [
        [types.KeyboardButton(text="Ha")],
        [types.KeyboardButton(text="Yoq")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
    await message.answer(total)
    await message.answer("Tasdiqlaysizmi?", reply_markup=keyboard)


async def check_user(message: types.Message):
    print("check_user")
    user_id = message.from_user.id
    total = (f"Ism: {user_data[user_id]['name']}\n"
             f"Phone: +{user_data[user_id]['phone']}\n"
             f"Age: {user_data[user_id]['age']}\n")
    if message.text == "Ha":
        await bot.send_message(chanal, f"NEW USER!!!\n{total}")
        await message.answer("Siz haqingizda yozib oldik!!!")
    else:
        await start(message)


async def main():
    await dp.start_polling(bot)

print("Bot is running... ")
asyncio.run(main())
