from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.controller_new_buttons import get_back_keyboard, get_language_keyboard
from utils.language import get_text
from utils.database import get_user_language, update_user_language

router = Router()

@router.message(F.text == "🌐 Tilni o'zgartirish")
async def handle_language_change(message: Message, state: FSMContext):
    """Tilni o'zgartirish handler for controller"""
    lang = await get_user_language(message.from_user.id)
    text = get_text("language_change_welcome", lang)
    
    # Show language selection options
    keyboard = get_language_keyboard(lang)
    
    await message.answer(
        text=text,
        reply_markup=keyboard
    )
    await state.set_state("language_change")

@router.callback_query(F.data.startswith("lang_"))
async def handle_language_selection(callback: CallbackQuery, state: FSMContext):
    """Handle language selection"""
    lang = await get_user_language(callback.from_user.id)
    selected_language = callback.data.split("_")[1]
    
    try:
        # Update user language in database
        await update_user_language(callback.from_user.id, selected_language)
        
        # Get text in new language
        success_text = get_text("language_changed_success", selected_language)
        
        await callback.message.edit_text(
            success_text,
            reply_markup=get_back_keyboard(selected_language)
        )
        
        await callback.answer()
        
    except Exception as e:
        error_text = get_text("language_change_error", lang).format(error=str(e))
        await callback.message.edit_text(
            error_text,
            reply_markup=get_back_keyboard(lang)
        )
        await callback.answer()

@router.message(F.text == "◀️ Orqaga")
async def handle_back(message: Message, state: FSMContext):
    """Back to main menu"""
    from .main_menu import handle_back as main_back
    await main_back(message, state)