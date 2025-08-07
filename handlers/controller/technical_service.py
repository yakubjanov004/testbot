"""
Controller Technical Service Handler
Manages technical service for controller
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.controllers_buttons import (
    get_technical_service_keyboard, 
    get_controller_back_keyboard,
    get_technical_service_navigation_keyboard
)
from typing import Dict, Any, List, Optional
from datetime import datetime
from filters.role_filter import RoleFilter

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

async def get_user_lang(user_id: int):
    """Mock get user language"""
    return 'uz'

async def get_technical_services():
    """Mock get technical services"""
    return [
        {
            'id': 'ts_001_2024_01_15',
            'client_name': 'Aziz Karimov',
            'client_phone': '+998901234567',
            'service_type': 'internet_repair',
            'status': 'pending',
            'description': 'Internet tezligi sekin',
            'address': 'Tashkent, Chorsu',
            'priority': 'high',
            'created_at': datetime.now(),
            'estimated_duration': '2-3 soat'
        },
        {
            'id': 'ts_002_2024_01_16',
            'client_name': 'Malika Toshmatova',
            'client_phone': '+998901234568',
            'service_type': 'tv_repair',
            'status': 'in_progress',
            'description': 'TV signal yo\'q',
            'address': 'Tashkent, Yunusabad',
            'priority': 'normal',
            'created_at': datetime.now(),
            'estimated_duration': '1-2 soat'
        },
        {
            'id': 'ts_003_2024_01_17',
            'client_name': 'Jahongir Azimov',
            'client_phone': '+998901234569',
            'service_type': 'cable_repair',
            'status': 'completed',
            'description': 'Kabel uzilgan',
            'address': 'Tashkent, Sergeli',
            'priority': 'urgent',
            'created_at': datetime.now(),
            'estimated_duration': 'Yakunlangan'
        }
    ]

def get_technical_service_router():
    """Get controller technical service router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("controller")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🔧 Texnik xizmat", "🔧 Техническое обслуживание"]))
    async def view_technical_service(message: Message, state: FSMContext):
        """Handle technical service view"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            
            lang = user.get('language', 'uz')
            services = await get_technical_services()
            
            if not services:
                no_services_text = "🔧 Hozircha texnik xizmatlar mavjud emas."
                await message.answer(no_services_text)
                return
            
            # Show first service
            await state.update_data(technical_services=services, current_index=0)
            await show_service_details(message, services[0], services, 0)
            
        except Exception as e:
            print(f"Error in view_technical_service: {str(e)}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    async def show_service_details(message_or_callback, service, services, index):
        """Show service details with navigation"""
        try:
            # Format service type
            service_type_emoji = {
                'internet_repair': '🌐',
                'tv_repair': '📺',
                'cable_repair': '🔌',
                'phone_repair': '📞',
                'installation': '🔧'
            }.get(service['service_type'], '🔧')
            
            service_type_text = {
                'internet_repair': 'Internet ta\'mirlash',
                'tv_repair': 'TV ta\'mirlash',
                'cable_repair': 'Kabel ta\'mirlash',
                'phone_repair': 'Telefon ta\'mirlash',
                'installation': 'O\'rnatish'
            }.get(service['service_type'], 'Boshqa')
            
            # Format status
            status_emoji = {
                'pending': '🟡',
                'in_progress': '🟠',
                'completed': '🟢',
                'cancelled': '🔴'
            }.get(service['status'], '⚪')
            
            status_text = {
                'pending': 'Kutilmoqda',
                'in_progress': 'Jarayonda',
                'completed': 'Bajarilgan',
                'cancelled': 'Bekor qilingan'
            }.get(service['status'], 'Noma\'lum')
            
            # Format priority
            priority_emoji = {
                'urgent': '🔴',
                'high': '🟠',
                'normal': '🟡',
                'low': '🟢'
            }.get(service.get('priority', 'normal'), '🟡')
            
            priority_text = {
                'urgent': 'Shoshilinch',
                'high': 'Yuqori',
                'normal': 'O\'rtacha',
                'low': 'Past'
            }.get(service.get('priority', 'normal'), 'O\'rtacha')
            
            # Format date
            created_date = service['created_at'].strftime('%d.%m.%Y %H:%M')
            
            # To'liq ma'lumot
            text = (
                f"{service_type_emoji} <b>{service_type_text} - To'liq ma'lumot</b>\n\n"
                f"🆔 <b>Xizmat ID:</b> {service['id']}\n"
                f"📅 <b>Sana:</b> {created_date}\n"
                f"👤 <b>Mijoz:</b> {service['client_name']}\n"
                f"📞 <b>Telefon:</b> {service['client_phone']}\n"
                f"🏠 <b>Manzil:</b> {service['address']}\n"
                f"📝 <b>Tavsif:</b> {service['description']}\n"
                f"{status_emoji} <b>Holat:</b> {status_text}\n"
                f"{priority_emoji} <b>Ustuvorlik:</b> {priority_text}\n"
                f"⏰ <b>Taxminiy vaqt:</b> {service['estimated_duration']}\n\n"
                f"📊 <b>Xizmat #{index + 1} / {len(services)}</b>"
            )
            
            # Create navigation keyboard
            keyboard = get_technical_service_navigation_keyboard(lang)
            
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer(text, reply_markup=keyboard, parse_mode='HTML')
            else:
                await message_or_callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                
        except Exception as e:
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            else:
                await message_or_callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "ts_prev_service")
    async def show_previous_service(callback: CallbackQuery, state: FSMContext):
        """Show previous service"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_service_index', 0)
            
            services = await get_technical_services()
            
            if current_index > 0:
                new_index = current_index - 1
                await state.update_data(current_service_index=new_index)
                await show_service_details(callback, services[new_index], services, new_index)
            else:
                await callback.answer("Bu birinchi xizmat")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "ts_next_service")
    async def show_next_service(callback: CallbackQuery, state: FSMContext):
        """Show next service"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_service_index', 0)
            
            services = await get_technical_services()
            
            if current_index < len(services) - 1:
                new_index = current_index + 1
                await state.update_data(current_service_index=new_index)
                await show_service_details(callback, services[new_index], services, new_index)
            else:
                await callback.answer("Bu oxirgi xizmat")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    return router

def get_services_navigation_keyboard(current_index: int, total_services: int):
    """Create navigation keyboard for services"""
    keyboard = []
    
    # Navigation row
    nav_buttons = []
    
    # Previous button
    if current_index > 0:
        nav_buttons.append(InlineKeyboardButton(
            text="⬅️ Oldingi",
            callback_data="ts_prev_service"
        ))
    
    # Next button
    if current_index < total_services - 1:
        nav_buttons.append(InlineKeyboardButton(
            text="Keyingi ➡️",
            callback_data="ts_next_service"
        ))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Back to menu
    keyboard.append([InlineKeyboardButton(text="🏠 Bosh sahifaserv", callback_data="back_to_main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_controller_technical_service_router():
    """Get controller technical service router - alias for get_technical_service_router"""
    return get_technical_service_router()
