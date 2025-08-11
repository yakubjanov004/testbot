from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.controllers_buttons import get_back_to_main_menu
from database.models import User
from handlers.controller.language import show_language_settings

router = Router()


@router.message(F.text.in_(['🌐 Tilni o\'zgartirish', '🌐 Изменить язык']))
async def language_handler(message: Message, state: FSMContext, db_session, user: User):
    """Tilni o'zgartirish"""
    await show_language_settings(message, state, db_session, user)