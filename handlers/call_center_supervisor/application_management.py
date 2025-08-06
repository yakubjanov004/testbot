"""
Call Center Supervisor Application Management Handler - Simplified Implementation

This module handles application creation, management and workflow for call center supervisors.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from states.call_center_supervisor_states import CallCenterSupervisorApplicationStates

def get_call_center_supervisor_application_management_router():
    """Get call center supervisor application management router - Simplified Implementation"""
    router = Router()

    @router.callback_query(F.data.startswith("ccs_client_search_"))
    async def handle_client_search_method(callback: CallbackQuery, state: FSMContext):
        """Handle client search method selection"""
        try:
            search_method = callback.data.split("_")[-1]
            
            if search_method == "phone":
                await state.set_state(CallCenterSupervisorApplicationStates.client_search_phone)
                text = "📱 Mijoz telefon raqamini kiriting:\n\nMasalan: +998901234567 yoki 901234567"
                
            elif search_method == "name":
                await state.set_state(CallCenterSupervisorApplicationStates.client_search_name)
                text = "👤 Mijoz ismini kiriting:\n\nTo'liq ism yoki ism qismini yozing"
                
            elif search_method == "id":
                await state.set_state(CallCenterSupervisorApplicationStates.client_search_id)
                text = "🆔 Mijoz ID raqamini kiriting:"
                
            elif search_method == "new":
                await state.set_state(CallCenterSupervisorApplicationStates.creating_new_client)
                text = "➕ Yangi mijoz yaratish\n\nMijozning to'liq ismini kiriting:"
                
            else:
                await callback.answer("❌ Noma'lum usul", show_alert=True)
                return

            await callback.message.edit_text(text)
            await callback.answer()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.message(CallCenterSupervisorApplicationStates.client_search_phone)
    async def handle_client_search_by_phone(message: Message, state: FSMContext):
        """Handle client search by phone number"""
        try:
            phone = message.text.strip()
            
            # Mock search results
            if phone.startswith('+998'):
                clients = [
                    {
                        'id': 1,
                        'full_name': 'Test Client 1',
                        'phone': phone,
                        'address': 'Test Address 1'
                    },
                    {
                        'id': 2,
                        'full_name': 'Test Client 2', 
                        'phone': phone,
                        'address': 'Test Address 2'
                    }
                ]
            else:
                clients = []
            
            if not clients:
                text = f"📱 Telefon raqami '{phone}' bo'yicha mijoz topilmadi.\n\nYangi mijoz yaratishni xohlaysizmi?"
                
                # Store phone for new client creation
                await state.update_data(new_client_phone=phone)
                await state.set_state(CallCenterSupervisorApplicationStates.creating_new_client)
                
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="✅ Ha, yaratish", callback_data="ccs_create_new_client")],
                    [InlineKeyboardButton(text="🔍 Boshqa qidirish", callback_data="ccs_search_again")],
                    [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="ccs_cancel_application_creation")]
                ])
                
                await message.answer(text, reply_markup=keyboard)
                return
            
            # Show found clients
            text = f"📱 Telefon raqami '{phone}' bo'yicha topilgan mijozlar:\n\nKerakli mijozni tanlang:"
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=f"👤 {client['full_name']} - {client['phone']}", callback_data=f"ccs_select_client_{client['id']}")]
                for client in clients
            ])
            
            await message.answer(text, reply_markup=keyboard)
            await state.set_state(CallCenterSupervisorApplicationStates.selecting_client)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(CallCenterSupervisorApplicationStates.client_search_name)
    async def handle_client_search_by_name(message: Message, state: FSMContext):
        """Handle client search by name"""
        try:
            name = message.text.strip()
            
            # Mock search results
            if len(name) > 2:
                clients = [
                    {
                        'id': 3,
                        'full_name': f'{name} Test',
                        'phone': '+998901234567',
                        'address': 'Test Address 3'
                    }
                ]
            else:
                clients = []
            
            if not clients:
                text = f"👤 '{name}' nomi bo'yicha mijoz topilmadi.\n\nBoshqa nom bilan qidirib ko'ring yoki yangi mijoz yarating."
                
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🔍 Boshqa qidirish", callback_data="ccs_search_again")],
                    [InlineKeyboardButton(text="➕ Yangi mijoz", callback_data="ccs_client_search_new")],
                    [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="ccs_cancel_application_creation")]
                ])
                
                await message.answer(text, reply_markup=keyboard)
                return
            
            # Show found clients
            text = f"👤 '{name}' nomi bo'yicha topilgan mijozlar:\n\nKerakli mijozni tanlang:"
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=f"👤 {client['full_name']} - {client['phone']}", callback_data=f"ccs_select_client_{client['id']}")]
                for client in clients
            ])
            
            await message.answer(text, reply_markup=keyboard)
            await state.set_state(CallCenterSupervisorApplicationStates.selecting_client)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(CallCenterSupervisorApplicationStates.client_search_id)
    async def handle_client_search_by_id(message: Message, state: FSMContext):
        """Handle client search by ID"""
        try:
            try:
                client_id = int(message.text.strip())
            except ValueError:
                await message.answer("❌ Noto'g'ri ID format. Faqat raqam kiriting.")
                return
            
            # Mock client data
            client = {
                'id': client_id,
                'full_name': f'Test Client {client_id}',
                'phone': '+998901234567',
                'address': f'Test Address {client_id}'
            }
            
            # Show found client and proceed
            await _proceed_with_selected_client(message, state, client)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data.startswith("ccs_select_client_"))
    async def handle_client_selection(callback: CallbackQuery, state: FSMContext):
        """Handle client selection from search results"""
        try:
            client_id = int(callback.data.split("_")[-1])
            
            # Mock client data
            client = {
                'id': client_id,
                'full_name': f'Test Client {client_id}',
                'phone': '+998901234567',
                'address': f'Test Address {client_id}'
            }
            
            # Proceed with selected client
            await _proceed_with_selected_client(callback.message, state, client)
            await callback.answer()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.message(CallCenterSupervisorApplicationStates.creating_new_client)
    async def handle_new_client_name(message: Message, state: FSMContext):
        """Handle new client name input"""
        try:
            client_name = message.text.strip()
            
            if len(client_name) < 2:
                await message.answer("❌ Ism juda qisqa. Kamida 2 ta harf kiriting.")
                return
            
            # Store client name and ask for phone
            await state.update_data(new_client_name=client_name)
            
            data = await state.get_data()
            if 'new_client_phone' in data:
                # Phone already provided, create client
                await _create_new_client_and_proceed(message, state)
            else:
                # Ask for phone number
                text = f"👤 Mijoz ismi: {client_name}\n\n📱 Endi telefon raqamini kiriting:"
                await message.answer(text)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "ccs_create_new_client")
    async def handle_create_new_client_callback(callback: CallbackQuery, state: FSMContext):
        """Handle create new client callback"""
        try:
            text = "➕ Yangi mijoz yaratish\n\nMijozning to'liq ismini kiriting:"
            
            await callback.message.edit_text(text)
            await state.set_state(CallCenterSupervisorApplicationStates.creating_new_client)
            await callback.answer()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    # Application creation handlers
    @router.message(CallCenterSupervisorApplicationStates.entering_application_details)
    async def handle_application_details(message: Message, state: FSMContext):
        """Handle application details input"""
        try:
            details = message.text.strip()
            
            if len(details) < 10:
                await message.answer("❌ Tavsif juda qisqa. Kamida 10 ta belgi kiriting.")
                return
            
            # Store application details
            await state.update_data(application_details=details)
            
            # Ask for priority
            text = "🎯 Ariza muhimlik darajasini tanlang:"
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔴 Yuqori", callback_data="ccs_priority_high")],
                [InlineKeyboardButton(text="🟡 O'rta", callback_data="ccs_priority_medium")],
                [InlineKeyboardButton(text="🟢 Past", callback_data="ccs_priority_low")]
            ])
            
            await message.answer(text, reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data.startswith("ccs_priority_"))
    async def handle_priority_selection(callback: CallbackQuery, state: FSMContext):
        """Handle priority selection"""
        try:
            priority = callback.data.split("_")[-1]
            
            # Store priority and show confirmation
            await state.update_data(application_priority=priority)
            await _show_application_confirmation(callback, state)
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "ccs_confirm_application")
    async def handle_application_confirmation(callback: CallbackQuery, state: FSMContext):
        """Handle application confirmation and creation"""
        try:
            data = await state.get_data()
            
            # Get application data
            client_id = data.get('selected_client_id')
            application_type = data.get('application_type')
            details = data.get('application_details')
            priority = data.get('application_priority', 'medium')
            
            if not all([client_id, application_type, details]):
                await callback.answer("❌ Ma'lumotlar to'liq emas", show_alert=True)
                return
            
            # Mock application creation
            application_id = 888  # Mock ID
            
            text = f"""
✅ Ariza muvaffaqiyatli yaratildi!

📋 Ariza ID: #{application_id}
👤 Mijoz ID: {client_id}
📝 Tur: {application_type}
🎯 Muhimlik: {priority}

Ariza tegishli xodimga tayinlanadi.
            """
            
            await callback.message.edit_text(text)
            await state.clear()
            await callback.answer()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router


async def _proceed_with_selected_client(message: Message, state: FSMContext, client: dict):
    """Proceed with selected client to application creation"""
    try:
        # Store selected client
        await state.update_data(selected_client_id=client['id'])
        
        # Get application type from state data
        data = await state.get_data()
        application_type = data.get('application_type')
        
        if application_type:
            # Application type already selected, ask for details
            text = f"""
👤 Tanlangan mijoz: {client['full_name']}
📱 Telefon: {client.get('phone', 'N/A')}

📝 {application_type} uchun batafsil tavsif kiriting:
            """
            
            await message.answer(text)
            await state.set_state(CallCenterSupervisorApplicationStates.entering_application_details)
        else:
            # Ask for application type
            text = f"""
👤 Tanlangan mijoz: {client['full_name']}
📱 Telefon: {client.get('phone', 'N/A')}

📋 Ariza turini tanlang:
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔌 Ulanish arizasi", callback_data="ccs_app_type_connection")],
                [InlineKeyboardButton(text="🔧 Texnik xizmat", callback_data="ccs_app_type_service")],
                [InlineKeyboardButton(text="📞 Call Center", callback_data="ccs_app_type_call_center")]
            ])
            
            await message.answer(text, reply_markup=keyboard)
        
    except Exception as e:
        await message.answer("❌ Xatolik yuz berdi")


async def _create_new_client_and_proceed(message: Message, state: FSMContext):
    """Create new client and proceed with application"""
    try:
        data = await state.get_data()
        client_name = data.get('new_client_name')
        client_phone = data.get('new_client_phone')
        
        if not client_name:
            await message.answer("❌ Mijoz ismi topilmadi. Qaytadan boshlang.")
            return
        
        # If phone not provided yet, ask for it
        if not client_phone:
            # Check if current message is phone number
            phone_text = message.text.strip()
            if phone_text and (phone_text.startswith('+') or phone_text.isdigit()):
                client_phone = phone_text
                await state.update_data(new_client_phone=client_phone)
            else:
                await message.answer("📱 Telefon raqamini kiriting:")
                return
        
        # Mock client creation
        client_id = 999  # Mock client ID
        
        # Get created client and proceed
        client = {
            'id': client_id,
            'full_name': client_name,
            'phone': client_phone,
            'address': 'Yangi mijoz'
        }
        
        await _proceed_with_selected_client(message, state, client)
        
    except Exception as e:
        await message.answer("❌ Xatolik yuz berdi")


async def _show_application_confirmation(callback: CallbackQuery, state: FSMContext):
    """Show application confirmation"""
    try:
        data = await state.get_data()
        
        client_id = data.get('selected_client_id')
        application_type = data.get('application_type')
        details = data.get('application_details')
        priority = data.get('application_priority')
        
        # Mock client info
        client_name = f'Test Client {client_id}' if client_id else 'Noma\'lum'
        
        priority_text = {
            'high': 'Yuqori',
            'medium': 'O\'rta',
            'low': 'Past'
        }.get(priority, priority)
        
        text = f"""
📋 Ariza tasdiqlash

👤 Mijoz: {client_name}
📝 Tur: {application_type}
🎯 Muhimlik: {priority_text}
📄 Tavsif: {details}

Arizani yaratishni tasdiqlaysizmi?
        """
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="ccs_confirm_application")],
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="ccs_cancel_application_creation")]
        ])
        
        await callback.message.edit_text(text, reply_markup=keyboard)
        await state.set_state(CallCenterSupervisorApplicationStates.confirming_application)
        
    except Exception as e:
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)