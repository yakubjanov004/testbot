"""
Controller Staff Application Creation Handler - Soddalashtirilgan versiya

Bu modul controller rol uchun ariza yaratish handlerlarini o'z ichiga oladi,
controllerlarga mijozlar uchun ulanish arizalari va texnik xizmat arizalarini yaratish imkonini beradi.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, Optional

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
    """Mock user language"""
    return 'uz'

async def get_role_router(role: str):
    """Mock role router"""
    from aiogram import Router
    return Router()

async def send_and_track(message_func, text: str, user_id: int, **kwargs):
    """Mock send and track"""
    return await message_func(text, **kwargs)

async def edit_and_track(message_func, text: str, user_id: int, **kwargs):
    """Mock edit and track"""
    return await message_func(text, **kwargs)

async def cleanup_user_inline_messages(user_id: int):
    """Mock cleanup function"""
    pass

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

# Mock keyboards
def controllers_main_menu(lang: str):
    """Mock controllers main menu keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔌 Ulanish arizasi", callback_data="connection_request"),
            InlineKeyboardButton(text="🔧 Texnik xizmat", callback_data="technical_service")
        ],
        [
            InlineKeyboardButton(text="📊 Hisobotlar", callback_data="reports"),
            InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="settings")
        ]
    ])

# Import states
from states.staff_application_states import StaffApplicationStates

def get_controller_staff_application_router():
    """Get router for controller staff application creation handlers"""
    from utils.role_system import get_role_router
    router = get_role_router("controller")
    
    # Initialize the role-based application handler
    app_handler = RoleBasedApplicationHandler()
    
    @router.message(F.text.in_(["🔌 Ulanish arizasi yaratish"]))
    async def controller_create_connection_request(message: Message, state: FSMContext):
        """Handle controller creating connection request for client"""
        user_id = message.from_user.id
        
        try:
            await cleanup_user_inline_messages(user_id)
            user = await get_user_by_telegram_id(user_id)
            
            if not user or user['role'] != 'controller':
                error_text = "Sizda controller huquqi yo'q."
                await send_and_track(
                    message.answer,
                    error_text,
                    user_id
                )
                return
            
            lang = user.get('language', 'uz')
            print(f"Controller {user['id']} starting connection request creation")
            
            try:
                # Start application creation process
                result = await app_handler.start_application_creation(
                    creator_role='controller',
                    creator_id=user['id'],
                    application_type='connection_request'
                )
                
                if not result['success']:
                    error_msg = result.get('error_message', 'Unknown error')
                    error_text = f"Xatolik yuz berdi: {error_msg}"
                    await send_and_track(
                        message.answer,
                        error_text,
                        user_id
                    )
                    return
                
                # Store creator context in FSM data
                await state.update_data(
                    creator_context=result['creator_context'],
                    application_type='connection_request'
                )
                
                # Set initial state and prompt for client selection
                await state.set_state(StaffApplicationStates.selecting_client_search_method)
                
                prompt_text = """🔌 Ulanish arizasi yaratish

Mijozni qanday qidirishni xohlaysiz?

📱 Telefon raqami bo'yicha
👤 Ism bo'yicha
🆔 Mijoz ID bo'yicha
➕ Yangi mijoz yaratish"""
                
                # Create inline keyboard for client search options
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="📱 Telefon",
                            callback_data="ctrl_client_search_phone"
                        ),
                        InlineKeyboardButton(
                            text="👤 Ism",
                            callback_data="ctrl_client_search_name"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="🆔 ID",
                            callback_data="ctrl_client_search_id"
                        ),
                        InlineKeyboardButton(
                            text="➕ Yangi",
                            callback_data="ctrl_client_search_new"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="❌ Bekor qilish",
                            callback_data="ctrl_cancel_application_creation"
                        )
                    ]
                ])
                
                await send_and_track(
                    message.answer,
                    prompt_text,
                    user_id,
                    reply_markup=keyboard
                )
                
            except Exception as e:
                print(f"Error in controller_create_connection_request: {e}")
                error_text = "Xatolik yuz berdi"
                await send_and_track(
                    message.answer,
                    error_text,
                    user_id
                )
                
        except Exception as e:
            print(f"Error in controller_create_connection_request: {e}")
            error_text = "Xatolik yuz berdi"
            await send_and_track(
                message.answer,
                error_text,
                user_id
            )
    
    @router.message(F.text.in_(["🔧 Texnik xizmat yaratish"]))
    async def controller_create_technical_service(message: Message, state: FSMContext):
        """Handle controller creating technical service request for client"""
        user_id = message.from_user.id
        
        try:
            await cleanup_user_inline_messages(user_id)
            user = await get_user_by_telegram_id(user_id)
            
            if not user or user['role'] != 'controller':
                error_text = "Sizda controller huquqi yo'q."
                await send_and_track(
                    message.answer,
                    error_text,
                    user_id
                )
                return
            
            lang = user.get('language', 'uz')
            print(f"Controller {user['id']} starting technical service creation")
            
            try:
                # Start application creation process
                result = await app_handler.start_application_creation(
                    creator_role='controller',
                    creator_id=user['id'],
                    application_type='technical_service'
                )
                
                if not result['success']:
                    error_msg = result.get('error_message', 'Unknown error')
                    error_text = f"Xatolik yuz berdi: {error_msg}"
                    await send_and_track(
                        message.answer,
                        error_text,
                        user_id
                    )
                    return
                
                # Store creator context in FSM data
                await state.update_data(
                    creator_context=result['creator_context'],
                    application_type='technical_service'
                )
                
                # Set initial state and prompt for client selection
                await state.set_state(StaffApplicationStates.selecting_client_search_method)
                
                prompt_text = """🔧 Texnik xizmat arizasi yaratish

Mijozni qanday qidirishni xohlaysiz?

📱 Telefon raqami bo'yicha
👤 Ism bo'yicha
🆔 Mijoz ID bo'yicha
➕ Yangi mijoz yaratish"""
                
                # Create inline keyboard for client search options
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="📱 Telefon",
                            callback_data="ctrl_client_search_phone"
                        ),
                        InlineKeyboardButton(
                            text="👤 Ism",
                            callback_data="ctrl_client_search_name"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="🆔 ID",
                            callback_data="ctrl_client_search_id"
                        ),
                        InlineKeyboardButton(
                            text="➕ Yangi",
                            callback_data="ctrl_client_search_new"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="❌ Bekor qilish",
                            callback_data="ctrl_cancel_application_creation"
                        )
                    ]
                ])
                
                await send_and_track(
                    message.answer,
                    prompt_text,
                    user_id,
                    reply_markup=keyboard
                )
                
            except Exception as e:
                print(f"Error in controller_create_technical_service: {e}")
                error_text = "Xatolik yuz berdi"
                await send_and_track(
                    message.answer,
                    error_text,
                    user_id
                )
                
        except Exception as e:
            print(f"Error in controller_create_technical_service: {e}")
            error_text = "Xatolik yuz berdi"
            await send_and_track(
                message.answer,
                error_text,
                user_id
            )
    
    @router.callback_query(F.data.startswith("ctrl_client_search_"))
    async def handle_controller_client_search_method(callback: CallbackQuery, state: FSMContext):
        """Handle client search method selection for controller"""
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            search_method = callback.data.split("_")[-1]  # phone, name, id, new
            
            try:
                # Update FSM data with search method
                await state.update_data(client_search_method=search_method)
                
                if search_method == "phone":
                    await state.set_state(StaffApplicationStates.entering_client_phone)
                    prompt_text = """📱 Mijoz telefon raqamini kiriting:

Masalan: +998901234567"""
                    
                elif search_method == "name":
                    await state.set_state(StaffApplicationStates.entering_client_name)
                    prompt_text = """👤 Mijoz ismini kiriting:

To'liq ism va familiyani kiriting"""
                    
                elif search_method == "id":
                    await state.set_state(StaffApplicationStates.entering_client_id)
                    prompt_text = """🆔 Mijoz ID raqamini kiriting:"""
                    
                elif search_method == "new":
                    prompt_text = """➕ Yangi mijoz yaratish

Yangi mijoz ma'lumotlarini kiritishni boshlaymiz.
Birinchi navbatda, mijoz ismini kiriting:"""
                    await state.set_state(StaffApplicationStates.entering_new_client_name)
                
                await edit_and_track(
                    callback.message.edit_text,
                    prompt_text,
                    user_id
                )
                await callback.answer()
                
            except Exception as e:
                print(f"Error in handle_controller_client_search_method: {e}")
                await callback.answer("Xatolik yuz berdi", show_alert=True)
                
        except Exception as e:
            print(f"Error in handle_controller_client_search_method: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "ctrl_cancel_application_creation")
    async def controller_cancel_application_creation(callback: CallbackQuery, state: FSMContext):
        """Cancel application creation and return to main menu for controller"""
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            
            try:
                await state.clear()
                
                cancel_text = """❌ Ariza yaratish bekor qilindi.

Asosiy menyuga qaytdingiz."""
                
                await edit_and_track(
                    callback.message.edit_text,
                    cancel_text,
                    user_id,
                    reply_markup=None
                )
                
                # Send main menu
                main_menu_text = "Asosiy menyu"
                await send_and_track(
                    callback.message.answer,
                    main_menu_text,
                    user_id,
                    reply_markup=controllers_main_menu(lang)
                )
                
                await callback.answer()
                
            except Exception as e:
                print(f"Error in controller_cancel_application_creation: {e}")
                await callback.answer("Xatolik yuz berdi", show_alert=True)
                
        except Exception as e:
            print(f"Error in controller_cancel_application_creation: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    # Client search input handlers for controller
    @router.message(StaffApplicationStates.entering_client_phone)
    async def handle_controller_client_phone_input(message: Message, state: FSMContext):
        """Handle client phone number input for controller"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await send_and_track(
                    message.answer,
                    "Sizda controller huquqi yo'q.",
                    user_id
                )
                return
            
            lang = user.get('language', 'uz')
            phone = message.text.strip()
            
            try:
                # Basic phone validation
                if not phone.startswith('+') or len(phone) < 10:
                    error_text = """❌ Telefon raqami noto'g'ri formatda.
Iltimos, +998901234567 formatida kiriting."""
                    await send_and_track(
                        message.answer,
                        error_text,
                        user_id
                    )
                    return
                
                # Store phone and search for client
                await state.update_data(client_phone=phone)
                await state.set_state(StaffApplicationStates.searching_client)
                
                search_text = f"🔍 Telefon raqami {phone} bo'yicha mijozni qidiryapman..."
                
                search_msg = await send_and_track(
                    message.answer,
                    search_text,
                    user_id
                )
                
                # For demo purposes, simulate found client
                await _simulate_controller_client_found(message, state, search_msg, phone, lang)
                
            except Exception as e:
                print(f"Error in handle_controller_client_phone_input: {e}")
                error_text = "Xatolik yuz berdi"
                await send_and_track(
                    message.answer,
                    error_text,
                    user_id
                )
                
        except Exception as e:
            print(f"Error in handle_controller_client_phone_input: {e}")
            error_text = "Xatolik yuz berdi"
            await send_and_track(
                message.answer,
                error_text,
                user_id
            )
    
    @router.message(StaffApplicationStates.entering_client_name)
    async def handle_controller_client_name_input(message: Message, state: FSMContext):
        """Handle client name input for controller"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await send_and_track(
                    message.answer,
                    "Sizda controller huquqi yo'q.",
                    user_id
                )
                return
            
            lang = user.get('language', 'uz')
            name = message.text.strip()
            
            try:
                # Basic name validation
                if len(name) < 2:
                    error_text = "❌ Ism juda qisqa. Kamida 2 ta harf bo'lishi kerak."
                    await send_and_track(
                        message.answer,
                        error_text,
                        user_id
                    )
                    return
                
                # Store name and search for client
                await state.update_data(client_name=name)
                await state.set_state(StaffApplicationStates.searching_client)
                
                search_text = f"🔍 '{name}' ismli mijozni qidiryapman..."
                
                search_msg = await send_and_track(
                    message.answer,
                    search_text,
                    user_id
                )
                
                # For demo purposes, simulate found client
                await _simulate_controller_client_found(message, state, search_msg, name, lang)
                
            except Exception as e:
                print(f"Error in handle_controller_client_name_input: {e}")
                error_text = "Xatolik yuz berdi"
                await send_and_track(
                    message.answer,
                    error_text,
                    user_id
                )
                
        except Exception as e:
            print(f"Error in handle_controller_client_name_input: {e}")
            error_text = "Xatolik yuz berdi"
            await send_and_track(
                message.answer,
                error_text,
                user_id
            )
    
    @router.message(StaffApplicationStates.entering_client_id)
    async def handle_controller_client_id_input(message: Message, state: FSMContext):
        """Handle client ID input for controller"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await send_and_track(
                    message.answer,
                    "Sizda controller huquqi yo'q.",
                    user_id
                )
                return
            
            lang = user.get('language', 'uz')
            client_id_str = message.text.strip()
            
            try:
                # Validate ID is numeric
                try:
                    client_id = int(client_id_str)
                except ValueError:
                    error_text = "❌ ID raqam bo'lishi kerak. Masalan: 12345"
                    await send_and_track(
                        message.answer,
                        error_text,
                        user_id
                    )
                    return
                
                # Store ID and search for client
                await state.update_data(client_id=client_id)
                await state.set_state(StaffApplicationStates.searching_client)
                
                search_text = f"🔍 ID {client_id} bo'yicha mijozni qidiryapman..."
                
                search_msg = await send_and_track(
                    message.answer,
                    search_text,
                    user_id
                )
                
                # For demo purposes, simulate found client
                await _simulate_controller_client_found(message, state, search_msg, str(client_id), lang)
                
            except Exception as e:
                print(f"Error in handle_controller_client_id_input: {e}")
                error_text = "Xatolik yuz berdi"
                await send_and_track(
                    message.answer,
                    error_text,
                    user_id
                )
                
        except Exception as e:
            print(f"Error in handle_controller_client_id_input: {e}")
            error_text = "Xatolik yuz berdi"
            await send_and_track(
                message.answer,
                error_text,
                user_id
            )
    
    @router.message(StaffApplicationStates.entering_new_client_name)
    async def handle_new_client_name(message: Message, state: FSMContext):
        """Handle new client name input"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'controller':
                return
            
            lang = user.get('language', 'uz')
            client_name = message.text.strip()
            
            if len(client_name) < 3:
                error_text = "❌ Ism juda qisqa. Kamida 3 ta belgi kiriting."
                await message.answer(error_text)
                return
            
            await state.update_data(new_client_name=client_name)
            
            prompt_text = f"""✅ Mijoz ismi: {client_name}

📱 Endi mijozning telefon raqamini kiriting:
(Masalan: +998901234567)"""
            
            await send_and_track(
                message.answer(prompt_text),
                message.from_user.id
            )
            await state.set_state(StaffApplicationStates.entering_new_client_phone)
            
        except Exception as e:
            print(f"Error in handle_new_client_name: {e}")
            await message.answer("Xatolik yuz berdi")
    
    @router.message(StaffApplicationStates.entering_new_client_phone)
    async def handle_new_client_phone(message: Message, state: FSMContext):
        """Handle new client phone input and create client"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'controller':
                return
            
            lang = user.get('language', 'uz')
            phone = message.text.strip()
            
            # Basic phone validation
            import re
            phone_pattern = re.compile(r'^\+?998[0-9]{9}$')
            clean_phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            
            if not phone_pattern.match(clean_phone):
                error_text = """❌ Noto'g'ri telefon raqam formati.
To'g'ri format: +998901234567"""
                await message.answer(error_text)
                return
            
            # Normalize phone number
            if not clean_phone.startswith('+'):
                clean_phone = '+' + clean_phone
            
            data = await state.get_data()
            client_name = data.get('new_client_name')
            
            # Create mock client
            client_data = {
                'id': 12345,
                'full_name': client_name,
                'phone': clean_phone,
                'role': 'client',
                'language': 'uz',
                'is_active': True,
                'address': 'Tashkent, Uzbekistan'
            }
            
            await state.update_data(selected_client_id=client_data['id'], selected_client=client_data)
            
            success_text = f"""✅ Yangi mijoz muvaffaqiyatli yaratildi!

👤 Ism: {client_name}
📱 Telefon: {clean_phone}

Endi ariza turini tanlang:"""
            
            # Show application type selection
            keyboard = _create_application_type_keyboard(lang)
            await send_and_track(
                message.answer(success_text, reply_markup=keyboard),
                message.from_user.id
            )
            await state.set_state(StaffApplicationStates.selecting_application_type)
                
        except Exception as e:
            print(f"Error in handle_new_client_phone: {e}")
            await message.answer("Xatolik yuz berdi")
            await state.clear()
    
    @router.callback_query(F.data == "create_new_client")
    async def handle_create_new_client_button(callback: CallbackQuery, state: FSMContext):
        """Handle create new client button from search results"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'controller':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            
            prompt_text = """➕ Yangi mijoz yaratish

Mijoz ismini kiriting:"""
            
            await edit_and_track(
                callback.message.edit_text(prompt_text),
                callback.from_user.id
            )
            await state.set_state(StaffApplicationStates.entering_new_client_name)
            await callback.answer()
            
        except Exception as e:
            print(f"Error in handle_create_new_client_button: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    return router


def _create_application_type_keyboard(lang: str):
    """Create application type selection keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔌 Ulanish arizasi",
                callback_data="app_type_connection"
            ),
            InlineKeyboardButton(
                text="🔧 Texnik xizmat",
                callback_data="app_type_technical"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Bekor qilish",
                callback_data="ctrl_cancel_application_creation"
            )
        ]
    ])


async def _simulate_controller_client_found(message: Message, state: FSMContext, search_msg: Message, 
                                          search_value: str, lang: str):
    """
    Simulate client found for controller demo purposes.
    In production, this would be replaced with actual database search logic.
    """
    # Mock client data
    client = {
        'id': 12345,
        'full_name': 'Test Client',
        'phone': '+998901234567',
        'address': 'Tashkent, Uzbekistan',
        'role': 'client',
        'is_active': True
    }
    
    await state.update_data(selected_client=client, selected_client_id=client['id'])
    await state.set_state(StaffApplicationStates.confirming_client_selection)
    
    # Update search message with found client
    found_text = f"""✅ Mijoz topildi!

👤 Ism: {client['full_name']}
📱 Telefon: {client.get('phone', 'N/A')}
📍 Manzil: {client.get('address', 'N/A')}

Bu mijoz uchun ariza yaratishni xohlaysizmi?"""
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Ha, davom etish",
                callback_data="ctrl_confirm_client_selection"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔍 Boshqa mijoz qidirish",
                callback_data="ctrl_search_another_client"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Bekor qilish",
                callback_data="ctrl_cancel_application_creation"
            )
        ]
    ])
    
    await search_msg.edit_text(found_text, reply_markup=keyboard)
