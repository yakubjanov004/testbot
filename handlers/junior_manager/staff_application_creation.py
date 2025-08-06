"""
Junior Manager Staff Application Creation Handler
Manages staff application creation for junior manager
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional
from datetime import datetime
from filters.role_filter import RoleFilter
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
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔌 Ulanish arizasi yaratish", callback_data="create_connection"),
            InlineKeyboardButton(text="🔧 Texnik xizmat yaratish", callback_data="create_technical")
        ],
        [
            InlineKeyboardButton(text="📥 Inbox", callback_data="view_inbox"),
            InlineKeyboardButton(text="📋 Buyurtmalar", callback_data="view_orders")
        ],
        [
            InlineKeyboardButton(text="🔍 Mijoz qidiruv", callback_data="search_clients"),
            InlineKeyboardButton(text="📊 Statistika", callback_data="view_statistics")
        ]
    ])

def get_client_search_menu(lang: str = 'uz'):
    """Mock client search menu"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📱 Telefon raqami", callback_data="search_by_phone"),
            InlineKeyboardButton(text="👤 Ism", callback_data="search_by_name")
        ],
        [
            InlineKeyboardButton(text="🆔 ID", callback_data="search_by_id"),
            InlineKeyboardButton(text="➕ Yangi mijoz", callback_data="create_new_client")
        ],
        [
            InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_main")
        ]
    ])

def get_application_priority_keyboard(lang: str = 'uz'):
    """Mock application priority keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🟢 Past", callback_data="priority_low"),
            InlineKeyboardButton(text="🟡 O'rta", callback_data="priority_medium")
        ],
        [
            InlineKeyboardButton(text="🟠 Yuqori", callback_data="priority_high"),
            InlineKeyboardButton(text="🔴 Shoshilinch", callback_data="priority_urgent")
        ],
        [
            InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_details")
        ]
    ])

def get_application_confirmation_keyboard(lang: str = 'uz'):
    """Mock application confirmation keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="confirm_application"),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_application")
        ]
    ])

def get_junior_manager_staff_application_router():
    """Get junior manager staff application router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("junior_manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🔌 Ulanish arizasi yaratish"]))
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
                    "🔌 <b>Ulanish arizasi yaratish</b>\n\n"
                    "Mijozni qanday qidirishni xohlaysiz?\n\n"
                    "📱 Telefon raqami bo'yicha\n"
                    "👤 Ism bo'yicha\n"
                    "🆔 ID bo'yicha\n"
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
