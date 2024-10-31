import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F
from aiogram import Router
from config import TOKEN

# Инициализация бота
bot = Bot(token=TOKEN)
router = Router()

# Логирование
logging.basicConfig(level=logging.INFO)

# Функция для создания инлайн-клавиатуры
def get_main_keyboard():
    # Создаем инлайн-кнопки
    button_start = InlineKeyboardButton(text="🟢 Привет!", callback_data="greet")
    button_exit = InlineKeyboardButton(text="🟢 Пока", callback_data="exit")
    button_dynamic = InlineKeyboardButton(text="🟢 Динамическое меню", callback_data="dynamic_menu")
    button_news = InlineKeyboardButton(text="📰 Новости", url="https://www.rbc.ru")
    button_music = InlineKeyboardButton(text="🎵 Музыка", url="https://zvuk.com/?ysclid=m2x2ua6nvl182333032")
    button_video = InlineKeyboardButton(text="🎥 Видео", url="https://vk.com/video?ysclid=m2x2xciode192627501")

    # Создаем инлайн-клавиатуру и добавляем кнопки
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [button_start],
        [button_exit],
        [button_dynamic],
        [button_news, button_music, button_video]
    ])
    return keyboard

# Функция для создания инлайн-клавиатуры с опциями
def get_dynamic_keyboard():
    button_option1 = InlineKeyboardButton(text="Опция 1", callback_data="option1")
    button_option2 = InlineKeyboardButton(text="Опция 2", callback_data="option2")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [button_option1, button_option2]
    ])
    return keyboard

# Обработчик команды /start
@router.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer(
        "Выберите действие:",
        reply_markup=get_main_keyboard()
    )

# Обработчик команды /dynamic
@router.message(Command('dynamic'))
async def dynamic_command(message: types.Message):
    await message.answer(
        "Нажмите кнопку, чтобы показать больше опций:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Показать больше", callback_data="show_more")]
        ])
    )

# Обработчик нажатия инлайн-кнопок
@router.callback_query(F.data == "greet")
async def greet_command(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(f"Привет, {callback.from_user.first_name}!", reply_markup=get_main_keyboard())

@router.callback_query(F.data == "exit")
async def exit_command(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(f"До свидания, {callback.from_user.first_name}!", reply_markup=get_main_keyboard())

@router.callback_query(F.data == "dynamic_menu")
async def dynamic_menu_command(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("Нажмите кнопку, чтобы показать больше опций:",
                                  reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                      [InlineKeyboardButton(text="Показать больше", callback_data="show_more")]
                                  ]))

@router.callback_query(F.data == "show_more")
async def show_more_command(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("Выберите опцию:",
                                  reply_markup=get_dynamic_keyboard())

@router.callback_query(F.data == "option1")
async def option1_command(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("Это пример текста сообщения Опции 1.", reply_markup=get_main_keyboard())

@router.callback_query(F.data == "option2")
async def option2_command(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("Это пример текста сообщения Опции 2.", reply_markup=get_main_keyboard())

# Создаем и регистрируем диспетчер
dp = Dispatcher()
dp.include_router(router)

# Запуск бота
if __name__ == '__main__':
    logging.info("Бот запущен и готов к приему команд.")
    dp.run_polling(bot, skip_updates=True)
