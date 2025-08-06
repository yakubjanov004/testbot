"""
Controller Staff Application Creation - Simplified Implementation

This module handles controller staff application creation functionality.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.controllers_buttons import get_staff_creation_keyboard, get_controller_back_keyboard
from typing import Dict, Any, List, Optional
from datetime import datetime

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'controller',
        'language': 'uz',
        'full_name': 'Test Controller',
        'phone_number': '+998901234567'
    }

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    return 'uz'

async def get_staff_members():
    """Mock get staff members"""
    return [
        {
            'id': 1,
            'full_name': 'Aziz Karimov',
            'role': 'technician',
            'phone': '+998901234567',
            'email': 'aziz@example.com',
            'status': 'active',
            'created_at': datetime.now(),
            'applications_count': 15
        },
        {
            'id': 2,
            'full_name': 'Malika Toshmatova',
            'role': 'manager',
            'phone': '+998901234568',
            'email': 'malika@example.com',
            'status': 'active',
            'created_at': datetime.now(),
            'applications_count': 8
        },
        {
            'id': 3,
            'full_name': 'Jahongir Azimov',
            'role': 'junior_manager',
            'phone': '+998901234569',
            'email': 'jahongir@example.com',
            'status': 'inactive',
            'created_at': datetime.now(),
            'applications_count': 3
        }
    ]

async def create_staff_application(staff_data: Dict):
    """Mock create staff application"""
    return {
        'id': 'staff_001_2024_01_15',
        'staff_id': staff_data.get('id'),
        'staff_name': staff_data.get('full_name'),
        'application_type': 'new_staff',
        'status': 'pending',
        'created_at': datetime.now(),
        'description': 'Yangi xodim qo\'shish arizasi'
    }

def get_staff_application_creation_router():
    """Router for staff application creation functionality"""
    router = Router()

    @router.message(F.text.in_(["👥 Xodim arizasi yaratish", "👥 Создание заявки сотрудника"]))
    async def view_staff_creation(message: Message, state: FSMContext):
        """Controller view staff creation handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'controller':
                return
            
            lang = user.get('language', 'uz')
            
            staff_text = (
                "👥 <b>Xodim arizasi yaratish - To'liq ma'lumot</b>\n\n"
                "📋 <b>Mavjud xodimlar:</b>\n"
                "• Texniklar\n"
                "• Menejerlar\n"
                "• Junior menejerlar\n"
                "• Call center operatorlari\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
                if lang == 'uz' else
                "👥 <b>Создание заявки сотрудника - Полная информация</b>\n\n"
                "📋 <b>Существующие сотрудники:</b>\n"
                "• Техники\n"
                "• Менеджеры\n"
                "• Младшие менеджеры\n"
                "• Операторы call center\n\n"
                "Выберите один из разделов ниже:"
            )
            
            sent_message = await message.answer(
                text=staff_text,
                reply_markup=get_staff_creation_keyboard(lang),
                parse_mode='HTML'
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "view_staff_members")
    async def view_staff_members(callback: CallbackQuery, state: FSMContext):
        """View staff members"""
        try:
            await callback.answer()
            
            # Get staff members
            staff_members = await get_staff_members()
            
            if not staff_members:
                no_staff_text = (
                    "📭 Xodimlar mavjud emas."
                    if callback.from_user.language_code == 'uz' else
                    "📭 Сотрудники не найдены."
                )
                
                await callback.message.edit_text(
                    text=no_staff_text,
                    reply_markup=get_controller_back_keyboard('uz')
                )
                return
            
            # Show first staff member
            await show_staff_details(callback, staff_members[0], staff_members, 0)
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    async def show_staff_details(callback, staff, staff_members, index):
        """Show staff details with navigation"""
        try:
            # Format status
            status_emoji = {
                'active': '🟢',
                'inactive': '🔴',
                'pending': '🟡'
            }.get(staff['status'], '⚪')
            
            status_text = {
                'active': 'Faol',
                'inactive': 'Faol emas',
                'pending': 'Kutilmoqda'
            }.get(staff['status'], 'Noma\'lum')
            
            # Format role
            role_text = {
                'technician': 'Texnik',
                'manager': 'Menejer',
                'junior_manager': 'Junior menejer',
                'call_center_operator': 'Call center operator'
            }.get(staff['role'], 'Boshqa')
            
            # Format date
            created_date = staff['created_at'].strftime('%d.%m.%Y')
            
            # To'liq ma'lumot
            text = (
                f"👤 <b>Xodim ma'lumotlari - To'liq ma'lumot</b>\n\n"
                f"🆔 <b>Xodim ID:</b> {staff['id']}\n"
                f"👤 <b>To'liq ism:</b> {staff['full_name']}\n"
                f"📋 <b>Lavozim:</b> {role_text}\n"
                f"📞 <b>Telefon:</b> {staff['phone']}\n"
                f"📧 <b>Email:</b> {staff['email']}\n"
                f"{status_emoji} <b>Holat:</b> {status_text}\n"
                f"📅 <b>Qo'shilgan:</b> {created_date}\n"
                f"📊 <b>Arizalar soni:</b> {staff['applications_count']}\n\n"
                f"📊 <b>Xodim #{index + 1} / {len(staff_members)}</b>"
            )
            
            # Create navigation keyboard
            keyboard = get_staff_navigation_keyboard(index, len(staff_members))
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "staff_prev")
    async def show_previous_staff(callback: CallbackQuery, state: FSMContext):
        """Show previous staff member"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_staff_index', 0)
            
            staff_members = await get_staff_members()
            
            if current_index > 0:
                new_index = current_index - 1
                await state.update_data(current_staff_index=new_index)
                await show_staff_details(callback, staff_members[new_index], staff_members, new_index)
            else:
                await callback.answer("Bu birinchi xodim")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "staff_next")
    async def show_next_staff(callback: CallbackQuery, state: FSMContext):
        """Show next staff member"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_staff_index', 0)
            
            staff_members = await get_staff_members()
            
            if current_index < len(staff_members) - 1:
                new_index = current_index + 1
                await state.update_data(current_staff_index=new_index)
                await show_staff_details(callback, staff_members[new_index], staff_members, new_index)
            else:
                await callback.answer("Bu oxirgi xodim")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "create_staff_application")
    async def create_staff_application_handler(callback: CallbackQuery, state: FSMContext):
        """Create staff application"""
        try:
            await callback.answer()
            
            # Get current staff from state
            current_index = await state.get_data()
            current_index = current_index.get('current_staff_index', 0)
            
            staff_members = await get_staff_members()
            
            if current_index >= len(staff_members):
                await callback.answer("Xodim topilmadi")
                return
            
            selected_staff = staff_members[current_index]
            
            # Create application
            application = await create_staff_application(selected_staff)
            
            success_text = (
                f"✅ <b>Ariza muvaffaqiyatli yaratildi!</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"👤 <b>Xodim:</b> {application['staff_name']}\n"
                f"📋 <b>Turi:</b> {application['application_type']}\n"
                f"📝 <b>Tavsif:</b> {application['description']}\n"
                f"📅 <b>Yaratilgan:</b> {application['created_at'].strftime('%d.%m.%Y %H:%M')}\n"
                f"📊 <b>Holat:</b> {application['status']}"
            )
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_staff_creation")]
            ])
            
            await callback.message.edit_text(success_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "back_to_staff_creation")
    async def back_to_staff_creation(callback: CallbackQuery, state: FSMContext):
        """Back to staff creation menu"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            staff_text = (
                "👥 <b>Xodim arizasi yaratish - To'liq ma'lumot</b>\n\n"
                "📋 <b>Mavjud xodimlar:</b>\n"
                "• Texniklar\n"
                "• Menejerlar\n"
                "• Junior menejerlar\n"
                "• Call center operatorlari\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
                if lang == 'uz' else
                "👥 <b>Создание заявки сотрудника - Полная информация</b>\n\n"
                "📋 <b>Существующие сотрудники:</b>\n"
                "• Техники\n"
                "• Менеджеры\n"
                "• Младшие менеджеры\n"
                "• Операторы call center\n\n"
                "Выберите один из разделов ниже:"
            )
            
            await callback.message.edit_text(
                text=staff_text,
                reply_markup=get_staff_creation_keyboard(lang),
                parse_mode='HTML'
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    return router

def get_staff_navigation_keyboard(current_index: int, total_staff: int):
    """Create navigation keyboard for staff members"""
    keyboard = []
    
    # Navigation row
    nav_buttons = []
    
    # Previous button
    if current_index > 0:
        nav_buttons.append(InlineKeyboardButton(
            text="⬅️ Oldingi",
            callback_data="staff_prev"
        ))
    
    # Next button
    if current_index < total_staff - 1:
        nav_buttons.append(InlineKeyboardButton(
            text="Keyingi ➡️",
            callback_data="staff_next"
        ))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Create application button
    keyboard.append([InlineKeyboardButton(text="📝 Ariza yaratish", callback_data="create_staff_application")])
    
    # Back to menu
    keyboard.append([InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="back_to_main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_controller_staff_application_router():
    """Get controller staff application router - alias for get_staff_application_creation_router"""
    return get_staff_application_creation_router()
