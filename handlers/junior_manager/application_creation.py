"""
Junior Manager Application Creation Handler - Soddalashtirilgan versiya

Bu modul junior manager uchun ariza yaratish funksionalligini o'z ichiga oladi.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional
import asyncio
import json
from datetime import datetime
from filters.role_filter import RoleFilter

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'junior_manager',
        'language': 'uz',
        'full_name': 'Test Junior Manager',
        'phone_number': '+998901234567'
    }

async def get_user_lang(telegram_id: int):
    """Mock user language"""
    return 'uz'

# Using get_role_router from utils.role_system

async def create_new_client(name: str, phone: str):
    """Mock create new client"""
    return {
        'id': 1,
        'name': name,
        'phone': phone,
        'address': 'Tashkent, Test Address',
        'created_at': datetime.now()
    }

async def create_junior_manager_application(junior_manager_id: int, client_id: int, details: str, priority: str):
    """Mock create junior manager application"""
    return {
        'id': 'app_001',
        'junior_manager_id': junior_manager_id,
        'client_id': client_id,
        'details': details,
        'priority': priority,
        'status': 'pending',
        'created_at': datetime.now()
    }

# Mock keyboard functions
def get_client_search_menu(lang: str):
    """Mock client search menu keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔍 Telefon raqami bilan qidirish", callback_data="search_by_phone"),
            InlineKeyboardButton(text="👤 Ism bilan qidirish", callback_data="search_by_name")
        ],
        [
            InlineKeyboardButton(text="➕ Yangi mijoz qo'shish", callback_data="add_new_client"),
            InlineKeyboardButton(text="🆔 ID bilan qidirish", callback_data="search_by_id")
        ],
        [
            InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_main")
        ]
    ])

def get_application_priority_keyboard(lang: str):
    """Mock application priority keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🟢 Past", callback_data="jm_priority_low"),
            InlineKeyboardButton(text="🟡 O'rta", callback_data="jm_priority_medium")
        ],
        [
            InlineKeyboardButton(text="🟠 Yuqori", callback_data="jm_priority_high"),
            InlineKeyboardButton(text="🔴 Shoshilinch", callback_data="jm_priority_urgent")
        ],
        [
            InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_details")
        ]
    ])

def get_application_confirmation_keyboard(lang: str):
    """Mock application confirmation keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="jm_confirm_application"),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="jm_cancel_application")
        ]
    ])

# Mock states
from aiogram.fsm.state import State, StatesGroup

class JuniorManagerApplicationStates(StatesGroup):
    creating_new_client = State()
    creating_new_client_phone = State()
    entering_application_details = State()
    selecting_priority = State()
    confirming_application = State()

def get_junior_manager_application_creation_router():
    """Get router for junior manager application creation handlers"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("junior_manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🔌 Ulanish arizasi yaratish"]))
    async def start_application_creation(message: Message, state: FSMContext):
        """Start application creation process"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'junior_manager':
                return

            lang = user.get('language', 'uz')
            
            text = "🔍 Mijozni qidirish usulini tanlang:"
            
            await message.answer(
                text,
                reply_markup=get_client_search_menu(lang=lang)
            )
            
        except Exception as e:
            print(f"Error in start_application_creation: {e}")
            await message.answer("Xatolik yuz berdi")

    @router.message(JuniorManagerApplicationStates.creating_new_client)
    async def handle_new_client_name(message: Message, state: FSMContext):
        """Handle new client name input"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'junior_manager':
                return

            lang = user.get('language', 'uz')
            client_name = message.text.strip()
            
            # Store client name in state
            await state.update_data(new_client_name=client_name)
            
            text = f"👤 Mijoz ismi: {client_name}\n\n📱 Endi telefon raqamini kiriting:"
            
            await state.set_state(JuniorManagerApplicationStates.creating_new_client_phone)
            await message.answer(text)
            
        except Exception as e:
            print(f"Error in handle_new_client_name: {e}")
            await message.answer("Xatolik yuz berdi")

    @router.message(JuniorManagerApplicationStates.creating_new_client_phone)
    async def handle_new_client_phone(message: Message, state: FSMContext):
        """Handle new client phone input"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'junior_manager':
                return

            lang = user.get('language', 'uz')
            phone = message.text.strip()
            
            # Get stored client name
            data = await state.get_data()
            client_name = data.get('new_client_name', '')
            
            # Create new client
            new_client = await create_new_client(name=client_name, phone=phone)
            
            if new_client:
                # Store client data in state
                await state.update_data(
                    selected_client=new_client,
                    client_id=new_client['id']
                )
                
                text = f"""✅ Yangi mijoz yaratildi:

👤 {new_client.get('name', 'N/A')}
📱 {new_client.get('phone', 'N/A')}

📝 Endi ariza tafsilotlarini kiriting:"""
                
                await state.set_state(JuniorManagerApplicationStates.entering_application_details)
                await message.answer(text)
            else:
                text = "❌ Mijoz yaratishda xatolik yuz berdi. Qaytadan urinib ko'ring."
                await message.answer(text)
            
        except Exception as e:
            print(f"Error in handle_new_client_phone: {e}")
            await message.answer("Xatolik yuz berdi")

    @router.message(JuniorManagerApplicationStates.entering_application_details)
    async def handle_application_details(message: Message, state: FSMContext):
        """Handle application details input"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'junior_manager':
                return

            lang = user.get('language', 'uz')
            details = message.text.strip()
            
            # Store application details in state
            await state.update_data(application_details=details)
            
            text = "⚡ Ariza ustuvorligini tanlang:"
            
            await message.answer(
                text,
                reply_markup=get_application_priority_keyboard(lang=lang)
            )
            
        except Exception as e:
            print(f"Error in handle_application_details: {e}")
            await message.answer("Xatolik yuz berdi")

    @router.callback_query(F.data.startswith("jm_priority_"))
    async def handle_priority_selection(callback: CallbackQuery, state: FSMContext):
        """Handle priority selection"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return

            lang = user.get('language', 'uz')
            priority = callback.data.split("_")[-1]
            
            # Store priority in state
            await state.update_data(priority=priority)
            
            # Show application confirmation
            await _show_application_confirmation(callback, state, lang)
            
        except Exception as e:
            print(f"Error in handle_priority_selection: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "jm_confirm_application")
    async def handle_application_confirmation(callback: CallbackQuery, state: FSMContext):
        """Handle application confirmation"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return

            lang = user.get('language', 'uz')
            
            # Get application data from state
            data = await state.get_data()
            client = data.get('selected_client')
            details = data.get('application_details')
            priority = data.get('priority')
            
            if not all([client, details, priority]):
                await callback.answer("Ma'lumotlar to'liq emas", show_alert=True)
                return
            
            # Create application
            application = await create_junior_manager_application(
                junior_manager_id=user['id'],
                client_id=client['id'],
                details=details,
                priority=priority
            )
            
            if application:
                text = f"""✅ Ariza muvaffaqiyatli yaratildi!

🆔 Ariza ID: {application['id']}
👤 Mijoz: {client.get('name', 'N/A')}
📱 Telefon: {client.get('phone', 'N/A')}
⚡ Ustuvorlik: {priority}
📝 Tafsilotlar: {details}"""
                
                await callback.message.edit_text(text)
                
                # Clear state
                await state.clear()
                
                print(f"Junior Manager {user['id']} created application {application['id']}")
            else:
                text = "❌ Ariza yaratishda xatolik yuz berdi"
                await callback.answer(text, show_alert=True)
            
        except Exception as e:
            print(f"Error in handle_application_confirmation: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    async def _show_application_confirmation(callback: CallbackQuery, state: FSMContext, lang: str):
        """Show application confirmation with all details"""
        try:
            data = await state.get_data()
            client = data.get('selected_client')
            details = data.get('application_details')
            priority = data.get('priority')
            
            priority_text = {
                'low': 'Past',
                'medium': 'O\'rta',
                'high': 'Yuqori',
                'urgent': 'Shoshilinch'
            }.get(priority, priority)
            
            text = f"""📋 Ariza ma'lumotlari:

👤 Mijoz: {client.get('name', 'N/A')}
📱 Telefon: {client.get('phone', 'N/A')}
📍 Manzil: {client.get('address', 'N/A')}
⚡ Ustuvorlik: {priority_text}
📝 Tafsilotlar: {details}

✅ Ariza yaratishni tasdiqlaysizmi?"""
            
            await callback.message.edit_text(
                text,
                reply_markup=get_application_confirmation_keyboard(lang=lang)
            )
            
        except Exception as e:
            print(f"Error in _show_application_confirmation: {e}")

    return router 