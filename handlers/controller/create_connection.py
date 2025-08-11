from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.controllers_buttons import get_back_to_main_menu
from database.models import User
from handlers.controller.staff_application_creation import start_connection_creation

router = Router()


@router.message(F.text.in_(['🔌 Ulanish arizasi yaratish', '🔌 Создать заявку на подключение']))
async def create_connection_handler(message: Message, state: FSMContext, db_session, user: User):
    """Ulanish arizasi yaratish"""
    await start_connection_creation(message, state, db_session, user)