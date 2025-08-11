from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.controller_new_buttons import get_back_keyboard, get_staff_activity_filter_keyboard
from utils.language import get_text
from utils.database import get_user_language, get_technicians_activity
from datetime import datetime, timedelta

router = Router()

@router.message(F.text == "👥 Xodimlar faoliyati")
async def handle_staff_activity(message: Message, state: FSMContext):
    """Xodimlar faoliyati handler for controller (faqat texniklar uchun)"""
    lang = await get_user_language(message.from_user.id)
    text = get_text("staff_activity_welcome", lang)
    
    # Show filter options
    keyboard = get_staff_activity_filter_keyboard(lang)
    
    await message.answer(
        text=text,
        reply_markup=keyboard
    )
    await state.set_state("staff_activity")

@router.callback_query(F.data.startswith("staff_"))
async def handle_staff_filter(callback: CallbackQuery, state: FSMContext):
    """Handle staff activity filter selection"""
    lang = await get_user_language(callback.from_user.id)
    filter_type = callback.data.split("_")[1]
    
    # Calculate date range based on filter
    now = datetime.now()
    if filter_type == "today":
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        period_text = get_text("today", lang)
    elif filter_type == "week":
        start_date = now - timedelta(days=7)
        period_text = get_text("this_week", lang)
    elif filter_type == "month":
        start_date = now - timedelta(days=30)
        period_text = get_text("this_month", lang)
    elif filter_type == "all":
        start_date = None
        period_text = get_text("all_time", lang)
    else:
        await callback.answer(get_text("invalid_filter", lang))
        return
    
    # Get technicians activity data
    technicians_data = await get_technicians_activity(start_date)
    
    if not technicians_data:
        text = get_text("no_technician_activity", lang).format(period=period_text)
        await callback.message.edit_text(text, reply_markup=get_back_keyboard(lang))
        await callback.answer()
        return
    
    # Format technicians activity data
    text = get_text("technicians_activity_header", lang).format(period=period_text) + "\n\n"
    
    for tech in technicians_data:
        # Calculate completion rate
        total_tasks = tech.get('total_tasks', 0)
        completed_tasks = tech.get('completed_tasks', 0)
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Calculate average time per task
        avg_time = tech.get('average_time', 'N/A')
        if avg_time and avg_time != 'N/A':
            avg_time_str = str(avg_time).split('.')[0]
        else:
            avg_time_str = get_text("unknown_time", lang)
        
        text += get_text("technician_activity_format", lang).format(
            name=tech.get('name', 'N/A'),
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            completion_rate=f"{completion_rate:.1f}%",
            avg_time=avg_time_str,
            current_task=tech.get('current_task', get_text("no_current_task", lang))
        ) + "\n\n"
    
    # Add back button
    keyboard = get_back_keyboard(lang)
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.message(F.text == "◀️ Orqaga")
async def handle_back(message: Message, state: FSMContext):
    """Back to main menu"""
    from .main_menu import handle_back as main_back
    await main_back(message, state)