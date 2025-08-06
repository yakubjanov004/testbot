"""
Junior Manager Client Search Handler - Soddalashtirilgan versiya

Bu modul junior manager uchun mijoz qidirish funksionalligini o'z ichiga oladi.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional
import asyncio
import json
from datetime import datetime
from utils.role_system import get_role_router

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

async def cleanup_user_inline_messages(user_id: int):
    """Mock cleanup function"""
    pass

async def send_and_track(message_func, text: str, user_id: int, **kwargs):
    """Mock send and track"""
    return await message_func(text, **kwargs)

async def edit_and_track(message_func, text: str, user_id: int, **kwargs):
    """Mock edit and track"""
    return await message_func(text, **kwargs)
            
async def search_clients_by_phone(phone: str):
    """Mock search clients by phone"""
    return [
        {
            'id': 1,
            'name': 'Aziz Karimov',
            'phone': phone,
            'address': 'Tashkent, Chorsu'
        },
        {
            'id': 2,
            'name': 'Aziza Azizova',
            'phone': phone,
            'address': 'Tashkent, Yunusabad'
        }
    ]

async def search_clients_by_name(name: str):
    """Mock search clients by name"""
    return [
        {
            'id': 1,
            'name': name,
            'phone': '+998901234567',
            'address': 'Tashkent, Chorsu'
        }
    ]

async def get_client_by_id(client_id: int):
    """Mock get client by ID"""
    return {
        'id': client_id,
        'name': 'Test Client',
        'phone': '+998901234567',
        'address': 'Tashkent, Test Address'
    }

async def create_new_client(name: str, phone: str):
    """Mock create new client"""
    return {
        'id': 999,
        'name': name,
        'phone': phone,
        'address': 'Tashkent, New Address',
        'created_at': datetime.now()
    }

# Mock keyboard functions
def get_client_search_menu(lang: str):
    """Mock client search menu keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔍 Telefon raqami bilan qidirish", callback_data="jm_client_search_phone"),
            InlineKeyboardButton(text="👤 Ism bilan qidirish", callback_data="jm_client_search_name")
        ],
        [
            InlineKeyboardButton(text="➕ Yangi mijoz qo'shish", callback_data="jm_add_new_client"),
            InlineKeyboardButton(text="🆔 ID bilan qidirish", callback_data="jm_client_search_id")
        ],
        [
            InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_main")
        ]
    ])

def get_client_selection_keyboard(clients: List[Dict], lang: str = 'uz'):
    """Mock client selection keyboard"""
    keyboard_buttons = []
    
    for client in clients:
        button_text = f"👤 {client.get('name', 'N/A')} - {client.get('phone', 'N/A')}"
        keyboard_buttons.append([
            InlineKeyboardButton(
                text=button_text,
                callback_data=f"jm_select_client_{client['id']}"
            )
        ])
    
    # Navigation buttons
    keyboard_buttons.append([
        InlineKeyboardButton(text="◀️ Orqaga", callback_data="jm_back_to_search"),
        InlineKeyboardButton(text="➕ Yangi mijoz", callback_data="jm_add_new_client")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

# Mock states
from aiogram.fsm.state import State, StatesGroup

class JuniorManagerApplicationStates(StatesGroup):
    client_search_phone = State()
    client_search_name = State()
    client_search_id = State()
    entering_application_details = State()

def get_junior_manager_client_search_router():
    """Get router for junior manager client search handlers"""
    router = get_role_router("junior_manager")

    @router.callback_query(F.data.startswith("jm_client_search_"))
    async def handle_client_search_method(callback: CallbackQuery, state: FSMContext):
        """Handle client search method selection"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return

            lang = user.get('language', 'uz')
            search_method = callback.data.split("_")[-1]
            
            if search_method == "phone":
                await state.set_state(JuniorManagerApplicationStates.client_search_phone)
                text = """📱 Mijoz telefon raqamini kiriting:

💡 Masalan: +998901234567"""
            elif search_method == "name":
                await state.set_state(JuniorManagerApplicationStates.client_search_name)
                text = """👤 Mijoz ismini kiriting:

💡 Masalan: Aziz Azizov"""
            elif search_method == "id":
                await state.set_state(JuniorManagerApplicationStates.client_search_id)
                text = """🆔 Mijoz ID raqamini kiriting:

💡 Masalan: 12345"""
            else:
                await callback.answer("Noto'g'ri qidiruv usuli", show_alert=True)
                return

            await edit_and_track(
                callback.message.edit_text(text),
                callback.from_user.id
            )
            
        except Exception as e:
            print(f"Error in handle_client_search_method: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.message(JuniorManagerApplicationStates.client_search_phone)
    async def handle_client_search_by_phone(message: Message, state: FSMContext):
        """Handle client search by phone number"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'junior_manager':
                return

            lang = user.get('language', 'uz')
            phone = message.text.strip()
            
            # Search for clients
            clients = await search_clients_by_phone(phone)
            
            if clients:
                text = f"📱 '{phone}' raqami bo'yicha {len(clients)} ta mijoz topildi:\n\n"
                
                await edit_and_track(
                    message.answer(
                        text,
                        reply_markup=get_client_selection_keyboard(clients, lang=lang)
                    ),
                    message.from_user.id
                )
            else:
                text = f"""❌ '{phone}' raqami bo'yicha mijoz topilmadi.

🆕 Yangi mijoz qo'shishni xohlaysizmi?"""
                
                await edit_and_track(
                    message.answer(
                        text,
                        reply_markup=get_client_search_menu(lang=lang)
                    ),
                    message.from_user.id
                )
            
        except Exception as e:
            print(f"Error in handle_client_search_by_phone: {e}")
            await message.answer("Xatolik yuz berdi")

    @router.message(JuniorManagerApplicationStates.client_search_name)
    async def handle_client_search_by_name(message: Message, state: FSMContext):
        """Handle client search by name"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'junior_manager':
                return

            lang = user.get('language', 'uz')
            name = message.text.strip()
            
            # Search for clients
            clients = await search_clients_by_name(name)
            
            if clients:
                text = f"👤 '{name}' ismi bo'yicha {len(clients)} ta mijoz topildi:\n\n"
                
                await edit_and_track(
                    message.answer(
                        text,
                        reply_markup=get_client_selection_keyboard(clients, lang=lang)
                    ),
                    message.from_user.id
                )
            else:
                text = f"""❌ '{name}' ismi bo'yicha mijoz topilmadi.

🆕 Yangi mijoz qo'shishni xohlaysizmi?"""
                
                await edit_and_track(
                    message.answer(
                        text,
                        reply_markup=get_client_search_menu(lang=lang)
                    ),
                    message.from_user.id
                )
            
        except Exception as e:
            print(f"Error in handle_client_search_by_name: {e}")
            await message.answer("Xatolik yuz berdi")

    @router.message(JuniorManagerApplicationStates.client_search_id)
    async def handle_client_search_by_id(message: Message, state: FSMContext):
        """Handle client search by ID"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'junior_manager':
                return

            lang = user.get('language', 'uz')
            client_id = message.text.strip()
            
            try:
                client_id_int = int(client_id)
                client = await get_client_by_id(client_id_int)
                
                if client:
                    text = f"""🆔 Mijoz ID: {client_id} topildi:

👤 Ism: {client.get('name', 'N/A')}
📱 Telefon: {client.get('phone', 'N/A')}
📍 Manzil: {client.get('address', 'N/A')}"""
                    
                    await edit_and_track(
                        message.answer(
                            text,
                            reply_markup=get_client_selection_keyboard([client], lang=lang)
                        ),
                        message.from_user.id
                    )
                else:
                    text = f"""❌ Mijoz ID: {client_id} topilmadi.

🆕 Yangi mijoz qo'shishni xohlaysizmi?"""
                    
                    await edit_and_track(
                        message.answer(
                            text,
                            reply_markup=get_client_search_menu(lang=lang)
                        ),
                        message.from_user.id
                    )
            except ValueError:
                text = "❌ Noto'g'ri ID format. Faqat raqam kiriting."
                await message.answer(text)
            
        except Exception as e:
            print(f"Error in handle_client_search_by_id: {e}")
            await message.answer("Xatolik yuz berdi")

    @router.callback_query(F.data.startswith("jm_select_client_"))
    async def handle_client_selection(callback: CallbackQuery, state: FSMContext):
        """Handle client selection from search results"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return

            lang = user.get('language', 'uz')
            client_id = int(callback.data.split("_")[-1])
            
            # Get client details
            client = await get_client_by_id(client_id)
            if not client:
                await callback.answer("Mijoz topilmadi", show_alert=True)
                return
            
            # Store client data in state
            await state.update_data(
                selected_client=client,
                client_id=client_id
            )
            
            # Proceed to application creation
            await _proceed_with_selected_client(callback.message, state, client, lang)
            
        except Exception as e:
            print(f"Error in handle_client_selection: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    async def _proceed_with_selected_client(message: Message, state: FSMContext, client: Dict[str, Any], lang: str):
        """Proceed with selected client for application creation"""
        try:
            text = f"""✅ Mijoz tanlandi:

👤 {client.get('name', 'N/A')}
📱 {client.get('phone', 'N/A')}
📍 {client.get('address', 'N/A')}

📝 Endi ariza tafsilotlarini kiriting:"""
            
            await state.set_state(JuniorManagerApplicationStates.entering_application_details)
            await edit_and_track(
                message.edit_text(text),
                message.chat.id
            )
            
        except Exception as e:
            print(f"Error in _proceed_with_selected_client: {e}")

    return router 