from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.controller_new_buttons import get_back_keyboard, get_realtime_refresh_keyboard
from utils.language import get_text
from utils.database import get_user_language, get_realtime_applications
from datetime import datetime, timedelta

router = Router()

@router.message(F.text == "🕐 Real vaqtda kuzatish")
async def handle_realtime_monitoring(message: Message, state: FSMContext):
    """Real vaqtda kuzatish handler for controller"""
    lang = await get_user_language(message.from_user.id)
    
    # Get realtime applications data
    applications = await get_realtime_applications()
    
    if not applications:
        text = get_text("no_realtime_data", lang)
        await message.answer(text, reply_markup=get_back_keyboard(lang))
        return
    
    # Format realtime data
    text = get_text("realtime_monitoring_header", lang) + "\n\n"
    
    for app in applications:
        # Calculate elapsed time
        start_time = app.get('start_time')
        if start_time:
            elapsed = datetime.now() - start_time
            elapsed_str = str(elapsed).split('.')[0]  # Remove microseconds
        else:
            elapsed_str = get_text("unknown_time", lang)
        
        # Get assigned technician
        technician = app.get('technician_name', get_text("unassigned", lang))
        
        text += get_text("realtime_application_format", lang).format(
            id=app.get('id', 'N/A'),
            title=app.get('title', 'N/A'),
            technician=technician,
            elapsed=elapsed_str,
            status=app.get('status', 'N/A')
        ) + "\n\n"
    
    # Add refresh button
    keyboard = get_realtime_refresh_keyboard(lang)
    
    await message.answer(text, reply_markup=keyboard)
    await state.set_state("realtime_monitoring")

@router.callback_query(F.data == "realtime_refresh")
async def handle_refresh(callback: CallbackQuery, state: FSMContext):
    """Refresh realtime monitoring data"""
    lang = await get_user_language(callback.from_user.id)
    
    # Get updated realtime data
    applications = await get_realtime_applications()
    
    if not applications:
        text = get_text("no_realtime_data", lang)
        await callback.message.edit_text(text, reply_markup=get_back_keyboard(lang))
        await callback.answer()
        return
    
    # Format updated data
    text = get_text("realtime_monitoring_header", lang) + "\n\n"
    
    for app in applications:
        start_time = app.get('start_time')
        if start_time:
            elapsed = datetime.now() - start_time
            elapsed_str = str(elapsed).split('.')[0]
        else:
            elapsed_str = get_text("unknown_time", lang)
        
        technician = app.get('technician_name', get_text("unassigned", lang))
        
        text += get_text("realtime_application_format", lang).format(
            id=app.get('id', 'N/A'),
            title=app.get('title', 'N/A'),
            technician=technician,
            elapsed=elapsed_str,
            status=app.get('status', 'N/A')
        ) + "\n\n"
    
    keyboard = get_realtime_refresh_keyboard(lang)
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "realtime_back")
async def handle_realtime_back(callback: CallbackQuery, state: FSMContext):
    """Back from realtime monitoring"""
    from .main_menu import handle_back as main_back
    await main_back(callback.message, state)
    await callback.answer()

@router.message(F.text == "◀️ Orqaga")
async def handle_back(message: Message, state: FSMContext):
    """Back to main menu"""
    from .main_menu import handle_back as main_back
    await main_back(message, state)