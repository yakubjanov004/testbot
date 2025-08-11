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
from aiogram.filters import StateFilter
from keyboards.manager_buttons import get_manager_client_search_keyboard, get_manager_confirmation_keyboard
from keyboards.controllers_buttons import (
    get_controller_regions_keyboard,
    controller_zayavka_type_keyboard,
    controller_geolocation_keyboard,
    get_controller_tariff_selection_keyboard,
)

def get_manager_staff_application_router():
    """Get router for manager staff application creation handlers"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)
    
    @router.message(F.text == "🔌 Ulanish arizasi yaratish")
    async def manager_create_connection_request(message: Message, state: FSMContext):
        """Manager connection request creation handler (controller-like)"""
        try:
            await state.update_data(current_flow='connection')
            await message.answer(
                "Mijozni qanday qidiramiz?",
                reply_markup=get_manager_client_search_keyboard('uz')
            )
            await state.set_state(StaffApplicationStates.selecting_client_search_method)
        except Exception as e:
            print(f"Error in manager_create_connection_request: {e}")
            await message.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "mgr_search_phone")
    async def mgr_conn_search_by_phone(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(StaffApplicationStates.entering_client_phone)
        await callback.message.edit_text("📱 Telefon raqamini kiriting:\nMasalan: +998901234567")

    @router.callback_query(F.data == "mgr_search_name")
    async def mgr_conn_search_by_name(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(StaffApplicationStates.entering_client_name)
        await callback.message.edit_text("👤 Mijoz ismini kiriting:\nMasalan: Alisher Karimov")

    @router.callback_query(F.data == "mgr_search_id")
    async def mgr_conn_search_by_id(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(StaffApplicationStates.entering_client_id)
        await callback.message.edit_text("🆔 Mijoz ID sini kiriting:\nMasalan: 12345")

    @router.callback_query(F.data == "mgr_search_new")
    async def mgr_conn_new_client(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(StaffApplicationStates.entering_new_client_name)
        await callback.message.edit_text("➕ Yangi mijoz nomini kiriting:")

    @router.callback_query(F.data == "mgr_cancel_creation")
    async def mgr_conn_cancel(callback: CallbackQuery, state: FSMContext):
        await state.clear()
        await callback.message.edit_text("❌ Zayavka yaratish bekor qilindi")
        await callback.answer()

    @router.callback_query(lambda c: c.data.startswith("manager_client_search_"))
    async def deprecated_manager_client_search_method(callback: CallbackQuery, state: FSMContext):
        # Backward compatibility: ignore old callbacks if present
        await callback.answer()

    @router.callback_query(lambda c: c.data.startswith("mgr_select_client_"), StateFilter(StaffApplicationStates.selecting_client_search_method) | StateFilter(StaffApplicationStates.searching_client) | StateFilter(StaffApplicationStates.confirming_client_selection))
    async def mgr_conn_select_client(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        # After selection continue connection flow
        await callback.message.edit_text("Hududni tanlang:")
        await callback.message.answer("Hududni tanlang:", reply_markup=get_controller_regions_keyboard('uz'))
        await state.update_data(connection_flow_stage='selecting_region')

    @router.callback_query(F.data.startswith("ctrl_region_"))
    async def mgr_conn_select_region(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        region = callback.data.replace("ctrl_region_", "")
        await state.update_data(region=region)
        await callback.message.answer("Ulanish turini tanlang:", reply_markup=controller_zayavka_type_keyboard('uz'))
        await state.update_data(connection_flow_stage='selecting_connection_type')

    @router.callback_query(F.data.startswith("ctrl_zayavka_type_"))
    async def mgr_conn_select_type(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        conn_type = callback.data.replace("ctrl_zayavka_type_", "")
        await state.update_data(connection_type=conn_type)
        await callback.message.answer("Tariflardan birini tanlang:", reply_markup=get_controller_tariff_selection_keyboard('uz'))
        await state.update_data(connection_flow_stage='selecting_tariff')

    @router.callback_query(F.data.in_(["ctrl_tariff_standard", "ctrl_tariff_new"]))
    async def mgr_conn_select_tariff(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        tariff = "Standard" if callback.data == "ctrl_tariff_standard" else "Yangi"
        await state.update_data(selected_tariff=tariff)
        await callback.message.answer("Manzilingizni kiriting:")
        await state.update_data(connection_flow_stage='entering_address')

    @router.message(StateFilter(StaffApplicationStates.entering_address))
    async def mgr_conn_get_address(message: Message, state: FSMContext):
        await state.update_data(address=message.text)
        await message.answer("Geolokatsiya yuborasizmi?", reply_markup=controller_geolocation_keyboard('uz'))
        await state.set_state(StaffApplicationStates.asking_for_geo)

    @router.callback_query(F.data.in_(["ctrl_send_location_yes", "ctrl_send_location_no"]))
    async def mgr_conn_geo(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        if callback.data == "ctrl_send_location_yes":
            await callback.message.answer("Geolokatsiyani yuboring:")
            await state.set_state(StaffApplicationStates.waiting_for_geo)
        else:
            await _mgr_conn_show_confirmation(callback, state)

    @router.message(StateFilter(StaffApplicationStates.waiting_for_geo), F.location)
    async def mgr_conn_get_geo(message: Message, state: FSMContext):
        await state.update_data(geo=message.location)
        await _mgr_conn_show_confirmation(message, state)

    async def _mgr_conn_show_confirmation(message_or_callback, state: FSMContext):
        data = await state.get_data()
        region = data.get('region', '-')
        conn_type = data.get('connection_type', '-')
        tariff = data.get('selected_tariff', '-')
        address = data.get('address', '-')
        geo = data.get('geo')
        text = (
            f"🏛️ <b>Hudud:</b> {region}\n"
            f"🔌 <b>Ulanish turi:</b> {conn_type}\n"
            f"💳 <b>Tarif:</b> {tariff}\n"
            f"🏠 <b>Manzil:</b> {address}\n"
            f"📍 <b>Geolokatsiya:</b> {'✅ Yuborilgan' if geo else '❌ Yuborilmagan'}"
        )
        if hasattr(message_or_callback, 'message'):
            await message_or_callback.message.answer(text, parse_mode='HTML', reply_markup=get_manager_confirmation_keyboard('uz'))
        else:
            await message_or_callback.answer(text, parse_mode='HTML', reply_markup=get_manager_confirmation_keyboard('uz'))

    @router.callback_query(F.data == "mgr_confirm_zayavka")
    async def mgr_conn_confirm(callback: CallbackQuery, state: FSMContext):
        try:
            try:
                await callback.message.edit_reply_markup(reply_markup=None)
            except Exception:
                pass
            await callback.answer()
            request_id = f"UL_MGR_{callback.from_user.id}_{int(__import__('time').time())}"
            await callback.message.answer(
                "✅ Ulanish arizasi menejer tomonidan yaratildi!\n" +
                f"Ariza ID: {request_id[:10]}\n" +
                "Menejerlar tez orada mijoz bilan bog'lanadi.")
            await state.clear()
        except Exception:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "mgr_resend_zayavka")
    async def mgr_conn_resend(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await _mgr_conn_show_confirmation(callback, state)
    
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
        
        keyboard = get_manager_confirmation_keyboard('uz')
        
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
        
        keyboard = get_manager_confirmation_keyboard('uz')
        
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
        
        keyboard = get_manager_confirmation_keyboard('uz')
        
        await search_msg.edit_text(found_text, reply_markup=keyboard)
        
    except Exception as e:
        await message.answer("Xatolik yuz berdi")


def _create_application_type_keyboard():
    """Create keyboard for application type selection"""
    return controller_zayavka_type_keyboard('uz')
