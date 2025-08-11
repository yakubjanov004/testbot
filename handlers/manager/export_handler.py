from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.manager_buttons import get_back_to_main_menu
from database.models import User
from handlers.manager.export import show_export

router = Router()


@router.message(F.text.in_(['📤 Export', '📤 Экспорт']))
async def export_handler(message: Message, state: FSMContext, db_session, user: User):
    """Export"""
    await show_export(message, state, db_session, user)