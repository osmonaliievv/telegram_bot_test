from aiogram import Router, F, types
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.context import FSMContext

from bot_config import database

review_router = Router()


class ComplaintProcess(StatesGroup):
    name = State()
    contact = State()
    complaint = State()


def validate_name(name: str) -> bool:
    return 1 <= len(name) <= 50


@review_router.callback_query(F.data == "review", default_state)
async def start_complaint(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Как вас зовут?")
    await state.set_state(ComplaintProcess.name)


@review_router.message(ComplaintProcess.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    if not validate_name(name):
        await message.answer("Имя должно быть от 1 до 50 символов.")
        return
    await state.update_data(name=name)
    await message.answer("Ваш номер телефона или инстаграмм?")
    await state.set_state(ComplaintProcess.contact)


@review_router.message(ComplaintProcess.contact)
async def process_contact(message: types.Message, state: FSMContext):
    contact = message.text
    await state.update_data(contact=contact)
    await message.answer("Опишите вашу жалобу:")
    await state.set_state(ComplaintProcess.complaint)


@review_router.message(ComplaintProcess.complaint)
async def process_complaint(message: types.Message, state: FSMContext):
    complaint = message.text
    await state.update_data(complaint=complaint)
    data = await state.get_data()
    summary = (
        f"Спасибо за ваше обращение!!!\n"
        f"Имя: {data.get('name')}\n"
        f"Контакт: {data.get('contact')}\n"
        f"Жалоба: {data.get('complaint')}"
    )
    try:
        (database.save_complaints(data))
        await message.answer("Ваш отзыв сохранён!")
    except Exception as e:
        await message.answer(f"Ошибка сохранения отзыва: {e}")
    await message.answer(summary)
    await state.clear()
