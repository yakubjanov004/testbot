from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.controllers_buttons import get_back_to_main_menu
from database.models import User
from handlers.controller.realtime_monitoring import show_realtime_monitoring

router = Router()


@router.message(F.text.in_(['🕐 Real vaqtda kuzatish', '🕐 Мониторинг в реальном времени']))
async def realtime_monitoring_handler(message: Message, state: FSMContext, db_session, user: User):
    """Real vaqtda kuzatish"""
    await show_realtime_monitoring(message, state, db_session, user)