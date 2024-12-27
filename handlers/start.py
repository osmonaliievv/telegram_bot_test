from aiogram import Router, F, types
from aiogram.filters import Command

start_router = Router()


@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Оставить отзыв", callback_data="review"),
            ],
        ]
    )
    await message.answer(
        "Здравствуйте! \n"
        "Я ваш виртуальный помощник и готов помочь:\n"
        "- Принять вашу жалобу.\n"
        "- Передать информацию ответственным специалистам.\n"
        "- Ответить на ваши вопросы. ",
        reply_markup=kb
    )
