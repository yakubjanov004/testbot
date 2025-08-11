from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.manager_new_buttons import get_back_keyboard, get_staff_activity_filter_keyboard
from utils.language import get_text
from utils.database import get_user_language, get_junior_managers_activity
from datetime import datetime, timedelta

router = Router()

@router.message(F.text == "👥 Xodimlar faoliyati")
async def handle_staff_activity(message: Message, state: FSMContext):
    """Xodimlar faoliyati handler (faqat kichik menejerlar uchun)"""
    lang = await get_user_language(message.from_user.id)
    user_id = message.from_user.id
    
    # Kichik menejerlar faoliyatini olish (bugungi)
    today = datetime.now().date()
    staff_data = await get_junior_managers_activity(user_id, today)
    
    if not staff_data:
        text = get_text("staff_activity_no_data", lang)
        await message.answer(text, reply_markup=get_back_keyboard(lang))
        return
    
    # Faoliyat ma'lumotlarini ko'rsatish
    text = get_text("staff_activity_welcome", lang)
    text += f"\n\n{get_text('period', lang)}: {get_text('today', lang)}"
    text += f"\n{get_text('total_junior_managers', lang)}: {len(staff_data)}"
    
    # Har bir kichik menejer uchun faoliyat
    for staff in staff_data:
        activity_emoji = "🟢" if staff.get('active_applications', 0) > 0 else "🔴"
        efficiency = staff.get('efficiency', 0)
        efficiency_emoji = "🟢" if efficiency >= 80 else "🟡" if efficiency >= 60 else "🔴"
        
        text += f"\n\n{activity_emoji} {staff['full_name']}"
        text += f"\n{get_text('active_applications', lang)}: {staff.get('active_applications', 0)}"
        text += f"\n{get_text('completed_today', lang)}: {staff.get('completed_today', 0)}"
        text += f"\n{get_text('efficiency', lang)}: {efficiency_emoji} {efficiency}%"
        text += f"\n{get_text('last_activity', lang)}: {staff.get('last_activity', 'N/A')}"
        
        # Ish vaqti
        work_hours = staff.get('work_hours', 0)
        if work_hours > 0:
            text += f"\n{get_text('work_hours', lang)}: {work_hours}h"
    
    # Filter keyboard
    filter_kb = get_staff_activity_filter_keyboard(lang)
    
    await message.answer(
        text=text,
        reply_markup=filter_kb
    )
    
    # State'ga ma'lumotlarni saqlash
    await state.update_data({
        'staff_data': staff_data,
        'current_period': 'today',
        'current_date': today
    })

@router.callback_query(F.data.startswith("staff_"))
async def handle_staff_filter(callback: CallbackQuery, state: FSMContext):
    """Xodimlar faoliyati filtri handler"""
    period = callback.data.split("_")[1]  # today, week, month, all
    lang = await get_user_language(callback.from_user.id)
    user_id = callback.from_user.id
    
    await callback.answer(get_text("loading", lang))
    
    # Period bo'yicha ma'lumotlarni olish
    if period == "today":
        date = datetime.now().date()
        period_text = get_text('today', lang)
    elif period == "week":
        date = datetime.now().date() - timedelta(days=7)
        period_text = get_text('week', lang)
    elif period == "month":
        date = datetime.now().date() - timedelta(days=30)
        period_text = get_text('month', lang)
    elif period == "all":
        date = None
        period_text = get_text('all', lang)
    else:
        await callback.answer(get_text("invalid_period", lang))
        return
    
    # Kichik menejerlar faoliyatini olish
    staff_data = await get_junior_managers_activity(user_id, date)
    
    if not staff_data:
        text = get_text("staff_activity_no_data", lang)
        await callback.message.edit_text(
            text=text,
            reply_markup=get_back_keyboard(lang)
        )
        return
    
    # Faoliyat ma'lumotlarini ko'rsatish
    text = get_text("staff_activity_welcome", lang)
    text += f"\n\n{get_text('period', lang)}: {period_text}"
    text += f"\n{get_text('total_junior_managers', lang)}: {len(staff_data)}"
    
    # Har bir kichik menejer uchun faoliyat
    for staff in staff_data:
        activity_emoji = "🟢" if staff.get('active_applications', 0) > 0 else "🔴"
        efficiency = staff.get('efficiency', 0)
        efficiency_emoji = "🟢" if efficiency >= 80 else "🟡" if efficiency >= 60 else "🔴"
        
        text += f"\n\n{activity_emoji} {staff['full_name']}"
        text += f"\n{get_text('active_applications', lang)}: {staff.get('active_applications', 0)}"
        text += f"\n{get_text('completed_today', lang)}: {staff.get('completed_today', 0)}"
        text += f"\n{get_text('efficiency', lang)}: {efficiency_emoji} {efficiency}%"
        text += f"\n{get_text('last_activity', lang)}: {staff.get('last_activity', 'N/A')}"
        
        # Ish vaqti
        work_hours = staff.get('work_hours', 0)
        if work_hours > 0:
            text += f"\n{get_text('work_hours', lang)}: {work_hours}h"
    
    # Yangi filter keyboard
    filter_kb = get_staff_activity_filter_keyboard(lang)
    
    await callback.message.edit_text(
        text=text,
        reply_markup=filter_kb
    )
    
    # State'ni yangilash
    await state.update_data({
        'staff_data': staff_data,
        'current_period': period,
        'current_date': date
    })

@router.message(F.text == "◀️ Orqaga")
async def handle_back(message: Message, state: FSMContext):
    """Orqaga qaytish handler"""
    from keyboards.manager_new_buttons import get_manager_main_keyboard
    from handlers.manager_new.main_menu import handle_back as main_back
    
    await main_back(message, state)