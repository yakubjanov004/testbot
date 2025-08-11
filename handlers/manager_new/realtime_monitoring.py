from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.manager_new_buttons import get_back_keyboard, get_realtime_refresh_keyboard
from utils.language import get_text
from utils.database import get_user_language, get_realtime_applications
from datetime import datetime, timedelta
import asyncio

router = Router()

@router.message(F.text == "🕐 Real vaqtda kuzatish")
async def handle_realtime_monitoring(message: Message, state: FSMContext):
    """Real vaqtda kuzatish handler"""
    lang = await get_user_language(message.from_user.id)
    user_id = message.from_user.id
    
    # Real vaqtda ma'lumotlarni olish
    realtime_data = await get_realtime_applications(user_id)
    
    if not realtime_data:
        text = get_text("realtime_no_data", lang)
        await message.answer(text, reply_markup=get_back_keyboard(lang))
        return
    
    # Real vaqtda ma'lumotlarni ko'rsatish
    text = get_text("realtime_monitoring_welcome", lang)
    text += f"\n\n{get_text('last_updated', lang)}: {datetime.now().strftime('%H:%M:%S')}"
    text += f"\n{get_text('total_active', lang)}: {len(realtime_data)}"
    
    # Har bir ariza uchun real vaqtda ma'lumot
    for app in realtime_data:
        status_emoji = {
            'in_progress': '⏳',
            'assigned': '👨‍🔧',
            'pending': '⏸️',
            'urgent': '🚨'
        }.get(app['status'], '❓')
        
        # Vaqt hisobini ko'rsatish
        start_time = app.get('start_time')
        if start_time:
            elapsed = datetime.now() - start_time
            hours = int(elapsed.total_seconds() // 3600)
            minutes = int((elapsed.total_seconds() % 3600) // 60)
            time_text = f"{hours}h {minutes}m"
        else:
            time_text = "N/A"
        
        text += f"\n\n{status_emoji} {get_text('application', lang)} #{app['id']}"
        text += f"\n{get_text('client', lang)}: {app['client_name']}"
        text += f"\n{get_text('type', lang)}: {app['type']}"
        text += f"\n{get_text('assigned_to', lang)}: {app.get('assigned_technician', 'N/A')}"
        text += f"\n{get_text('elapsed_time', lang)}: {time_text}"
        text += f"\n{get_text('priority', lang)}: {get_text(f'priority_{app.get('priority', 'medium')}', lang)}"
    
    # Refresh keyboard
    refresh_kb = get_realtime_refresh_keyboard(lang)
    
    await message.answer(
        text=text,
        reply_markup=refresh_kb
    )
    
    # State'ga ma'lumotlarni saqlash
    await state.update_data({
        'realtime_data': realtime_data,
        'last_update': datetime.now()
    })

@router.callback_query(F.data == "realtime_refresh")
async def handle_refresh(callback: CallbackQuery, state: FSMContext):
    """Real vaqtda yangilash handler"""
    lang = await get_user_language(callback.from_user.id)
    user_id = callback.from_user.id
    
    await callback.answer(get_text("refreshing", lang))
    
    # Yangi ma'lumotlarni olish
    realtime_data = await get_realtime_applications(user_id)
    
    if not realtime_data:
        text = get_text("realtime_no_data", lang)
        await callback.message.edit_text(
            text=text,
            reply_markup=get_back_keyboard(lang)
        )
        return
    
    # Yangilangan ma'lumotlarni ko'rsatish
    text = get_text("realtime_monitoring_welcome", lang)
    text += f"\n\n{get_text('last_updated', lang)}: {datetime.now().strftime('%H:%M:%S')}"
    text += f"\n{get_text('total_active', lang)}: {len(realtime_data)}"
    
    # Har bir ariza uchun real vaqtda ma'lumot
    for app in realtime_data:
        status_emoji = {
            'in_progress': '⏳',
            'assigned': '👨‍🔧',
            'pending': '⏸️',
            'urgent': '🚨'
        }.get(app['status'], '❓')
        
        # Vaqt hisobini ko'rsatish
        start_time = app.get('start_time')
        if start_time:
            elapsed = datetime.now() - start_time
            hours = int(elapsed.total_seconds() // 3600)
            minutes = int((elapsed.total_seconds() % 3600) // 60)
            time_text = f"{hours}h {minutes}m"
        else:
            time_text = "N/A"
        
        text += f"\n\n{status_emoji} {get_text('application', lang)} #{app['id']}"
        text += f"\n{get_text('client', lang)}: {app['client_name']}"
        text += f"\n{get_text('type', lang)}: {app['type']}"
        text += f"\n{get_text('assigned_to', lang)}: {app.get('assigned_technician', 'N/A')}"
        text += f"\n{get_text('elapsed_time', lang)}: {time_text}"
        text += f"\n{get_text('priority', lang)}: {get_text(f'priority_{app.get('priority', 'medium')}', lang)}"
    
    # Yangi refresh keyboard
    refresh_kb = get_realtime_refresh_keyboard(lang)
    
    await callback.message.edit_text(
        text=text,
        reply_markup=refresh_kb
    )
    
    # State'ni yangilash
    await state.update_data({
        'realtime_data': realtime_data,
        'last_update': datetime.now()
    })

@router.callback_query(F.data == "realtime_back")
async def handle_realtime_back(callback: CallbackQuery, state: FSMContext):
    """Real vaqtda orqaga qaytish handler"""
    from keyboards.manager_new_buttons import get_manager_main_keyboard
    from handlers.manager_new.main_menu import handle_back as main_back
    
    await main_back(callback.message, state)
    await callback.answer()

@router.message(F.text == "◀️ Orqaga")
async def handle_back(message: Message, state: FSMContext):
    """Orqaga qaytish handler"""
    from keyboards.manager_new_buttons import get_manager_main_keyboard
    from handlers.manager_new.main_menu import handle_back as main_back
    
    await main_back(message, state)