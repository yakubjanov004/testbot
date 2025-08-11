from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.manager_buttons import get_back_to_main_menu
from database.models import User
from handlers.manager.inbox import show_inbox

router = Router()


@router.message(F.text.in_(['📥 Inbox', '📥 Входящие']))
async def inbox_handler(message: Message, state: FSMContext, db_session, user: User):
    """Inbox handler"""
    await show_inbox(message, state, db_session, user)