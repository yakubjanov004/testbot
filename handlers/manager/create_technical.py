from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.manager_buttons import get_back_to_main_menu
from database.models import User
from handlers.manager.staff_application_creation import start_technical_creation

router = Router()


@router.message(F.text.in_(['🔧 Texnik xizmat yaratish', '🔧 Создать техническое обслуживание']))
async def create_technical_handler(message: Message, state: FSMContext, db_session, user: User):
    """Texnik xizmat arizasi yaratish"""
    await start_technical_creation(message, state, db_session, user)