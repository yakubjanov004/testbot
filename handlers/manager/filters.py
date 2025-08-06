"""
Manager Filters Handler - Simplified Implementation

This module handles manager filters functionality.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.manager_buttons import get_manager_filters_keyboard, get_manager_back_keyboard
from typing import Dict, Any, List, Optional
from datetime import datetime

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'manager',
        'language': 'uz',
        'full_name': 'Test Manager',
        'phone_number': '+998901234567'
    }

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    return 'uz'

async def get_filtered_applications(filters: dict):
    """Mock get filtered applications"""
    return [
        {
            'id': 'req_001_2024_01_15',
            'workflow_type': 'connection_request',
            'current_status': 'in_progress',
            'contact_info': {
                'full_name': 'Aziz Karimov',
                'phone': '+998901234567'
            },
            'created_at': datetime.now(),
            'description': 'Internet ulanish arizasi',
            'location': 'Tashkent, Chorsu',
            'priority': 'high',
            'region': 'Toshkent shahri'
        },
        {
            'id': 'req_002_2024_01_16',
            'workflow_type': 'technical_service',
            'current_status': 'created',
            'contact_info': {
                'full_name': 'Malika Toshmatova',
                'phone': '+998901234568'
            },
            'created_at': datetime.now(),
            'description': 'TV signal muammosi',
            'location': 'Tashkent, Yunusabad',
            'priority': 'normal',
            'region': 'Toshkent shahri'
        }
    ]

def get_filters_router():
    """Router for filters functionality"""
    router = Router()

    @router.message(F.text.in_(["🔍 Filtrlash", "🔍 Фильтрация"]))
    async def view_filters(message: Message, state: FSMContext):
        """Manager view filters handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'manager':
                return
            
            lang = user.get('language', 'uz')
            
            filters_text = (
                "🔍 <b>Filtrlash - To'liq ma'lumot</b>\n\n"
                "📋 <b>Mavjud filtrlash turlari:</b>\n"
                "• Hudud bo'yicha\n"
                "• Holat bo'yicha\n"
                "• Sana bo'yicha\n"
                "• Ustuvorlik bo'yicha\n"
                "• Ariza turi bo'yicha\n\n"
                "Quyidagi filtrlardan birini tanlang:"
                if lang == 'uz' else
                "🔍 <b>Фильтрация - Полная информация</b>\n\n"
                "📋 <b>Доступные типы фильтрации:</b>\n"
                "• По региону\n"
                "• По статусу\n"
                "• По дате\n"
                "• По приоритету\n"
                "• По типу заявки\n\n"
                "Выберите один из фильтров ниже:"
            )
            
            sent_message = await message.answer(
                text=filters_text,
                reply_markup=get_manager_filters_keyboard(lang),
                parse_mode='HTML'
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "filter_by_region")
    async def filter_by_region(callback: CallbackQuery, state: FSMContext):
        """Filter by region"""
        try:
            await callback.answer()
            
            # Mock filter by region
            filters = {'region': 'Toshkent shahri'}
            applications = await get_filtered_applications(filters)
            
            if not applications:
                no_results_text = (
                    "📭 Bu hududda arizalar topilmadi."
                    if callback.from_user.language_code == 'uz' else
                    "📭 В этом регионе заявки не найдены."
                )
                
                await callback.message.edit_text(
                    text=no_results_text,
                    reply_markup=get_manager_back_keyboard('uz')
                )
                return
            
            # Show first application
            await show_filtered_application(callback, applications[0], applications, 0)
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "filter_by_status")
    async def filter_by_status(callback: CallbackQuery, state: FSMContext):
        """Filter by status"""
        try:
            await callback.answer()
            
            # Mock filter by status
            filters = {'status': 'in_progress'}
            applications = await get_filtered_applications(filters)
            
            if not applications:
                no_results_text = (
                    "📭 Bu holatda arizalar topilmadi."
                    if callback.from_user.language_code == 'uz' else
                    "📭 Заявки в этом статусе не найдены."
                )
                
                await callback.message.edit_text(
                    text=no_results_text,
                    reply_markup=get_manager_back_keyboard('uz')
                )
                return
            
            # Show first application
            await show_filtered_application(callback, applications[0], applications, 0)
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    async def show_filtered_application(callback, application, applications, index):
        """Show filtered application details"""
        try:
            # Format workflow type
            workflow_type_emoji = {
                'connection_request': '🔌',
                'technical_service': '🔧',
                'call_center_direct': '📞'
            }.get(application['workflow_type'], '📄')
            
            workflow_type_text = {
                'connection_request': 'Ulanish arizasi',
                'technical_service': 'Texnik xizmat',
                'call_center_direct': 'Call Center'
            }.get(application['workflow_type'], 'Boshqa')
            
            # Format status
            status_emoji = {
                'in_progress': '🟡',
                'created': '🟠',
                'completed': '🟢',
                'cancelled': '🔴'
            }.get(application['current_status'], '⚪')
            
            status_text = {
                'in_progress': 'Jarayonda',
                'created': 'Yaratilgan',
                'completed': 'Bajarilgan',
                'cancelled': 'Bekor qilingan'
            }.get(application['current_status'], 'Noma\'lum')
            
            # Format priority
            priority_emoji = {
                'high': '🔴',
                'normal': '🟡',
                'low': '🟢'
            }.get(application.get('priority', 'normal'), '🟡')
            
            priority_text = {
                'high': 'Yuqori',
                'normal': 'O\'rtacha',
                'low': 'Past'
            }.get(application.get('priority', 'normal'), 'O\'rtacha')
            
            # Format date
            created_date = application['created_at'].strftime('%d.%m.%Y %H:%M')
            
            # To'liq ma'lumot
            text = (
                f"{workflow_type_emoji} <b>{workflow_type_text} - To'liq ma'lumot</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"📅 <b>Sana:</b> {created_date}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📞 <b>Telefon:</b> {application['contact_info']['phone']}\n"
                f"🏛️ <b>Hudud:</b> {application.get('region', 'Noma\'lum')}\n"
                f"🏠 <b>Manzil:</b> {application.get('location', 'Noma\'lum')}\n"
                f"📝 <b>Tavsif:</b> {application['description']}\n"
                f"{status_emoji} <b>Holat:</b> {status_text}\n"
                f"{priority_emoji} <b>Ustuvorlik:</b> {priority_text}\n\n"
                f"📊 <b>Ariza #{index + 1} / {len(applications)}</b>"
            )
            
            # Create navigation keyboard
            keyboard = get_filtered_applications_navigation_keyboard(index, len(applications))
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    return router

def get_filtered_applications_navigation_keyboard(current_index: int, total_applications: int):
    """Create navigation keyboard for filtered applications"""
    keyboard = []
    
    # Navigation row
    nav_buttons = []
    
    # Previous button
    if current_index > 0:
        nav_buttons.append(InlineKeyboardButton(
            text="⬅️ Oldingi",
            callback_data="prev_filtered_app"
        ))
    
    # Next button
    if current_index < total_applications - 1:
        nav_buttons.append(InlineKeyboardButton(
            text="Keyingi ➡️",
            callback_data="next_filtered_app"
        ))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Back to menu
    keyboard.append([InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="back_to_main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)