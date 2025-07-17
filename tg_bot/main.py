import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Главное меню
main_menu_kb = InlineKeyboardBuilder()
main_menu_kb.button(text="Классифицировать", callback_data="classify")
main_menu_kb.button(text="Выделить текст", callback_data="extract_text")
main_menu_kb.button(text="Демотиватор", callback_data="demotivator")
main_menu_kb.adjust(1)

# Клавиатура выбора модели
model_kb = InlineKeyboardBuilder()
model_kb.button(text="EfficientNet", callback_data="model_efficientnet")
model_kb.button(text="Vision Transformer", callback_data="model_vit")
model_kb.button(text="ResNet", callback_data="model_resnet")
model_kb.adjust(1)

# Состояния пользователя
user_state = {}
user_model = {}

@dp.message(Command("start"))
async def cmd_start(message: Message):
    text = (
        "Добро пожаловать в МемоБот!\n"
        "С помощью бота вы можете определить подходит ли мем для группы про биохимию, выделить текст с фотографии, создать демотиватор"
    )
    await message.answer(text, reply_markup=main_menu_kb.as_markup())

@dp.callback_query(F.data == "classify")
async def classify_menu(callback: CallbackQuery):
    await callback.message.edit_text("Выберите модель:", reply_markup=model_kb.as_markup())
    user_state[callback.from_user.id] = "choose_model"
    await callback.answer()

@dp.callback_query(F.data.startswith("model_"))
async def choose_model(callback: CallbackQuery):
    model = callback.data.replace("model_", "")
    user_model[callback.from_user.id] = model
    user_state[callback.from_user.id] = "awaiting_classify_photo"
    await callback.message.edit_text("Пришлите фотографию для классификации")
    await callback.answer()

@dp.callback_query(F.data == "extract_text")
async def extract_text_menu(callback: CallbackQuery):
    user_state[callback.from_user.id] = "awaiting_text_photo"
    await callback.message.edit_text("Пришлите фотографию для выделения текста")
    await callback.answer()

@dp.callback_query(F.data == "demotivator")
async def demotivator_menu(callback: CallbackQuery):
    user_state[callback.from_user.id] = "awaiting_demotivator_photo"
    await callback.message.edit_text("Пришлите фотографию для создания демотиватора")
    await callback.answer()

@dp.message(F.photo)
async def handle_photo(message: Message):
    state = user_state.get(message.from_user.id)
    if state == "awaiting_classify_photo":
        photo = message.photo[-1]
        file = await bot.get_file(photo.file_id)
        photo_bytes = await bot.download_file(file.file_path)  # Это BytesIO объект
        image = Image.open(photo_bytes)
        try:
            transformed = prepare_photo(image)
            await message.answer("Фото успешно обработано!")
        except Exception as e:
            await message.answer(f"Ошибка обработки фото: {str(e)}")
        await message.answer('"Выберите действие"', reply_markup=main_menu_kb.as_markup())
        user_state[message.from_user.id] = None

    elif state == "awaiting_text_photo":
        await message.answer('"здесь будет ответ с бэкенда"', reply_markup=main_menu_kb.as_markup())
        user_state[message.from_user.id] = None
    elif state == "awaiting_demotivator_photo":
        await message.answer('"здесь будет ответ с бэкенда"', reply_markup=main_menu_kb.as_markup())
        user_state[message.from_user.id] = None
    else:
        await message.answer("Пожалуйста, выберите действие в главном меню.", reply_markup=main_menu_kb.as_markup())

@dp.message()
async def fallback(message: Message):
    await message.answer("Пожалуйста, выберите действие в главном меню.", reply_markup=main_menu_kb.as_markup())

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
