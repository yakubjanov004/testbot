"""
Call Center Supervisor Inbox Handler - Simplified Implementation

This module handles call center supervisor inbox functionality.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from datetime import datetime

def get_supervisor_inbox_router():
    """Router for supervisor inbox functionality - Simplified Implementation"""
    router = Router()

    @router.message(F.text.in_(["📥 Inbox", "📥 Входящие"]))
    async def view_inbox(message: Message, state: FSMContext):
        """Supervisor view inbox handler"""
        try:
            # Mock applications data
            applications = [
                {
                    'id': 'req_001_2024_01_15',
                    'workflow_type': 'call_center_direct',
                    'current_status': 'pending',
                    'contact_info': {
                        'full_name': 'Aziz Karimov',
                        'phone': '+998901234567'
                    },
                    'created_at': datetime.now(),
                    'description': 'Qo\'ng\'iroq markazi arizasi',
                    'location': 'Tashkent, Chorsu',
                    'priority': 'high',
                    'region': 'Toshkent shahri',
                    'call_type': 'complaint'
                },
                {
                    'id': 'req_002_2024_01_16',
                    'workflow_type': 'call_center_direct',
                    'current_status': 'in_progress',
                    'contact_info': {
                        'full_name': 'Malika Toshmatova',
                        'phone': '+998901234568'
                    },
                    'created_at': datetime.now(),
                    'description': 'Xizmat haqida ma\'lumot',
                    'location': 'Tashkent, Yunusabad',
                    'priority': 'normal',
                    'region': 'Toshkent shahri',
                    'call_type': 'information'
                }
            ]
            
            if not applications:
                await message.answer("📭 Hozircha qo'ng'iroq markazi arizalari yo'q.")
                return
            
            # Show first application
            await show_application_details(message, applications[0], applications, 0)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    async def show_application_details(message_or_callback, application, applications, index):
        """Show application details with navigation"""
        try:
            # Format workflow type
            workflow_type_emoji = {
                'call_center_direct': '📞',
                'connection_request': '🔌',
                'technical_service': '🔧'
            }.get(application['workflow_type'], '📄')
            
            workflow_type_text = {
                'call_center_direct': 'Call Center arizasi',
                'connection_request': 'Ulanish arizasi',
                'technical_service': 'Texnik xizmat'
            }.get(application['workflow_type'], 'Boshqa')
            
            # Format status
            status_emoji = {
                'pending': '🟡',
                'in_progress': '🟠',
                'completed': '🟢',
                'cancelled': '🔴'
            }.get(application['current_status'], '⚪')
            
            status_text = {
                'pending': 'Kutilmoqda',
                'in_progress': 'Jarayonda',
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
            
            # Format call type
            call_type_text = {
                'complaint': 'Shikoyat',
                'information': 'Ma\'lumot',
                'request': 'So\'rov',
                'support': 'Yordam'
            }.get(application.get('call_type', 'unknown'), 'Boshqa')
            
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
                f"📞 <b>Qo'ng'iroq turi:</b> {call_type_text}\n"
                f"{priority_emoji} <b>Ustuvorlik:</b> {priority_text}\n\n"
                f"📊 <b>Ariza #{index + 1} / {len(applications)}</b>"
            )
            
            # Create navigation keyboard
            keyboard = get_applications_navigation_keyboard(index, len(applications))
            
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer(text, reply_markup=keyboard, parse_mode='HTML')
            else:
                await message_or_callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                
        except Exception as e:
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            else:
                await message_or_callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "supervisor_prev_application")
    async def show_previous_application(callback: CallbackQuery, state: FSMContext):
        """Show previous application"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_app_index', 0)
            
            # Mock applications data
            applications = [
                {
                    'id': 'req_001_2024_01_15',
                    'workflow_type': 'call_center_direct',
                    'current_status': 'pending',
                    'contact_info': {
                        'full_name': 'Aziz Karimov',
                        'phone': '+998901234567'
                    },
                    'created_at': datetime.now(),
                    'description': 'Qo\'ng\'iroq markazi arizasi',
                    'location': 'Tashkent, Chorsu',
                    'priority': 'high',
                    'region': 'Toshkent shahri',
                    'call_type': 'complaint'
                },
                {
                    'id': 'req_002_2024_01_16',
                    'workflow_type': 'call_center_direct',
                    'current_status': 'in_progress',
                    'contact_info': {
                        'full_name': 'Malika Toshmatova',
                        'phone': '+998901234568'
                    },
                    'created_at': datetime.now(),
                    'description': 'Xizmat haqida ma\'lumot',
                    'location': 'Tashkent, Yunusabad',
                    'priority': 'normal',
                    'region': 'Toshkent shahri',
                    'call_type': 'information'
                }
            ]
            
            if current_index > 0:
                new_index = current_index - 1
                await state.update_data(current_app_index=new_index)
                await show_application_details(callback, applications[new_index], applications, new_index)
            else:
                await callback.answer("Bu birinchi ariza")
                
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "supervisor_next_application")
    async def show_next_application(callback: CallbackQuery, state: FSMContext):
        """Show next application"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_app_index', 0)
            
            # Mock applications data
            applications = [
                {
                    'id': 'req_001_2024_01_15',
                    'workflow_type': 'call_center_direct',
                    'current_status': 'pending',
                    'contact_info': {
                        'full_name': 'Aziz Karimov',
                        'phone': '+998901234567'
                    },
                    'created_at': datetime.now(),
                    'description': 'Qo\'ng\'iroq markazi arizasi',
                    'location': 'Tashkent, Chorsu',
                    'priority': 'high',
                    'region': 'Toshkent shahri',
                    'call_type': 'complaint'
                },
                {
                    'id': 'req_002_2024_01_16',
                    'workflow_type': 'call_center_direct',
                    'current_status': 'in_progress',
                    'contact_info': {
                        'full_name': 'Malika Toshmatova',
                        'phone': '+998901234568'
                    },
                    'created_at': datetime.now(),
                    'description': 'Xizmat haqida ma\'lumot',
                    'location': 'Tashkent, Yunusabad',
                    'priority': 'normal',
                    'region': 'Toshkent shahri',
                    'call_type': 'information'
                }
            ]
            
            if current_index < len(applications) - 1:
                new_index = current_index + 1
                await state.update_data(current_app_index=new_index)
                await show_application_details(callback, applications[new_index], applications, new_index)
            else:
                await callback.answer("Bu oxirgi ariza")
                
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    return router

def get_applications_navigation_keyboard(current_index: int, total_applications: int):
    """Create navigation keyboard for applications"""
    keyboard = []
    
    # Navigation row
    nav_buttons = []
    
    # Previous button
    if current_index > 0:
        nav_buttons.append(InlineKeyboardButton(
            text="⬅️ Oldingi",
            callback_data="supervisor_prev_application"
        ))
    
    # Next button
    if current_index < total_applications - 1:
        nav_buttons.append(InlineKeyboardButton(
            text="Keyingi ➡️",
            callback_data="supervisor_next_application"
        ))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Back to menu
    keyboard.append([InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="back_to_main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)