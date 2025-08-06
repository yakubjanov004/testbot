"""
Manager Applications Search Handler - Simplified Implementation

This module handles manager applications search functionality.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.manager_buttons import get_manager_search_keyboard, get_manager_back_keyboard
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

async def search_applications(query: str):
    """Mock search applications"""
    # Mock search results
    all_applications = [
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
        },
        {
            'id': 'req_003_2024_01_17',
            'workflow_type': 'call_center_direct',
            'current_status': 'completed',
            'contact_info': {
                'full_name': 'Jahongir Azimov',
                'phone': '+998901234569'
            },
            'created_at': datetime.now(),
            'description': 'Qo\'ng\'iroq markazi arizasi',
            'location': 'Tashkent, Sergeli',
            'priority': 'low',
            'region': 'Toshkent shahri'
        }
    ]
    
    # Simple search logic
    query_lower = query.lower()
    results = []
    
    for app in all_applications:
        if (query_lower in app['id'].lower() or
            query_lower in app['contact_info']['full_name'].lower() or
            query_lower in app['contact_info']['phone'].lower() or
            query_lower in app['description'].lower() or
            query_lower in app['location'].lower()):
            results.append(app)
    
    return results

def get_manager_applications_search_router():
    """Router for applications search functionality"""
    router = Router()

    @router.message(F.text.in_(["🔍 Qidiruv", "🔍 Поиск"]))
    async def view_search(message: Message, state: FSMContext):
        """Manager view search handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'manager':
                return
            
            lang = user.get('language', 'uz')
            
            search_text = (
                "🔍 <b>Qidiruv - To'liq ma'lumot</b>\n\n"
                "📋 <b>Qidirish mumkin bo'lgan ma'lumotlar:</b>\n"
                "• Ariza ID raqami\n"
                "• Mijoz ismi va familiyasi\n"
                "• Telefon raqami\n"
                "• Ariza tavsifi\n"
                "• Manzil va hudud\n\n"
                "Qidiruv so'zini kiriting:"
                if lang == 'uz' else
                "🔍 <b>Поиск - Полная информация</b>\n\n"
                "📋 <b>Информация для поиска:</b>\n"
                "• Номер заявки ID\n"
                "• Имя и фамилия клиента\n"
                "• Номер телефона\n"
                "• Описание заявки\n"
                "• Адрес и регион\n\n"
                "Введите поисковый запрос:"
            )
            
            sent_message = await message.answer(
                text=search_text,
                reply_markup=get_manager_search_keyboard(lang),
                parse_mode='HTML'
            )
            
            await state.set_state("waiting_for_search_query")
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(lambda message: message.text and len(message.text) > 2)
    async def handle_search_query(message: Message, state: FSMContext):
        """Handle search query"""
        try:
            current_state = await state.get_state()
            if current_state != "waiting_for_search_query":
                return
            
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'manager':
                return
            
            # Perform search
            search_results = await search_applications(message.text)
            
            if not search_results:
                no_results_text = (
                    f"📭 '{message.text}' bo'yicha natija topilmadi.\n\n"
                    f"Boshqa so'z bilan qidirib ko'ring."
                    if user.get('language', 'uz') == 'uz' else
                    f"📭 По запросу '{message.text}' ничего не найдено.\n\n"
                    f"Попробуйте поиск с другими словами."
                )
                
                await message.answer(
                    text=no_results_text,
                    reply_markup=get_manager_back_keyboard(user.get('language', 'uz'))
                )
                return
            
            # Show first result
            await show_search_result(message, search_results[0], search_results, 0, message.text)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    async def show_search_result(message_or_callback, application, applications, index, query):
        """Show search result details"""
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
                f"🔍 <b>Qidiruv natijasi - To'liq ma'lumot</b>\n\n"
                f"🔎 <b>Qidiruv so'zi:</b> {query}\n"
                f"{workflow_type_emoji} <b>{workflow_type_text}</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"📅 <b>Sana:</b> {created_date}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📞 <b>Telefon:</b> {application['contact_info']['phone']}\n"
                f"🏛️ <b>Hudud:</b> {application.get('region', 'Noma\'lum')}\n"
                f"🏠 <b>Manzil:</b> {application.get('location', 'Noma\'lum')}\n"
                f"📝 <b>Tavsif:</b> {application['description']}\n"
                f"{status_emoji} <b>Holat:</b> {status_text}\n"
                f"{priority_emoji} <b>Ustuvorlik:</b> {priority_text}\n\n"
                f"📊 <b>Natija #{index + 1} / {len(applications)}</b>"
            )
            
            # Create navigation keyboard
            keyboard = get_search_results_navigation_keyboard(index, len(applications))
            
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer(text, reply_markup=keyboard, parse_mode='HTML')
            else:
                await message_or_callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                
        except Exception as e:
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            else:
                await message_or_callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "prev_search_result")
    async def show_previous_search_result(callback: CallbackQuery, state: FSMContext):
        """Show previous search result"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_search_index', 0)
            
            # Get search results from state
            search_data = await state.get_data()
            search_results = search_data.get('search_results', [])
            query = search_data.get('search_query', '')
            
            if current_index > 0:
                new_index = current_index - 1
                await state.update_data(current_search_index=new_index)
                await show_search_result(callback, search_results[new_index], search_results, new_index, query)
            else:
                await callback.answer("Bu birinchi natija")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "next_search_result")
    async def show_next_search_result(callback: CallbackQuery, state: FSMContext):
        """Show next search result"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_search_index', 0)
            
            # Get search results from state
            search_data = await state.get_data()
            search_results = search_data.get('search_results', [])
            query = search_data.get('search_query', '')
            
            if current_index < len(search_results) - 1:
                new_index = current_index + 1
                await state.update_data(current_search_index=new_index)
                await show_search_result(callback, search_results[new_index], search_results, new_index, query)
            else:
                await callback.answer("Bu oxirgi natija")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    return router

def get_search_results_navigation_keyboard(current_index: int, total_results: int):
    """Create navigation keyboard for search results"""
    keyboard = []
    
    # Navigation row
    nav_buttons = []
    
    # Previous button
    if current_index > 0:
        nav_buttons.append(InlineKeyboardButton(
            text="⬅️ Oldingi",
            callback_data="prev_search_result"
        ))
    
    # Next button
    if current_index < total_results - 1:
        nav_buttons.append(InlineKeyboardButton(
            text="Keyingi ➡️",
            callback_data="next_search_result"
        ))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Back to menu
    keyboard.append([InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="back_to_main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard) 