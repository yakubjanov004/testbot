"""
Applications List Handler - Simplified Implementation

Bu modul manager uchun arizalar ro'yxati va navigatsiya funksionalligini o'z ichiga oladi.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.manager_buttons import get_manager_view_applications_keyboard, get_manager_back_keyboard
from typing import Dict, Any, List, Optional
from datetime import datetime
from filters.role_filter import RoleFilter

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

# Mock workflow access control
class MockWorkflowAccessControl:
    """Mock workflow access control"""
    async def get_filtered_requests_for_role(self, user_id: int, user_role: str):
        """Mock get filtered requests for role"""
        from datetime import datetime
        return [
            {
                'id': 'req_001_2024_01_15',
                'workflow_type': 'connection_request',
                'current_status': 'in_progress',
                'role_current': 'manager',
                'contact_info': {
                    'full_name': 'Aziz Karimov',
                    'phone': '+998901234567'
                },
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'description': 'Internet ulanish arizasi',
                'location': 'Tashkent, Chorsu',
                'priority': 'high',
                'estimated_time': '2-3 kun',
                'technician': 'Ahmad Karimov',
                'region': 'Toshkent shahri',
                'address': 'Chorsu tumani, 15-uy'
            },
            {
                'id': 'req_002_2024_01_16',
                'workflow_type': 'technical_service',
                'current_status': 'created',
                'role_current': 'manager',
                'contact_info': {
                    'full_name': 'Malika Toshmatova',
                    'phone': '+998901234568'
                },
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'description': 'TV signal muammosi',
                'location': 'Tashkent, Yunusabad',
                'priority': 'normal',
                'estimated_time': '1-2 kun',
                'technician': 'Bekzod Azimov',
                'region': 'Toshkent shahri',
                'address': 'Yunusobod tumani, 25-uy'
            },
            {
                'id': 'req_003_2024_01_17',
                'workflow_type': 'call_center_direct',
                'current_status': 'completed',
                'role_current': 'manager',
                'contact_info': {
                    'full_name': 'Jahongir Azimov',
                    'phone': '+998901234569'
                },
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'description': 'Qo\'ng\'iroq markazi arizasi',
                'location': 'Tashkent, Sergeli',
                'priority': 'low',
                'estimated_time': '1 kun',
                'technician': 'Karim Karimov',
                'region': 'Toshkent shahri',
                'address': 'Sergeli tumani, 8-uy'
            }
        ]

def get_manager_applications_list_router():
    """Router for applications list and navigation functionality"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["📋 Arizalarni ko'rish"]))
    async def view_all_applications(message: Message, state: FSMContext):
        """Manager view all applications handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'manager':
                return
            
            lang = user.get('language', 'uz')
            
            # Use workflow access control to get filtered requests for manager role
            access_control = MockWorkflowAccessControl()
            applications = await access_control.get_filtered_requests_for_role(message.from_user.id, 'manager')
            
            if not applications:
                await message.answer("Hozircha arizalar yo'q.")
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
            
            # Format dates
            created_date = application['created_at'].strftime('%d.%m.%Y %H:%M')
            updated_date = application['updated_at'].strftime('%d.%m.%Y %H:%M')
            
            # To'liq ma'lumot
            text = (
                f"{workflow_type_emoji} <b>{workflow_type_text} - To'liq ma'lumot</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"📅 <b>Yaratilgan:</b> {created_date}\n"
                f"🔄 <b>Yangilangan:</b> {updated_date}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📞 <b>Telefon:</b> {application['contact_info']['phone']}\n"
                f"🏛️ <b>Hudud:</b> {application.get('region', 'Noma\'lum')}\n"
                f"🏠 <b>Manzil:</b> {application.get('address', 'Noma\'lum')}\n"
                f"📝 <b>Tavsif:</b> {application['description']}\n"
                f"{status_emoji} <b>Holat:</b> {status_text}\n"
                f"👨‍🔧 <b>Texnik:</b> {application.get('technician', 'Tayinlanmagan')}\n"
                f"⏰ <b>Taxminiy vaqt:</b> {application.get('estimated_time', 'Noma\'lum')}\n"
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
                await message_or_callback.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            else:
                await message_or_callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "mgr_prev_application")
    async def show_previous_application(callback: CallbackQuery, state: FSMContext):
        """Show previous application"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_app_index', 0)
            
            access_control = MockWorkflowAccessControl()
            applications = await access_control.get_filtered_requests_for_role(callback.from_user.id, 'manager')
            
            if current_index > 0:
                new_index = current_index - 1
                await state.update_data(current_app_index=new_index)
                await show_application_details(callback, applications[new_index], applications, new_index)
            else:
                await callback.answer("Bu birinchi ariza")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "mgr_next_application")
    async def show_next_application(callback: CallbackQuery, state: FSMContext):
        """Show next application"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_app_index', 0)
            
            access_control = MockWorkflowAccessControl()
            applications = await access_control.get_filtered_requests_for_role(callback.from_user.id, 'manager')
            
            if current_index < len(applications) - 1:
                new_index = current_index + 1
                await state.update_data(current_app_index=new_index)
                await show_application_details(callback, applications[new_index], applications, new_index)
            else:
                await callback.answer("Bu oxirgi ariza")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "mgr_view_all_applications")
    async def view_all_applications_callback(callback: CallbackQuery, state: FSMContext):
        """View all applications from callback"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                return
            
            access_control = MockWorkflowAccessControl()
            applications = await access_control.get_filtered_requests_for_role(callback.from_user.id, 'manager')
            
            if not applications:
                await callback.message.edit_text("Hozircha arizalar yo'q.")
                return
            
            # Reset index to 0
            await state.update_data(current_app_index=0)
            await show_application_details(callback, applications[0], applications, 0)
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

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
            callback_data="mgr_prev_application"
        ))
    
    # Next button
    if current_index < total_applications - 1:
        nav_buttons.append(InlineKeyboardButton(
            text="Keyingi ➡️",
            callback_data="mgr_next_application"
        ))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Back to menu
    keyboard.append([InlineKeyboardButton(text="🏠 Bosh sahifaapplist", callback_data="back_to_main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard) 