from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.manager_new_buttons import get_back_keyboard, get_priority_keyboard
from utils.language import get_text
from utils.database import get_user_language, create_connection_application

router = Router()

class ConnectionApplicationStates(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_priority = State()
    waiting_for_confirmation = State()

@router.message(F.text == "🔌 Ulanish arizasi yaratish")
async def handle_create_connection(message: Message, state: FSMContext):
    """Ulanish arizasi yaratish handler for manager"""
    lang = await get_user_language(message.from_user.id)
    text = get_text("create_connection_welcome", lang)
    
    await message.answer(
        text=text,
        reply_markup=get_back_keyboard(lang)
    )
    await state.set_state(ConnectionApplicationStates.waiting_for_title)

@router.message(ConnectionApplicationStates.waiting_for_title)
async def handle_title_input(message: Message, state: FSMContext):
    """Handle title input for connection application"""
    lang = await get_user_language(message.from_user.id)
    
    if len(message.text) < 5:
        text = get_text("title_too_short", lang)
        await message.answer(text)
        return
    
    await state.update_data(title=message.text)
    
    text = get_text("enter_connection_description", lang)
    await message.answer(text)
    await state.set_state(ConnectionApplicationStates.waiting_for_description)

@router.message(ConnectionApplicationStates.waiting_for_description)
async def handle_description_input(message: Message, state: FSMContext):
    """Handle description input for connection application"""
    lang = await get_user_language(message.from_user.id)
    
    if len(message.text) < 10:
        text = get_text("description_too_short", lang)
        await message.answer(text)
        return
    
    await state.update_data(description=message.text)
    
    # Show priority selection
    text = get_text("select_priority", lang)
    keyboard = get_priority_keyboard(0, lang)  # 0 as placeholder application_id
    
    await message.answer(text, reply_markup=keyboard)
    await state.set_state(ConnectionApplicationStates.waiting_for_priority)

@router.callback_query(F.data.startswith("priority_"))
async def handle_priority_selection(callback: CallbackQuery, state: FSMContext):
    """Handle priority selection for connection application"""
    lang = await get_user_language(callback.from_user.id)
    priority = callback.data.split("_")[1]
    
    await state.update_data(priority=priority)
    
    # Get all collected data
    data = await state.get_data()
    
    # Show confirmation with all details
    text = get_text("connection_application_summary", lang).format(
        title=data.get('title', 'N/A'),
        description=data.get('description', 'N/A'),
        priority=data.get('priority', 'N/A')
    )
    
    # Add confirmation buttons
    from keyboards.manager_new_buttons import get_confirmation_keyboard
    keyboard = get_confirmation_keyboard("connection_confirm", lang)
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await state.set_state(ConnectionApplicationStates.waiting_for_confirmation)
    await callback.answer()

@router.callback_query(F.data == "connection_confirm_yes")
async def handle_connection_confirmation(callback: CallbackQuery, state: FSMContext):
    """Handle connection application confirmation"""
    lang = await get_user_language(callback.from_user.id)
    
    try:
        # Get all collected data
        data = await state.get_data()
        
        # Create connection application in database
        application_id = await create_connection_application(
            title=data.get('title'),
            description=data.get('description'),
            priority=data.get('priority'),
            created_by=callback.from_user.id
        )
        
        success_text = get_text("connection_application_created", lang).format(id=application_id)
        await callback.message.edit_text(success_text, reply_markup=get_back_keyboard(lang))
        
        await callback.answer()
        await state.clear()
        
    except Exception as e:
        error_text = get_text("connection_creation_error", lang).format(error=str(e))
        await callback.message.edit_text(error_text, reply_markup=get_back_keyboard(lang))
        await callback.answer()

@router.callback_query(F.data == "connection_confirm_no")
async def handle_connection_cancel(callback: CallbackQuery, state: FSMContext):
    """Handle connection application cancellation"""
    lang = await get_user_language(callback.from_user.id)
    
    text = get_text("connection_application_cancelled", lang)
    await callback.message.edit_text(text, reply_markup=get_back_keyboard(lang))
    
    await callback.answer()
    await state.clear()

@router.message(F.text == "◀️ Orqaga")
async def handle_back(message: Message, state: FSMContext):
    """Back to main menu"""
    from .main_menu import handle_back as main_back
    await main_back(message, state)