from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.manager_new_buttons import get_back_keyboard, get_priority_keyboard
from utils.language import get_text
from utils.database import get_user_language, create_technical_service

router = Router()

class TechnicalServiceStates(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_service_type = State()
    waiting_for_priority = State()
    waiting_for_confirmation = State()

@router.message(F.text == "🔧 Texnik xizmat yaratish")
async def handle_create_technical(message: Message, state: FSMContext):
    """Texnik xizmat yaratish handler for manager"""
    lang = await get_user_language(message.from_user.id)
    text = get_text("create_technical_welcome", lang)
    
    await message.answer(
        text=text,
        reply_markup=get_back_keyboard(lang)
    )
    await state.set_state(TechnicalServiceStates.waiting_for_title)

@router.message(TechnicalServiceStates.waiting_for_title)
async def handle_title_input(message: Message, state: FSMContext):
    """Handle title input for technical service"""
    lang = await get_user_language(message.from_user.id)
    
    if len(message.text) < 5:
        text = get_text("title_too_short", lang)
        await message.answer(text)
        return
    
    await state.update_data(title=message.text)
    
    text = get_text("enter_technical_description", lang)
    await message.answer(text)
    await state.set_state(TechnicalServiceStates.waiting_for_description)

@router.message(TechnicalServiceStates.waiting_for_description)
async def handle_description_input(message: Message, state: FSMContext):
    """Handle description input for technical service"""
    lang = await get_user_language(message.from_user.id)
    
    if len(message.text) < 10:
        text = get_text("description_too_short", lang)
        await message.answer(text)
        return
    
    await state.update_data(description=message.text)
    
    # Show service type selection
    text = get_text("select_service_type", lang)
    service_types = [
        "🔧 Texnik xizmat",
        "🛠️ Ta'mirlash",
        "⚡ Elektr ta'minot",
        "🌐 Internet aloqa",
        "📱 Telefon aloqa"
    ]
    
    from keyboards.manager_new_buttons import InlineKeyboardBuilder, InlineKeyboardButton
    builder = InlineKeyboardBuilder()
    
    for service_type in service_types:
        builder.add(InlineKeyboardButton(
            text=service_type,
            callback_data=f"service_type_{service_type.replace(' ', '_').lower()}"
        ))
    
    builder.adjust(1)  # 1 button per row
    
    await message.answer(text, reply_markup=builder.as_markup())
    await state.set_state(TechnicalServiceStates.waiting_for_service_type)

@router.callback_query(F.data.startswith("service_type_"))
async def handle_service_type_selection(callback: CallbackQuery, state: FSMContext):
    """Handle service type selection for technical service"""
    lang = await get_user_language(callback.from_user.id)
    service_type = callback.data.split("service_type_")[1].replace('_', ' ')
    
    await state.update_data(service_type=service_type)
    
    # Show priority selection
    text = get_text("select_priority", lang)
    keyboard = get_priority_keyboard(0, lang)  # 0 as placeholder application_id
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await state.set_state(TechnicalServiceStates.waiting_for_priority)
    await callback.answer()

@router.callback_query(F.data.startswith("priority_"))
async def handle_priority_selection(callback: CallbackQuery, state: FSMContext):
    """Handle priority selection for technical service"""
    lang = await get_user_language(callback.from_user.id)
    priority = callback.data.split("_")[1]
    
    await state.update_data(priority=priority)
    
    # Get all collected data
    data = await state.get_data()
    
    # Show confirmation with all details
    text = get_text("technical_service_summary", lang).format(
        title=data.get('title', 'N/A'),
        description=data.get('description', 'N/A'),
        service_type=data.get('service_type', 'N/A'),
        priority=data.get('priority', 'N/A')
    )
    
    # Add confirmation buttons
    from keyboards.manager_new_buttons import get_confirmation_keyboard
    keyboard = get_confirmation_keyboard("technical_confirm", lang)
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await state.set_state(TechnicalServiceStates.waiting_for_confirmation)
    await callback.answer()

@router.callback_query(F.data == "technical_confirm_yes")
async def handle_technical_confirmation(callback: CallbackQuery, state: FSMContext):
    """Handle technical service confirmation"""
    lang = await get_user_language(callback.from_user.id)
    
    try:
        # Get all collected data
        data = await state.get_data()
        
        # Create technical service in database
        service_id = await create_technical_service(
            title=data.get('title'),
            description=data.get('description'),
            service_type=data.get('service_type'),
            priority=data.get('priority'),
            created_by=callback.from_user.id
        )
        
        success_text = get_text("technical_service_created", lang).format(id=service_id)
        await callback.message.edit_text(success_text, reply_markup=get_back_keyboard(lang))
        
        await callback.answer()
        await state.clear()
        
    except Exception as e:
        error_text = get_text("technical_service_creation_error", lang).format(error=str(e))
        await callback.message.edit_text(error_text, reply_markup=get_back_keyboard(lang))
        await callback.answer()

@router.callback_query(F.data == "technical_confirm_no")
async def handle_technical_cancel(callback: CallbackQuery, state: FSMContext):
    """Handle technical service cancellation"""
    lang = await get_user_language(callback.from_user.id)
    
    text = get_text("technical_service_cancelled", lang)
    await callback.message.edit_text(text, reply_markup=get_back_keyboard(lang))
    
    await callback.answer()
    await state.clear()

@router.message(F.text == "◀️ Orqaga")
async def handle_back(message: Message, state: FSMContext):
    """Back to main menu"""
    from .main_menu import handle_back as main_back
    await main_back(message, state)