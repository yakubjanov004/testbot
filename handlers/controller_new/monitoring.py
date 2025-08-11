from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.controller_new_buttons import get_back_keyboard
from utils.language import get_text
from utils.database import get_user_language, get_monitoring_data
from datetime import datetime, timedelta

router = Router()

@router.message(F.text == "📊 Monitoring")
async def handle_monitoring(message: Message, state: FSMContext):
    """Monitoring handler for controller (avvalgisi kabi)"""
    lang = await get_user_language(message.from_user.id)
    
    # Get monitoring data
    monitoring_data = await get_monitoring_data()
    
    if not monitoring_data:
        text = get_text("no_monitoring_data", lang)
        await message.answer(text, reply_markup=get_back_keyboard(lang))
        return
    
    # Format monitoring data
    text = get_text("monitoring_header", lang) + "\n\n"
    
    # Overall statistics
    total_applications = monitoring_data.get('total_applications', 0)
    completed_applications = monitoring_data.get('completed_applications', 0)
    pending_applications = monitoring_data.get('pending_applications', 0)
    in_progress_applications = monitoring_data.get('in_progress_applications', 0)
    
    text += get_text("monitoring_overview", lang).format(
        total=total_applications,
        completed=completed_applications,
        pending=pending_applications,
        in_progress=in_progress_applications
    ) + "\n\n"
    
    # Performance metrics
    avg_completion_time = monitoring_data.get('average_completion_time', 'N/A')
    if avg_completion_time and avg_completion_time != 'N/A':
        avg_time_str = str(avg_completion_time).split('.')[0]
    else:
        avg_time_str = get_text("unknown_time", lang)
    
    text += get_text("monitoring_performance", lang).format(
        avg_completion_time=avg_time_str,
        success_rate=f"{monitoring_data.get('success_rate', 0):.1f}%"
    ) + "\n\n"
    
    # Recent activity
    recent_activities = monitoring_data.get('recent_activities', [])
    if recent_activities:
        text += get_text("monitoring_recent_activity", lang) + "\n"
        for activity in recent_activities[:5]:  # Show last 5 activities
            text += get_text("monitoring_activity_format", lang).format(
                time=activity.get('time', 'N/A'),
                action=activity.get('action', 'N/A'),
                user=activity.get('user', 'N/A')
            ) + "\n"
    
    # Add back button
    keyboard = get_back_keyboard(lang)
    
    await message.answer(text, reply_markup=keyboard)
    await state.set_state("monitoring")

@router.message(F.text == "◀️ Orqaga")
async def handle_back(message: Message, state: FSMContext):
    """Back to main menu"""
    from .main_menu import handle_back as main_back
    await main_back(message, state)