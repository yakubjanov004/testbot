"""
Junior Manager Inbox - Simplified Implementation

This module handles junior manager inbox functionality.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.junior_manager_buttons import get_junior_manager_back_keyboard
from datetime import datetime
from filters.role_filter import RoleFilter
from states.junior_manager_states import JuniorManagerStates

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

async def get_junior_manager_applications(user_id: int):
    """Mock get junior manager applications"""
    return [
        {
            'id': 'req_001_2024_01_15',
            'workflow_type': 'connection_request',
            'current_status': 'pending',
            'contact_info': {
                'full_name': 'Aziz Karimov',
                'phone': '+998901234567'
            },
            'created_at': datetime.now(),
            'description': 'Yangi internet ulanish',
            'location': 'Tashkent, Chorsu',
            'priority': 'high',
            'region': 'Toshkent shahri',
            'address': 'Chorsu tumani, 15-uy'
        },
        {
            'id': 'req_002_2024_01_16',
            'workflow_type': 'technical_service',
            'current_status': 'in_progress',
            'contact_info': {
                'full_name': 'Malika Toshmatova',
                'phone': '+998901234568'
            },
            'created_at': datetime.now(),
            'description': 'Internet tezligi sekin',
            'location': 'Tashkent, Yunusabad',
            'priority': 'normal',
            'region': 'Toshkent shahri',
            'address': 'Yunusobod tumani, 25-uy'
        }
    ]

def get_junior_manager_inbox_router():
    """Router for junior manager inbox functionality"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("junior_manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["📥 Inbox", "📥 Входящие"]))
    async def view_inbox(message: Message, state: FSMContext):
        """Junior manager view inbox handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                return
            
            lang = user.get('language', 'uz')
            
            # Get junior manager applications
            applications = await get_junior_manager_applications(message.from_user.id)
            
            if not applications:
                no_applications_text = (
                    "📭 Hozircha sizga biriktirilgan arizalar yo'q."
                    if lang == 'uz' else
                    "📭 Пока нет заявок, назначенных вам."
                )
                
                await message.answer(
                    text=no_applications_text,
                    reply_markup=get_junior_manager_back_keyboard(lang)
                )
                return
            
            # Show first application
            await show_application_details(message, applications[0], applications, 0)
            
        except Exception as e:
            pass

    async def show_application_details(message_or_callback, application, applications, index):
        """Show application details with navigation"""
        try:
            # Format workflow type
            workflow_type_emoji = {
                'connection_request': '🔌',
                'technical_service': '🔧',
                'call_center_direct': '📞'
            }.get(application['workflow_type'], '📄')
            
            workflow_type_text = {
                'connection_request': 'Ulanish arizasi',
                'technical_service': 'Texnik xizmat',
                'call_center_direct': 'Call Center'
            }.get(application['workflow_type'], 'Boshqa')
            
            # Format status
            status_emoji = {
                'pending': '🟡',
                'in_progress': '🟠',
                'completed': '🟢',
                'cancelled': '🔴'
            }.get(application['current_status'], '⚪')
            
            status_text = {
                'pending': 'Kutilmoqda',
                'in_progress': 'Jarayonda',
                'completed': 'Bajarilgan',
                'cancelled': 'Bekor qilingan'
            }.get(application['current_status'], 'Noma\'lum')
            
            # Format priority
            priority_emoji = {
                'high': '🔴',
                'normal': '🟡',
                'low': '🟢'
            }.get(application.get('priority', 'normal'), '🟡')
            
            priority_text = {
                'high': 'Yuqori',
                'normal': 'O\'rtacha',
                'low': 'Past'
            }.get(application.get('priority', 'normal'), 'O\'rtacha')
            
            # Format date
            created_date = application['created_at'].strftime('%d.%m.%Y %H:%M')
            
            # To'liq ma'lumot
            text = (
                f"{workflow_type_emoji} <b>{workflow_type_text} - To'liq ma'lumot</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"📅 <b>Sana:</b> {created_date}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📞 <b>Telefon:</b> {application['contact_info']['phone']}\n"
                f"🏛️ <b>Hudud:</b> {application.get('region', 'Noma\'lum')}\n"
                f"🏠 <b>Manzil:</b> {application.get('address', 'Noma\'lum')}\n"
                f"📝 <b>Tavsif:</b> {application['description']}\n"
                f"{status_emoji} <b>Holat:</b> {status_text}\n"
                f"{priority_emoji} <b>Ustuvorlik:</b> {priority_text}\n\n"
                f"📊 <b>Ariza #{index + 1} / {len(applications)}</b>"
            )
            
            # Create navigation keyboard
            keyboard = get_applications_navigation_keyboard(index, len(applications))
            
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer(text, reply_markup=keyboard, parse_mode='HTML')
            else:
                await message_or_callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                
        except Exception as e:
            pass

    @router.callback_query(F.data == "jm_prev_application")
    async def show_previous_application(callback: CallbackQuery, state: FSMContext):
        """Show previous application"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_app_index', 0)
            
            applications = await get_junior_manager_applications(callback.from_user.id)
            
            if current_index > 0:
                new_index = current_index - 1
                await state.update_data(current_app_index=new_index)
                await show_application_details(callback, applications[new_index], applications, new_index)
            else:
                await callback.answer("Bu birinchi ariza")
                
        except Exception as e:
            pass

    @router.callback_query(F.data == "jm_next_application")
    async def show_next_application(callback: CallbackQuery, state: FSMContext):
        """Show next application"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_app_index', 0)
            
            applications = await get_junior_manager_applications(callback.from_user.id)
            
            if current_index < len(applications) - 1:
                new_index = current_index + 1
                await state.update_data(current_app_index=new_index)
                await show_application_details(callback, applications[new_index], applications, new_index)
            else:
                await callback.answer("Bu oxirgi ariza")
                
        except Exception as e:
            pass

    @router.callback_query(F.data == "jm_contact_client")
    async def contact_client_handler(callback: CallbackQuery, state: FSMContext):
        """Handle contact client button"""
        try:
            await callback.answer()
            
            # Get current application
            current_index = await state.get_data()
            current_index = current_index.get('current_app_index', 0)
            
            applications = await get_junior_manager_applications(callback.from_user.id)
            if not applications or current_index >= len(applications):
                await callback.answer("Ariza topilmadi")
                return
            
            application = applications[current_index]
            
            # Show contact information
            contact_text = (
                f"📞 <b>Mijoz bilan bog'lanish</b>\n\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📞 <b>Telefon:</b> {application['contact_info']['phone']}\n"
                f"🏠 <b>Manzil:</b> {application.get('address', 'Noma\'lum')}\n"
                f"📝 <b>Ariza ID:</b> {application['id']}\n\n"
            )
            
            # Create back button
            back_button = InlineKeyboardButton(
                text="⬅️ Orqaga qaytish",
                callback_data="jm_back_to_application"
            )
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button]])
            
            await callback.message.edit_text(
                contact_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "jm_send_to_controller")
    async def send_to_controller_handler(callback: CallbackQuery, state: FSMContext):
        """Handle send to controller button"""
        try:
            await callback.answer()
            
            # Get current application
            current_index = await state.get_data()
            current_index = current_index.get('current_app_index', 0)
            
            applications = await get_junior_manager_applications(callback.from_user.id)
            if not applications or current_index >= len(applications):
                await callback.answer("Ariza topilmadi")
                return
            
            application = applications[current_index]
            
            # Store application info in state for later use
            await state.update_data(
                current_application_id=application['id'],
                current_application_data=application
            )
            
            # Show text input prompt
            input_text = (
                f"📝 <b>Controller'ga qo'shimcha ma'lumot kiriting</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📝 <b>Asosiy tavsif:</b> {application['description']}\n\n"
                f"📝 Iltimos, qo'shimcha ma'lumotlarni yozing:"
            )
            
            # Create cancel button
            cancel_button = InlineKeyboardButton(
                text="❌ Bekor qilish",
                callback_data="jm_back_to_application"
            )
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[cancel_button]])
            
            await callback.message.edit_text(
                input_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
            # Set state to wait for text input
            await state.set_state(JuniorManagerStates.waiting_for_controller_note)
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.message(JuniorManagerStates.waiting_for_controller_note)
    async def handle_controller_note_input(message: Message, state: FSMContext):
        """Handle text input for controller note"""
        try:
            # Get the note text
            note_text = message.text.strip()
            
            if len(note_text) < 10:
                await message.answer(
                    "⚠️ Iltimos, kamida 10 ta belgi kiriting. Qo'shimcha ma'lumotlarni batafsil yozing."
                )
                return
            
            # Store the note in state
            await state.update_data(controller_note=note_text)
            
            # Get application data from state
            data = await state.get_data()
            application = data.get('current_application_data')
            
            if not application:
                await message.answer("❌ Ariza ma'lumotlari topilmadi. Iltimos, qaytadan urinib ko'ring.")
                return
            
            # Show review and confirmation
            review_text = (
                f"📋 <b>Yuborishdan oldin tekshirish</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📞 <b>Telefon:</b> {application['contact_info']['phone']}\n"
                f"🏠 <b>Manzil:</b> {application.get('address', 'Noma\'lum')}\n"
                f"📝 <b>Asosiy tavsif:</b> {application['description']}\n\n"
                f"📝 <b>Qo'shimcha ma'lumotlar:</b>\n"
                f"<i>{note_text}</i>\n\n"
                f"Controller'ga yuborishni tasdiqlaysizmi?"
            )
            
            # Create confirmation buttons
            confirm_button = InlineKeyboardButton(
                text="✅ Ha, yuborish",
                callback_data="jm_confirm_send_to_controller"
            )
            edit_button = InlineKeyboardButton(
                text="✏️ Qayta yozish",
                callback_data="jm_edit_controller_note"
            )
            cancel_button = InlineKeyboardButton(
                text="❌ Bekor qilish",
                callback_data="jm_back_to_application"
            )
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[confirm_button], [edit_button], [cancel_button]])
            
            await message.answer(
                review_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
            # Clear the waiting state
            await state.clear()
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "jm_edit_controller_note")
    async def edit_controller_note_handler(callback: CallbackQuery, state: FSMContext):
        """Handle edit controller note button"""
        try:
            await callback.answer()
            
            # Get application data from state
            data = await state.get_data()
            application = data.get('current_application_data')
            
            if not application:
                await callback.answer("Ariza ma'lumotlari topilmadi")
                return
            
            # Show text input prompt again
            input_text = (
                f"📝 <b>Controller'ga qo'shimcha ma'lumot kiriting</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📝 <b>Asosiy tavsif:</b> {application['description']}\n\n"
                f"📝 <b>Qo'shimcha ma'lumotlarni yozing:</b>"
            )
            
            # Create cancel button
            cancel_button = InlineKeyboardButton(
                text="❌ Bekor qilish",
                callback_data="jm_back_to_application"
            )
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[cancel_button]])
            
            await callback.message.edit_text(
                input_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
            # Set state to wait for text input again
            await state.set_state(JuniorManagerStates.waiting_for_controller_note)
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "jm_confirm_send_to_controller")
    async def confirm_send_to_controller_handler(callback: CallbackQuery, state: FSMContext):
        """Handle confirmation to send to controller"""
        try:
            await callback.answer()
            
            # Get application data and note from state
            data = await state.get_data()
            application = data.get('current_application_data')
            note_text = data.get('controller_note', '')
            
            if not application:
                await callback.answer("Ariza ma'lumotlari topilmadi")
                return
            
            # Mock sending to controller (in real implementation, this would update database)
            success_text = (
                f"✅ <b>Ariza muvaffaqiyatli yuborildi!</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📤 <b>Yuborilgan vaqt:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
                f"📝 <b>Qo'shimcha ma'lumotlar:</b>\n"
                f"<i>{note_text}</i>\n\n"
            )
            
            # Create back to inbox button
            back_button = InlineKeyboardButton(
                text="📥 Inbox'ga qaytish",
                callback_data="jm_back_to_inbox"
            )
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button]])
            
            await callback.message.edit_text(
                success_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "jm_back_to_application")
    async def back_to_application_handler(callback: CallbackQuery, state: FSMContext):
        """Handle back to application button"""
        try:
            await callback.answer()
            
            # Get current application
            current_index = await state.get_data()
            current_index = current_index.get('current_app_index', 0)
            
            applications = await get_junior_manager_applications(callback.from_user.id)
            if not applications or current_index >= len(applications):
                await callback.answer("Ariza topilmadi")
                return
            
            # Show application details again
            await show_application_details(callback, applications[current_index], applications, current_index)
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "jm_back_to_inbox")
    async def back_to_inbox_handler(callback: CallbackQuery, state: FSMContext):
        """Handle back to inbox button"""
        try:
            await callback.answer()
            
            # Show inbox again
            await view_inbox(callback.message, state)
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    return router

def get_applications_navigation_keyboard(current_index: int, total_applications: int):
    """Create navigation keyboard for applications"""
    keyboard = []
    
    # Navigation row
    nav_buttons = []
    
    # Previous button
    if current_index > 0:
        nav_buttons.append(InlineKeyboardButton(
            text="⬅️ Oldingi",
            callback_data="jm_prev_application"
        ))
    
    # Next button
    if current_index < total_applications - 1:
        nav_buttons.append(InlineKeyboardButton(
            text="Keyingi ➡️",
            callback_data="jm_next_application"
        ))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Action buttons row
    action_buttons = []
    
    # Contact client button
    action_buttons.append(InlineKeyboardButton(
        text="📞 Mijoz bilan bog'lanish",
        callback_data="jm_contact_client"
    ))
    
    # Send to controller button
    action_buttons.append(InlineKeyboardButton(
        text="📤 Controller'ga yuborish",
        callback_data="jm_send_to_controller"
    ))
    
    keyboard.append(action_buttons)
     
    return InlineKeyboardMarkup(inline_keyboard=keyboard)