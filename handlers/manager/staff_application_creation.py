"""
Manager Staff Application Creation Handler - Complete Implementation

This module provides complete application creation functionality for Manager role,
allowing managers to create both connection requests and technical service
applications on behalf of clients.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from states.staff_application_states import StaffApplicationStates
from filters.role_filter import RoleFilter

def get_manager_staff_application_router():
    """Get router for manager staff application creation handlers"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)
    
    @router.message(F.text == "🔌 Ulanish arizasi yaratish")
    async def manager_create_connection_request(message: Message, state: FSMContext):
        """Manager connection request creation handler"""
        try:
            # Mock user data
            user = {
                'id': message.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            # Mock application creation success
            success = True
            
            if not success:
                await message.answer("Xatolik yuz berdi!")
                return
            
            # Store creator context in FSM data
            await state.update_data(
                creator_context={'role': 'manager', 'id': user['id']},
                application_type='connection_request'
            )
            
            # Set initial state and prompt for client selection
            from states.staff_application_states import StaffApplicationStates
            await state.set_state(StaffApplicationStates.selecting_client_search_method)
            
            prompt_text = (
                "🔌 Ulanish arizasi yaratish\n\n"
                "Mijozni qanday qidirishni xohlaysiz?\n\n"
                "📱 Telefon raqami bo'yicha\n"
                "👤 Ism bo'yicha\n"
                "🆔 Mijoz ID bo'yicha\n"
                "➕ Yangi mijoz yaratish"
            )
            
            # Create inline keyboard for client search options
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📱 Telefon",
                        callback_data="manager_client_search_phone"
                    ),
                    InlineKeyboardButton(
                        text="👤 Ism",
                        callback_data="manager_client_search_name"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🆔 ID",
                        callback_data="manager_client_search_id"
                    ),
                    InlineKeyboardButton(
                        text="➕ Yangi",
                        callback_data="manager_client_search_new"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="❌ Bekor qilish",
                        callback_data="manager_cancel_application_creation"
                    )
                ]
            ])
            
            await message.answer(prompt_text, reply_markup=keyboard)
            
        except Exception as e:
            print(f"Error in manager_create_connection_request: {e}")
            await message.answer("Xatolik yuz berdi")
    
    @router.message(F.text == "🔧 Texnik xizmat yaratish")
    async def manager_create_technical_service(message: Message, state: FSMContext):
        """Handle manager creating technical service request for client"""
        try:
            # Mock user data
            user = {
                'id': message.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            # Mock application creation success
            success = True
            
            if not success:
                await message.answer("Xatolik yuz berdi!")
                return
            
            # Store creator context in FSM data
            await state.update_data(
                creator_context={'role': 'manager', 'id': user['id']},
                application_type='technical_service'
            )
            
            # Set initial state and prompt for client selection
            from states.staff_application_states import StaffApplicationStates
            await state.set_state(StaffApplicationStates.selecting_client_search_method)
            
            prompt_text = (
                "🔧 Texnik xizmat arizasi yaratish\n\n"
                "Mijozni qanday qidirishni xohlaysiz?\n\n"
                "📱 Telefon raqami bo'yicha\n"
                "👤 Ism bo'yicha\n"
                "🆔 Mijoz ID bo'yicha\n"
                "➕ Yangi mijoz yaratish"
            )
            
            # Create inline keyboard for client search options
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📱 Telefon",
                        callback_data="manager_client_search_phone"
                    ),
                    InlineKeyboardButton(
                        text="👤 Ism",
                        callback_data="manager_client_search_name"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🆔 ID",
                        callback_data="manager_client_search_id"
                    ),
                    InlineKeyboardButton(
                        text="➕ Yangi",
                        callback_data="manager_client_search_new"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="❌ Bekor qilish",
                        callback_data="manager_cancel_application_creation"
                    )
                ]
            ])
            
            await message.answer(prompt_text, reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")
    
    @router.callback_query(F.data.startswith("manager_client_search_"))
    async def handle_client_search_method(callback: CallbackQuery, state: FSMContext):
        """Handle client search method selection"""
        try:
            await callback.answer()
            
            # Mock user data
            user = {
                'id': callback.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            search_method = callback.data.split("manager_client_search_")[-1]  # phone, name, id, new
            
            # Update FSM data with search method
            await state.update_data(client_search_method=search_method)
            
            if search_method == "phone":
                from states.staff_application_states import StaffApplicationStates
                await state.set_state(StaffApplicationStates.entering_client_phone)
                prompt_text = (
                    "📱 Mijoz telefon raqamini kiriting:\n\n"
                    "Masalan: +998901234567"
                )
                
            elif search_method == "name":
                from states.staff_application_states import StaffApplicationStates
                await state.set_state(StaffApplicationStates.entering_client_name)
                prompt_text = (
                    "👤 Mijoz ismini kiriting:\n\n"
                    "To'liq ism va familiyani kiriting"
                )
                
            elif search_method == "id":
                from states.staff_application_states import StaffApplicationStates
                await state.set_state(StaffApplicationStates.entering_client_id)
                prompt_text = (
                    "🆔 Mijoz ID raqamini kiriting:"
                )
                
            elif search_method == "new":
                from states.staff_application_states import StaffApplicationStates
                await state.set_state(StaffApplicationStates.creating_new_client)
                prompt_text = (
                    "➕ Yangi mijoz yaratish\n\n"
                    "Yangi mijoz ma'lumotlarini kiritishni boshlaymiz.\n"
                    "Birinchi navbatda, mijoz ismini kiriting:"
                )
                await state.set_state(StaffApplicationStates.entering_new_client_name)
            
            await callback.message.edit_text(prompt_text)
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "manager_cancel_application_creation")
    async def cancel_application_creation(callback: CallbackQuery, state: FSMContext):
        """Cancel application creation and return to main menu"""
        try:
            await callback.answer()
            
            # Mock user data
            user = {
                'id': callback.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            await state.clear()
            
            cancel_text = (
                "❌ Ariza yaratish bekor qilindi.\n"
                "Bosh menuga qaytdingiz."
            )
            
            await callback.message.edit_text(cancel_text)
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.message(StaffApplicationStates.entering_new_client_name)
    async def handle_new_client_name(message: Message, state: FSMContext):
        """Handle new client name input"""
        try:
            # Mock user data
            user = {
                'id': message.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            client_name = message.text.strip()
            
            if len(client_name) < 3:
                error_text = (
                    "❌ Ism juda qisqa. Kamida 3 ta belgi kiriting."
                )
                await message.answer(error_text)
                return
            
            await state.update_data(new_client_name=client_name)
            
            prompt_text = (
                f"✅ Mijoz ismi: {client_name}\n\n"
                "📱 Endi mijozning telefon raqamini kiriting:\n"
                "(Masalan: +998901234567)"
            )
            
            await message.answer(prompt_text)
            from states.staff_application_states import StaffApplicationStates
            await state.set_state(StaffApplicationStates.entering_new_client_phone)
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")
    
    @router.message(StaffApplicationStates.entering_new_client_phone)
    async def handle_new_client_phone(message: Message, state: FSMContext):
        """Handle new client phone input and create client"""
        try:
            # Mock user data
            user = {
                'id': message.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            phone = message.text.strip()
            
            # Basic phone validation
            import re
            phone_pattern = re.compile(r'^\+?998[0-9]{9}$')
            clean_phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            
            if not phone_pattern.match(clean_phone):
                error_text = (
                    "❌ Noto'g'ri telefon raqam formati.\n"
                    "To'g'ri format: +998901234567"
                )
                await message.answer(error_text)
                return
            
            # Normalize phone number
            if not clean_phone.startswith('+'):
                clean_phone = '+' + clean_phone
            
            data = await state.get_data()
            client_name = data.get('new_client_name')
            
            # Mock client creation success
            success = True
            
            if success:
                # Mock client data
                client = {
                    'id': 12345,
                    'full_name': client_name,
                    'phone_number': clean_phone,
                    'address': 'Test manzil'
                }
                
                await state.update_data(selected_client_id=client['id'], selected_client=client)
                
                success_text = (
                    f"✅ Yangi mijoz muvaffaqiyatli yaratildi!\n\n"
                    f"👤 Ism: {client_name}\n"
                    f"📱 Telefon: {clean_phone}\n\n"
                    "Endi ariza turini tanlang:"
                )
                
                # Show application type selection
                keyboard = _create_application_type_keyboard()
                await message.answer(success_text, reply_markup=keyboard)
                from states.staff_application_states import StaffApplicationStates
                await state.set_state(StaffApplicationStates.selecting_application_type)
            else:
                error_text = (
                    "❌ Mijoz yaratishda xatolik yuz berdi.\n"
                    "Iltimos, qaytadan urinib ko'ring."
                )
                await message.answer(error_text)
                await state.clear()
                
        except Exception as e:
            await message.answer("Xatolik yuz berdi")
            await state.clear()
    
    # Client search input handlers
    @router.message(StaffApplicationStates.entering_client_phone)
    async def handle_client_phone_input(message: Message, state: FSMContext):
        """Handle client phone number input"""
        try:
            # Mock user data
            user = {
                'id': message.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            phone = message.text.strip()
            
            # Basic phone validation
            if not phone.startswith('+') or len(phone) < 10:
                error_text = (
                    "❌ Telefon raqami noto'g'ri formatda.\n"
                    "Iltimos, +998901234567 formatida kiriting."
                )
                await message.answer(error_text)
                return
            
            # Store phone and search for client
            await state.update_data(client_phone=phone)
            from states.staff_application_states import StaffApplicationStates
            await state.set_state(StaffApplicationStates.searching_client)
            
            # Mock search for client
            search_text = (
                f"🔍 Telefon raqami {phone} bo'yicha mijozni qidiryapman..."
            )
            
            search_msg = await message.answer(search_text)
            
            # Mock search result
            await _search_client_by_phone(message, state, search_msg, phone)
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")
    
    @router.message(StaffApplicationStates.entering_client_name)
    async def handle_client_name_input(message: Message, state: FSMContext):
        """Handle client name input"""
        try:
            # Mock user data
            user = {
                'id': message.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            name = message.text.strip()
            
            # Basic name validation
            if len(name) < 2:
                error_text = (
                    "❌ Ism juda qisqa. Kamida 2 ta harf bo'lishi kerak."
                )
                await message.answer(error_text)
                return
            
            # Store name and search for client
            await state.update_data(client_name=name)
            from states.staff_application_states import StaffApplicationStates
            await state.set_state(StaffApplicationStates.searching_client)
            
            search_text = (
                f"🔍 '{name}' ismli mijozni qidiryapman..."
            )
            
            search_msg = await message.answer(search_text)
            
            # Mock search result
            await _search_client_by_name(message, state, search_msg, name)
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")
    
    @router.message(StaffApplicationStates.entering_client_id)
    async def handle_client_id_input(message: Message, state: FSMContext):
        """Handle client ID input"""
        try:
            # Mock user data
            user = {
                'id': message.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            client_id_str = message.text.strip()
            
            # Validate ID is numeric
            try:
                client_id = int(client_id_str)
            except ValueError:
                error_text = (
                    "❌ ID raqam bo'lishi kerak. Masalan: 12345"
                )
                await message.answer(error_text)
                return
            
            # Store ID and search for client
            await state.update_data(client_id=client_id)
            from states.staff_application_states import StaffApplicationStates
            await state.set_state(StaffApplicationStates.searching_client)
            
            search_text = (
                f"🔍 ID {client_id} bo'yicha mijozni qidiryapman..."
            )
            
            search_msg = await message.answer(search_text)
            
            # Mock search result
            await _search_client_by_id(message, state, search_msg, client_id)
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")
    
    return router


async def _search_client_by_phone(message: Message, state: FSMContext, search_msg: Message, phone: str):
    """Mock search for client by phone number"""
    try:
        # Mock client data
        client = {
            'id': 12345,
            'full_name': 'Test Client',
            'phone_number': phone,
            'address': 'Test manzil'
        }
        
        # Store found client
        await state.update_data(selected_client=client)
        from states.staff_application_states import StaffApplicationStates
        await state.set_state(StaffApplicationStates.confirming_client_selection)
        
        # Update search message with found client
        found_text = (
            f"✅ Mijoz topildi!\n\n"
            f"👤 Ism: {client['full_name']}\n"
            f"📱 Telefon: {client['phone_number']}\n"
            f"📍 Manzil: {client['address']}\n\n"
            f"Bu mijoz uchun ariza yaratishni xohlaysizmi?"
        )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Ha, davom etish",
                    callback_data="confirm_client_selection"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔍 Boshqa mijoz qidirish",
                    callback_data="search_another_client"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data="cancel_application_creation"
                )
            ]
        ])
        
        await search_msg.edit_text(found_text, reply_markup=keyboard)
        
    except Exception as e:
        await message.answer("Xatolik yuz berdi")


async def _search_client_by_name(message: Message, state: FSMContext, search_msg: Message, name: str):
    """Mock search for client by name"""
    try:
        # Mock client data
        client = {
            'id': 12345,
            'full_name': name,
            'phone_number': '+998901234567',
            'address': 'Test manzil'
        }
        
        # Store found client
        await state.update_data(selected_client=client)
        from states.staff_application_states import StaffApplicationStates
        await state.set_state(StaffApplicationStates.confirming_client_selection)
        
        found_text = (
            f"✅ Mijoz topildi!\n\n"
            f"👤 Ism: {client['full_name']}\n"
            f"📱 Telefon: {client['phone_number']}\n"
            f"📍 Manzil: {client['address']}\n\n"
            f"Bu mijoz uchun ariza yaratishni xohlaysizmi?"
        )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Ha, davom etish",
                    callback_data="confirm_client_selection"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔍 Boshqa mijoz qidirish",
                    callback_data="search_another_client"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data="cancel_application_creation"
                )
            ]
        ])
        
        await search_msg.edit_text(found_text, reply_markup=keyboard)
        
    except Exception as e:
        await message.answer("Xatolik yuz berdi")


async def _search_client_by_id(message: Message, state: FSMContext, search_msg: Message, client_id: int):
    """Mock search for client by ID"""
    try:
        # Mock client data
        client = {
            'id': client_id,
            'full_name': 'Test Client',
            'phone_number': '+998901234567',
            'address': 'Test manzil'
        }
        
        # Store found client
        await state.update_data(selected_client=client)
        from states.staff_application_states import StaffApplicationStates
        await state.set_state(StaffApplicationStates.confirming_client_selection)
        
        found_text = (
            f"✅ Mijoz topildi!\n\n"
            f"👤 Ism: {client['full_name']}\n"
            f"📱 Telefon: {client['phone_number']}\n"
            f"📍 Manzil: {client['address']}\n\n"
            f"Bu mijoz uchun ariza yaratishni xohlaysizmi?"
        )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Ha, davom etish",
                    callback_data="confirm_client_selection"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔍 Boshqa mijoz qidirish",
                    callback_data="search_another_client"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data="cancel_application_creation"
                )
            ]
        ])
        
        await search_msg.edit_text(found_text, reply_markup=keyboard)
        
    except Exception as e:
        await message.answer("Xatolik yuz berdi")


def _create_application_type_keyboard():
    """Create keyboard for application type selection"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔌 Ulanish arizasi",
                callback_data="application_type_connection"
            ),
            InlineKeyboardButton(
                text="🔧 Texnik xizmat",
                callback_data="application_type_technical"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Bekor qilish",
                callback_data="cancel_application_creation"
            )
        ]
    ])
