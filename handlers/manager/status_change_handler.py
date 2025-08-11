from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.manager_buttons import get_back_to_main_menu
from database.models import User
from handlers.manager.status_management import show_status_management

router = Router()


@router.message(F.text.in_(['🔄 Status o\'zgartirish', '🔄 Изменить статус']))
async def status_change_handler(message: Message, state: FSMContext, db_session, user: User):
    """Status o'zgartirish"""
    await show_status_management(message, state, db_session, user)