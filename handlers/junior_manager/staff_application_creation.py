"""
Junior Manager Staff Application Creation Handler - Soddalashtirilgan versiya

Bu modul junior manager uchun xodimlar arizasi yaratish funksionalligini o'z ichiga oladi.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional
from datetime import datetime
from states.staff_application_states import StaffApplicationStates

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
    if "test" in query.lower():
        return [{'id': 123, 'full_name': 'Test Client', 'phone': '+998901234567', 'address': 'Tashkent'}]
    return []

async def create_new_client(client_data: Dict):
    """Mock create new client"""
    print(f"Mock: Creating new client: {client_data}")
    return 456 # Mock client ID

async def get_client_by_id(client_id: int):
    """Mock get client by ID"""
    if client_id == 456:
        return {'id': 456, 'full_name': 'New Test Client', 'phone': '+998909876543', 'address': 'New Address'}
    return None

# Mock application handler
class RoleBasedApplicationHandler:
    """Mock application handler"""
    async def start_application_creation(self, creator_role: str, creator_id: int, application_type: str):
        """Mock start application creation"""
        return {
            'success': True,
            'creator_context': {
                'role': creator_role,
                'id': creator_id,
                'application_type': application_type
            }
        }

# Mock keyboard functions
def get_junior_manager_main_keyboard(lang: str = 'uz'):
    """Mock junior manager main keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📥 Inbox", callback_data="jm_inbox"),
            InlineKeyboardButton(text="📋 Arizalar", callback_data="jm_applications")
        ],
        [
            InlineKeyboardButton(text="🔌 Yangi ariza", callback_data="jm_new_application"),
            InlineKeyboardButton(text="📊 Hisobotlar", callback_data="jm_reports")
        ],
        [
            InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="jm_settings"),
            InlineKeyboardButton(text="🌐 Til", callback_data="jm_language")
        ]
    ])

def get_client_search_menu(lang: str = 'uz'):
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

def get_application_priority_keyboard(lang: str = 'uz'):
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
            InlineKeyboardButton(text="◀️ Orqaga", callback_data="jm_back_to_client_search")
        ]
    ])

def get_application_confirmation_keyboard(lang: str = 'uz'):
    """Mock application confirmation keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="jm_confirm_application"),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="jm_cancel_application")
        ],
        [
            InlineKeyboardButton(text="✏️ Tahrirlash", callback_data="jm_edit_application")
        ]
    ])

# Import states
from states.staff_application_states import StaffApplicationStates

def get_junior_manager_staff_application_router():
    """Get router for junior manager staff application handlers"""
    router = Router()

    @router.message(F.text.in_(["🔌 Ulanish arizasi yaratish"]))
    async def junior_manager_create_connection_request(message: Message, state: FSMContext):
        """Handle connection request creation for junior manager"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await message.answer("Sizda ruxsat yo'q.")
                return

            lang = user.get('language', 'uz')
            
            # Initialize application handler
            app_handler = RoleBasedApplicationHandler()
            
            # Start application creation
            result = await app_handler.start_application_creation(
                creator_role=user['role'],
                creator_id=user['id'],
                application_type='connection_request'
            )
            
            if not result.get('success'):
                await message.answer("Ariza yaratishda xatolik yuz berdi.")
                return
            
            # Show client search menu
            text = """🔌 **Ulanish arizasi yaratish**

Mijozni topish uchun quyidagi usullardan birini tanlang:"""
            
            keyboard = get_client_search_menu(lang)
            
            await message.answer(
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
            # Set state
            await state.set_state(StaffApplicationStates.selecting_client_search_method)
            
        except Exception as e:
            print(f"Error in junior_manager_create_connection_request: {e}")
            await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(F.text.in_(["🔧 Texnik xizmat yaratish"]))
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
                    InlineKeyboardButton(text="🔌 Ulanish arizasi yaratish", callback_data="jm_create_connection"),
                    InlineKeyboardButton(text="📞 Controller bilan bog'lanish", callback_data="jm_contact_controller")
                ],
                [
                    InlineKeyboardButton(text="🔙 Orqaga", callback_data="jm_back_to_main")
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
                text = """📱 **Telefon raqami bilan qidirish**

Mijoz telefon raqamini kiriting:"""
                await state.set_state(StaffApplicationStates.entering_client_phone)
                
            elif search_method == "name":
                text = """👤 **Ism bilan qidirish**

Mijoz ismini kiriting:"""
                await state.set_state(StaffApplicationStates.entering_client_name)
                
            elif search_method == "id":
                text = """🆔 **ID bilan qidirish**

Mijoz ID raqamini kiriting:"""
                await state.set_state(StaffApplicationStates.entering_client_id)
                
            else:
                await callback.answer("Noto'g'ri amal", show_alert=True)
                return
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="🔙 Orqaga", callback_data="jm_back_to_client_search")
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
                        InlineKeyboardButton(text="🔍 Boshqa qidirish", callback_data="jm_client_search_phone")
                    ],
                    [
                        InlineKeyboardButton(text="🔙 Orqaga", callback_data="jm_back_to_client_search")
                    ]
                ])
                
                await message.answer(
                    text,
                    reply_markup=keyboard,
                    parse_mode="Markdown"
                )
            
        except Exception as e:
            print(f"Error in handle_junior_manager_client_phone_input: {e}")
            await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(StaffApplicationStates.entering_client_name)
    async def handle_junior_manager_client_name_input(message: Message, state: FSMContext):
        """Handle client name input"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await message.answer("Sizda ruxsat yo'q.")
                return

            lang = user.get('language', 'uz')
            name = message.text.strip()
            
            # Validate name
            if not name or len(name) < 2:
                await message.answer("❌ Noto'g'ri ism. Iltimos, to'g'ri ism kiriting.")
                return
            
            # Search for client by name
            clients = await search_clients_by_name(name, exact_match=False)
            
            if clients:
                # Client found
                await _simulate_junior_manager_client_found(message, state, None, name, lang)
            else:
                # Client not found, offer to create new
                text = f"""❌ **Mijoz topilmadi**

Ism: {name}

Bu mijoz tizimda mavjud emas. Yangi mijoz qo'shishni xohlaysizmi?"""
                
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="➕ Yangi mijoz qo'shish", callback_data="jm_create_new_client"),
                        InlineKeyboardButton(text="🔍 Boshqa qidirish", callback_data="jm_client_search_name")
                    ],
                    [
                        InlineKeyboardButton(text="🔙 Orqaga", callback_data="jm_back_to_client_search")
                    ]
                ])
                
                await message.answer(
                    text,
                    reply_markup=keyboard,
                    parse_mode="Markdown"
                )
            
        except Exception as e:
            print(f"Error in handle_junior_manager_client_name_input: {e}")
            await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(StaffApplicationStates.entering_client_id)
    async def handle_junior_manager_client_id_input(message: Message, state: FSMContext):
        """Handle client ID input"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await message.answer("Sizda ruxsat yo'q.")
                return

            lang = user.get('language', 'uz')
            client_id = message.text.strip()
            
            # Validate client ID
            try:
                client_id_int = int(client_id)
            except ValueError:
                await message.answer("❌ Noto'g'ri ID. Iltimos, raqam kiriting.")
                return
            
            # Get client by ID
            client = await get_client_by_id(client_id_int)
            
            if client:
                # Client found
                await _simulate_junior_manager_client_found(message, state, None, str(client_id), lang)
            else:
                # Client not found
                text = f"""❌ **Mijoz topilmadi**

ID: {client_id}

Bu ID bilan mijoz tizimda mavjud emas."""
                
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="🔍 Boshqa qidirish", callback_data="jm_client_search_id"),
                        InlineKeyboardButton(text="➕ Yangi mijoz qo'shish", callback_data="jm_create_new_client")
                    ],
                    [
                        InlineKeyboardButton(text="🔙 Orqaga", callback_data="jm_back_to_client_search")
                    ]
                ])
                
                await message.answer(
                    text,
                    reply_markup=keyboard,
                    parse_mode="Markdown"
                )
            
        except Exception as e:
            print(f"Error in handle_junior_manager_client_id_input: {e}")
            await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(StaffApplicationStates.entering_new_client_name)
    async def handle_new_client_name(message: Message, state: FSMContext):
        """Handle new client name input"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await message.answer("Sizda ruxsat yo'q.")
                return

            lang = user.get('language', 'uz')
            name = message.text.strip()
            
            # Validate name
            if not name or len(name) < 2:
                await message.answer("❌ Noto'g'ri ism. Iltimos, to'g'ri ism kiriting.")
                return
            
            # Store name in state
            await state.update_data(new_client_name=name)
            
            text = f"""📝 **Yangi mijoz ma'lumotlari**

👤 **Ism:** {name}

Endi telefon raqamini kiriting:"""
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="🔙 Orqaga", callback_data="jm_back_to_client_search")
                ]
            ])
            
            await message.answer(
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
            # Set state for phone input
            await state.set_state(StaffApplicationStates.entering_new_client_phone)
            
        except Exception as e:
            print(f"Error in handle_new_client_name: {e}")
            await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(StaffApplicationStates.entering_new_client_phone)
    async def handle_new_client_phone(message: Message, state: FSMContext):
        """Handle new client phone input"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await message.answer("Sizda ruxsat yo'q.")
                return

            lang = user.get('language', 'uz')
            phone = message.text.strip()
            
            # Validate phone
            if not phone or len(phone) < 10:
                await message.answer("❌ Noto'g'ri telefon raqam. Iltimos, to'g'ri raqam kiriting.")
                return
            
            # Get stored name
            data = await state.get_data()
            name = data.get('new_client_name', 'N/A')
            
            # Create new client
            client_data = {
                'full_name': name,
                'phone': phone,
                'address': 'Manzil kiritilmagan'
            }
            
            new_client_id = await create_new_client(client_data)
            
            if new_client_id:
                text = f"""✅ **Yangi mijoz qo'shildi**

👤 **Ism:** {name}
📱 **Telefon:** {phone}
🆔 **ID:** {new_client_id}

Endi ariza ma'lumotlarini kiriting:"""
                
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="📝 Ariza ma'lumotlari", callback_data="jm_enter_application_details")
                    ],
                    [
                        InlineKeyboardButton(text="🔙 Orqaga", callback_data="jm_back_to_client_search")
                    ]
                ])
                
                await message.answer(
                    text,
                    reply_markup=keyboard,
                    parse_mode="Markdown"
                )
                
                # Set state for application details
                await state.set_state(StaffApplicationStates.entering_application_details)
                
            else:
                await message.answer("❌ Mijoz qo'shishda xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            
        except Exception as e:
            print(f"Error in handle_new_client_phone: {e}")
            await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "jm_create_new_client")
    async def handle_create_new_client_button(callback: CallbackQuery, state: FSMContext):
        """Handle create new client button"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return

            lang = user.get('language', 'uz')
            
            text = """👤 **Yangi mijoz qo'shish**

Yangi mijoz ismini kiriting:"""
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="🔙 Orqaga", callback_data="jm_back_to_client_search")
                ]
            ])
            
            await callback.message.edit_text(
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
            # Set state for name input
            await state.set_state(StaffApplicationStates.entering_new_client_name)
            
        except Exception as e:
            print(f"Error in handle_create_new_client_button: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    async def _simulate_junior_manager_client_found(message: Message, state: FSMContext, search_msg: Message, 
                                                  search_value: str, lang: str):
        """Simulate client found for junior manager"""
        try:
            # Mock client data
            client_data = {
                'id': 123,
                'full_name': 'Test Client',
                'phone': '+998901234567',
                'address': 'Tashkent, Test Address'
            }
            
            text = f"""✅ **Mijoz topildi**

👤 **Ism:** {client_data['full_name']}
📱 **Telefon:** {client_data['phone']}
📍 **Manzil:** {client_data['address']}
🆔 **ID:** {client_data['id']}

Endi ariza ma'lumotlarini kiriting:"""
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="📝 Ariza ma'lumotlari", callback_data="jm_enter_application_details")
                ],
                [
                    InlineKeyboardButton(text="🔙 Orqaga", callback_data="jm_back_to_client_search")
                ]
            ])
            
            await message.answer(
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
            # Store client data in state
            await state.update_data(selected_client=client_data)
            
            # Set state for application details
            await state.set_state(StaffApplicationStates.entering_application_details)
            
        except Exception as e:
            print(f"Error in _simulate_junior_manager_client_found: {e}")
            await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    return router
