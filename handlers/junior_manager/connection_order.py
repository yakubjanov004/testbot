"""
Junior Manager Connection Order Handler
Manages connection order creation for junior manager
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional
from datetime import datetime
from filters.role_filter import RoleFilter
from states.staff_application_states import StaffApplicationStates
from keyboards.junior_manager_buttons import (
    get_junior_manager_main_keyboard_updated,
    get_client_search_menu_updated,
    get_application_priority_keyboard_updated,
    get_application_confirmation_keyboard_updated
)

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

async def search_clients_by_name(query: str, exact_match: bool = False):
    """Mock search clients by name"""
    return [
        {
            'id': 1,
            'full_name': 'Aziz Karimov',
            'phone': '+998901234567',
            'address': 'Tashkent, Chorsu'
        }
    ]

async def create_new_client(client_data: Dict):
    """Mock create new client"""
    return {
        'id': 1,
        'full_name': client_data.get('name', ''),
        'phone': client_data.get('phone', ''),
        'address': client_data.get('address', '')
    }

async def get_client_by_id(client_id: int):
    """Mock get client by ID"""
    return {
        'id': client_id,
        'full_name': f'Test Client {client_id}',
        'phone': '+998901234567',
        'address': 'Tashkent, Test Address'
    }

class RoleBasedApplicationHandler:
    """Mock role-based application handler"""
    
    async def start_application_creation(self, creator_role: str, creator_id: int, application_type: str):
        """Mock start application creation"""
        return {
            'success': True,
            'application_id': f'APP_{creator_role}_{creator_id}_{application_type}'
        }

def get_junior_manager_main_keyboard(lang: str = 'uz'):
    """Mock junior manager main keyboard"""
    return get_junior_manager_main_keyboard_updated(lang)


def get_client_search_menu(lang: str = 'uz'):
    """Mock client search menu"""
    return get_client_search_menu_updated(lang)


def get_application_priority_keyboard(lang: str = 'uz'):
    """Mock application priority keyboard"""
    return get_application_priority_keyboard_updated(lang)


def get_application_confirmation_keyboard(lang: str = 'uz'):
    """Mock application confirmation keyboard"""
    return get_application_confirmation_keyboard_updated(lang)


def get_junior_manager_connection_order_router():
    """Get junior manager connection order router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("junior_manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(['\ud83d\udd0c Ulanish arizasi yaratish']))
    async def junior_manager_create_connection_request(message: Message, state: FSMContext):
        """Handle junior manager creating connection request"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'junior_manager':
                await message.answer("Sizda ruxsat yo'q.")
                return
            
            lang = user.get('language', 'uz')
            
            # Initialize application creation
            app_handler = RoleBasedApplicationHandler()
            result = await app_handler.start_application_creation(
                creator_role='junior_manager',
                creator_id=user['id'],
                application_type='connection_request'
            )
            
            if result['success']:
                text = (
                    "\ud83d\udd0c <b>Ulanish arizasi yaratish</b>\n\n"
                    "Mijozni qanday qidirishni xohlaysiz?\n\n"
                    "\ud83d\udcf1 Telefon raqami bo'yicha\n"
                    "\ud83d\dc64 Ism bo'yicha\n"
                    "\ud83c\udd94 ID bo'yicha\n"
                    "➕ Yangi mijoz qo'shish"
                )
                
                await message.answer(
                    text,
                    reply_markup=get_client_search_menu(lang),
                    parse_mode='HTML'
                )
            else:
                await message.answer("Ariza yaratishda xatolik yuz berdi")
            
        except Exception as e:
            print(f"Error in junior_manager_create_connection_request: {str(e)}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    @router.message(F.text.in_(['\ud83d\udd27 Texnik xizmat yaratish']))
    async def junior_manager_technical_service_denied(message: Message, state: FSMContext):
        """Handle technical service creation denial for junior manager"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await message.answer("Sizda ruxsat yo'q.")
                return

            lang = user.get('language', 'uz')
            
            text = """❌ **Ruxsat yo'q**

Kichik menejer faqat ulanish arizalarini yarata oladi.
Texnik xizmat arizalarini yaratish uchun controller bilan bog'laning."""
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="\ud83d\udd0c Ulanish arizasi yaratish", callback_data="jm_create_connection"),
                    InlineKeyboardButton(text="\ud83d\udcde Controller bilan bog'lanish", callback_data="jm_contact_controller")
                ],
                [
                    InlineKeyboardButton(text="\ud83d\udd19 Orqaga", callback_data="jm_back_to_main")
                ]
            ])
            
            await message.answer(
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            print(f"Error in junior_manager_technical_service_denied: {e}")
            await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.startswith("jm_client_search_"))
    async def handle_junior_manager_client_search_method(callback: CallbackQuery, state: FSMContext):
        """Handle client search method selection"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return

            lang = user.get('language', 'uz')
            search_method = callback.data.split("_")[-1]
            
            if search_method == "phone":
                text = """\ud83d\udcf1 **Telefon raqami bilan qidirish**

Mijoz telefon raqamini kiriting:"""
                await state.set_state(StaffApplicationStates.entering_client_phone)
                
            elif search_method == "name":
                text = """\ud83d\dc64 **Ism bilan qidirish**

Mijoz ismini kiriting:"""
                await state.set_state(StaffApplicationStates.entering_client_name)
                
            elif search_method == "id":
                text = """\ud83c\udd94 **ID bilan qidirish**

Mijoz ID raqamini kiriting:"""
                await state.set_state(StaffApplicationStates.entering_client_id)
                
            else:
                await callback.answer("Noto'g'ri amal", show_alert=True)
                return
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="\ud83d\udd19 Orqaga", callback_data="jm_back_to_client_search")
                ]
            ])
            
            await callback.message.edit_text(
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            print(f"Error in handle_junior_manager_client_search_method: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "jm_cancel_application_creation")
    async def junior_manager_cancel_application_creation(callback: CallbackQuery, state: FSMContext):
        """Cancel application creation"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return

            lang = user.get('language', 'uz')
            
            # Clear state
            await state.clear()
            
            text = """❌ **Ariza yaratish bekor qilindi**

Boshqa amallar uchun quyidagi tugmalardan foydalaning:"""
            
            keyboard = get_junior_manager_main_keyboard(lang)
            
            await callback.message.edit_text(
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
            await callback.answer("Ariza yaratish bekor qilindi")
            
        except Exception as e:
            print(f"Error in junior_manager_cancel_application_creation: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.message(StaffApplicationStates.entering_client_phone)
    async def handle_junior_manager_client_phone_input(message: Message, state: FSMContext):
        """Handle client phone number input"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await message.answer("Sizda ruxsat yo'q.")
                return

            lang = user.get('language', 'uz')
            phone = message.text.strip()
            
            # Validate phone number
            if not phone or len(phone) < 10:
                await message.answer("❌ Noto'g'ri telefon raqam. Iltimos, to'g'ri raqam kiriting.")
                return
            
            # Search for client by phone
            clients = await search_clients_by_name(phone, exact_match=True)
            
            if clients:
                # Client found
                await _simulate_junior_manager_client_found(message, state, None, phone, lang)
            else:
                # Client not found, offer to create new
                text = f"""❌ **Mijoz topilmadi**

Telefon raqam: {phone}

Bu mijoz tizimda mavjud emas. Yangi mijoz qo'shishni xohlaysizmi?"""
                
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="➕ Yangi mijoz qo'shish", callback_data="jm_create_new_client"),
                        InlineKeyboardButton(text="\ud83d\udd0d Boshqa qidirish", callback_data="jm_client_search_phone")
                    ],
                    [
                        InlineKeyboardButton(text="\ud83d\udd19 Orqaga", callback_data="jm_back_to_client_search")
                    ]
                ])
                
                await message.answer(
                    text,
                    reply_markup=keyboard,
                    parse_mode="Markdown"
                )
        except Exception as e:
            print(f"Error in handle_junior_manager_client_phone_input: {e}")
            await message.answer("Xatolik yuz berdi")

    return router