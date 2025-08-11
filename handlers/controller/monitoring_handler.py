from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.controllers_buttons import get_back_to_main_menu
from database.models import User
from handlers.controller.monitoring import show_monitoring

router = Router()


@router.message(F.text.in_(['📊 Monitoring', '📊 Мониторинг']))
async def monitoring_handler(message: Message, state: FSMContext, db_session, user: User):
    """Monitoring"""
    await show_monitoring(message, state, db_session, user)