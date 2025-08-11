from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.controllers_buttons import get_controller_main_menu
from database.models import User

router = Router()


@router.message(F.text.in_(['🏠 Asosiy menyu', '🏠 Главное меню']))
async def back_to_main_menu(message: Message, state: FSMContext, db_session, user: User):
    """Asosiy menyuga qaytish"""
    await state.clear()
    lang = user.language if user else 'uz'
    
    text = {
        'uz': "📋 Asosiy menyu",
        'ru': "📋 Главное меню"
    }
    
    await message.answer(
        text.get(lang, text['uz']),
        reply_markup=get_controller_main_menu(lang)
    )


@router.message(F.text == '/start')
async def start_command(message: Message, state: FSMContext, db_session, user: User):
    """Start komandasi"""
    await state.clear()
    lang = user.language if user else 'uz'
    
    text = {
        'uz': f"Assalomu alaykum, {user.full_name}!\nController paneliga xush kelibsiz!",
        'ru': f"Здравствуйте, {user.full_name}!\nДобро пожаловать в панель контроллера!"
    }
    
    await message.answer(
        text.get(lang, text['uz']),
        reply_markup=get_controller_main_menu(lang)
    )
