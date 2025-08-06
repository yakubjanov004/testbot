"""
Junior Manager Inbox Viewing Handler - Soddalashtirilgan versiya

Bu modul junior manager uchun inbox ko'rish funksionalligini o'z ichiga oladi.
Inbox.py dan yaxshiroq tashkil etish uchun ajratilgan.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional
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

# Using get_role_router from utils.role_system

async def get_junior_manager_applications(junior_manager_id: int, limit: int = 50):
    """Mock junior manager applications"""
    from datetime import datetime
    return [
        {
            'id': 1,
            'client_name': 'Aziz Karimov',
            'client_phone': '+998901234567',
            'address': 'Tashkent, Chorsu',
            'description': 'Internet ulanish arizasi',
            'priority': 'medium',
            'status': 'pending',
            'created_at': datetime.now()
        },
        {
            'id': 2,
            'client_name': 'Malika Toshmatova',
            'client_phone': '+998901234568',
            'address': 'Tashkent, Yunusabad',
            'description': 'TV signal muammosi',
            'priority': 'high',
            'status': 'in_progress',
            'created_at': datetime.now()
        },
        {
            'id': 3,
            'client_name': 'Bekzod Mirzayev',
            'client_phone': '+998901234569',
            'address': 'Tashkent, Sergeli',
            'description': 'Telefon xizmati',
            'priority': 'low',
            'status': 'completed',
            'created_at': datetime.now()
        }
    ]

async def get_junior_manager_recent_activity(junior_manager_id: int):
    """Mock recent activity"""
    from datetime import datetime
    return [
        {
            'action': 'Ariza ko\'rildi',
            'created_at': datetime.now()
        },
        {
            'action': 'Mijoz chaqirildi',
            'created_at': datetime.now()
        }
    ]

async def get_junior_manager_workload(junior_manager_id: int):
    """Mock workload statistics"""
    return {
        'pending': 5,
        'in_progress': 3,
        'completed': 12
    }

async def get_service_request_details_for_junior_manager(app_id: int):
    """Mock get service request details"""
    return {
        'id': app_id,
        'client_name': 'Aziz Karimov',
        'client_phone': '+998901234567',
        'address': 'Tashkent, Chorsu',
        'description': 'Internet ulanish arizasi',
        'status': 'pending',
        'priority': 'medium',
        'created_at': datetime.now()
    }

async def forward_application_to_controller(app_id: int, junior_manager_id: int):
    """Mock forward application to controller"""
    return True

# Mock keyboard functions
def get_back_to_inbox_keyboard(lang: str = 'uz'):
    """Mock back to inbox keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📥 Inbox-ga qaytish", callback_data="jm_back_to_inbox"),
            InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="jm_main_menu")
        ]
    ])

def get_inbox_keyboard(lang: str = 'uz'):
    """Mock inbox keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📋 Barcha arizalar", callback_data="jm_inbox_all"),
            InlineKeyboardButton(text="⏳ Kutilayotgan", callback_data="jm_inbox_pending")
        ],
        [
            InlineKeyboardButton(text="🔄 Jarayonda", callback_data="jm_inbox_progress"),
            InlineKeyboardButton(text="📞 Ommaviy chaqirish", callback_data="jm_bulk_call")
        ],
        [
            InlineKeyboardButton(text="📤 Ommaviy yuborish", callback_data="jm_bulk_forward"),
            InlineKeyboardButton(text="🔄 Yangilash", callback_data="jm_inbox_refresh")
        ]
    ])

# Mock states
from aiogram.fsm.state import State, StatesGroup

class JuniorManagerInboxStates(StatesGroup):
    viewing_inbox = State()
    viewing_application = State()
    entering_call_notes = State()


def get_junior_manager_inbox_viewing_router():
    """Get router for junior manager inbox viewing handlers"""
    router = get_role_router("junior_manager")

    @router.message(F.text.in_(["📥 Inbox", "Inbox"]))
    async def handle_inbox_message(message: Message, state: FSMContext):
        """Handle inbox message command"""
        # Check user role first - only process if user is junior_manager
        from loader import get_user_role
        user_role = get_user_role(message.from_user.id)
        if user_role != 'junior_manager':
            return  # Skip processing for non-junior-manager users
        
        await junior_manager_inbox(message, state)

    @router.callback_query(F.data.startswith("jm_inbox_"))
    async def handle_inbox_actions(callback: CallbackQuery, state: FSMContext):
        """Handle inbox action buttons"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return

            lang = user.get('language', 'uz')
            action = callback.data.split("_")[-1]
            
            if action == "all":
                await _show_all_applications_inbox(callback, user['id'], lang)
            elif action == "pending":
                await _show_pending_applications_inbox(callback, user['id'], lang)
            elif action == "progress":
                await _show_progress_applications_inbox(callback, user['id'], lang)
            elif action == "refresh":
                await _refresh_inbox(callback, user['id'], lang)
            else:
                await callback.answer("Noto'g'ri amal", show_alert=True)
            
        except Exception as e:
            print(f"Error in handle_inbox_actions: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("jm_app_"))
    async def handle_application_selection(callback: CallbackQuery, state: FSMContext):
        """Handle application selection from inbox"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return

            lang = user.get('language', 'uz')
            app_id = int(callback.data.split("_")[-1])
            
            # Get application details
            app_details = await get_service_request_details_for_junior_manager(app_id)
            if not app_details:
                await callback.answer("Ariza topilmadi", show_alert=True)
                return
            
            # Show application details and contact options
            await _show_application_details(callback, app_details, lang)
            
        except Exception as e:
            print(f"Error in handle_application_selection: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("jm_contact_"))
    async def handle_client_contact(callback: CallbackQuery, state: FSMContext):
        """Handle client contact actions"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return

            lang = user.get('language', 'uz')
            action = callback.data.split("_")[-1]
            
            if action == "call":
                await _handle_call_client(callback, state, lang)
            elif action == "forward":
                await _handle_forward_to_controller(callback, state, lang)
            else:
                await callback.answer("Noto'g'ri amal", show_alert=True)
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("jm_page_"))
    async def handle_pagination(callback: CallbackQuery, state: FSMContext):
        """Handle pagination in inbox"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return

            lang = user.get('language', 'uz')
            page = int(callback.data.split("_")[-1])
            
            # Show applications for the selected page
            await _show_applications_page(callback, user['id'], lang, page)
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("jm_bulk_"))
    async def handle_bulk_actions(callback: CallbackQuery, state: FSMContext):
        """Handle bulk actions for applications"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return

            lang = user.get('language', 'uz')
            action = callback.data.split("_")[-1]
            
            if action == "call":
                await _handle_bulk_call(callback, user['id'], lang)
            elif action == "forward":
                await _handle_bulk_forward(callback, user['id'], lang)
            else:
                await callback.answer("Noto'g'ri amal", show_alert=True)
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    async def junior_manager_inbox(event, state: FSMContext, page: int = 1):
        """Show junior manager inbox with comprehensive view, supports Message and CallbackQuery"""
        user_id = None
        send_method = None
        try:
            # Determine user_id and message object
            if hasattr(event, 'from_user') and hasattr(event, 'message'):
                # CallbackQuery
                user_id = event.from_user.id
                msg_obj = event.message
                send_method = msg_obj.edit_text
            else:
                # Message
                user_id = event.from_user.id
                msg_obj = event
                send_method = msg_obj.answer

            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'junior_manager':
                error_text = "Sizda ruxsat yo'q."
                await send_method(error_text)
                return

            lang = user.get('language', 'uz')
            
            # Get workload statistics
            workload = await get_junior_manager_workload(user['id'])
            
            # Get recent activity
            recent_activity = await get_junior_manager_recent_activity(user['id'])
            
            # Build inbox text
            text = _build_inbox_text(workload, recent_activity, lang)
            
            # Create keyboard
            keyboard = _create_inbox_keyboard(lang)
            
            # Send message
            await send_method(text, reply_markup=keyboard)
            
        except Exception as e:
            print(f"Error in junior_manager_inbox: {e}")

    async def _show_all_applications_inbox(callback: CallbackQuery, junior_manager_id: int, lang: str):
        """Show all applications in inbox with pagination"""
        try:
            applications = await get_junior_manager_applications(junior_manager_id, limit=1000)
            
            if applications:
                await _show_applications_page(callback, junior_manager_id, lang, 1, applications)
            else:
                text = "📋 Hozircha arizalar yo'q"
                
                # Create back keyboard
                await callback.message.edit_text(
                    text,
                    reply_markup=get_back_to_inbox_keyboard(lang=lang)
                )
            
        except Exception as e:
            print(f"Error in _show_all_applications_inbox: {e}")

    async def _show_pending_applications_inbox(callback: CallbackQuery, junior_manager_id: int, lang: str):
        """Show pending applications in inbox with pagination"""
        try:
            applications = await get_junior_manager_applications(junior_manager_id, limit=1000)
            pending_apps = [app for app in applications if app.get('status') == 'pending']
            
            if pending_apps:
                await _show_applications_page(callback, junior_manager_id, lang, 1, pending_apps)
            else:
                text = "⏳ Kutilayotgan arizalar yo'q"
                
                # Create back keyboard
                await callback.message.edit_text(
                    text,
                    reply_markup=get_back_to_inbox_keyboard(lang=lang)
                )
            
        except Exception as e:
            print(f"Error in _show_pending_applications_inbox: {e}")

    async def _show_progress_applications_inbox(callback: CallbackQuery, junior_manager_id: int, lang: str):
        """Show in-progress applications in inbox with pagination"""
        try:
            applications = await get_junior_manager_applications(junior_manager_id, limit=1000)
            progress_apps = [app for app in applications if app.get('status') == 'in_progress']
            
            if progress_apps:
                await _show_applications_page(callback, junior_manager_id, lang, 1, progress_apps)
            else:
                text = "🔄 Jarayondagi arizalar yo'q"
                
                # Create back keyboard
                await callback.message.edit_text(
                    text,
                    reply_markup=get_back_to_inbox_keyboard(lang=lang)
                )
            
        except Exception as e:
            print(f"Error in _show_progress_applications_inbox: {e}")

    async def _show_applications_page(callback: CallbackQuery, junior_manager_id: int, lang: str, page: int, applications: List = None):
        """Show applications with pagination and full details - 1 per page"""
        try:
            if applications is None:
                applications = await get_junior_manager_applications(junior_manager_id, limit=1000)
            
            # Pagination settings - 1 application per page
            items_per_page = 1
            total_pages = (len(applications) + items_per_page - 1) // items_per_page
            start_idx = (page - 1) * items_per_page
            end_idx = start_idx + items_per_page
            page_applications = applications[start_idx:end_idx]
            
            if not page_applications:
                text = "📋 Arizalar yo'q"
                
                # Create back keyboard
                await callback.message.edit_text(
                    text,
                    reply_markup=get_back_to_inbox_keyboard(lang=lang)
                )
                return
            
            # Build detailed text for single application
            app = page_applications[0]
            status_emoji = _get_status_emoji(app.get('status', 'pending'))
            priority_emoji = "⚡" if app.get('priority') == 'urgent' else "📋"
            priority_text = "Shoshilinch" if app.get('priority') == 'urgent' else "Oddiy"
            status_text = _get_status_text(app.get('status', 'pending'), lang)
            
            # Format date
            created_date = app.get('created_at')
            if created_date:
                if isinstance(created_date, str):
                    date_str = created_date
                else:
                    date_str = created_date.strftime("%d.%m.%Y %H:%M")
            else:
                date_str = "N/A"
            
            text = (
                f"🔸 **Ariza #{app['id']}**\n\n"
                f"👤 **Mijoz:** {app.get('client_name', 'N/A')}\n"
                f"📱 **Telefon:** {app.get('client_phone', 'N/A')}\n"
                f"📍 **Manzil:** {app.get('address', 'N/A')}\n"
                f"📝 **Izoh:** {app.get('description', 'N/A')}\n"
                f"⚡ **Daraja:** {priority_emoji} {priority_text}\n"
                f"📊 **Holat:** {status_emoji} {status_text}\n"
                f"📅 **Sana:** {date_str}\n\n"
                f"📋 Sahifa {page}/{total_pages}"
            ) if lang == 'uz' else (
                f"🔸 **Заявка #{app['id']}**\n\n"
                f"👤 **Клиент:** {app.get('client_name', 'N/A')}\n"
                f"📱 **Телефон:** {app.get('client_phone', 'N/A')}\n"
                f"📍 **Адрес:** {app.get('address', 'N/A')}\n"
                f"📝 **Описание:** {app.get('description', 'N/A')}\n"
                f"⚡ **Приоритет:** {priority_emoji} {priority_text}\n"
                f"📊 **Статус:** {status_emoji} {status_text}\n"
                f"📅 **Дата:** {date_str}\n\n"
                f"📋 Страница {page}/{total_pages}"
            )
            
            # Create keyboard with pagination
            keyboard = _create_applications_keyboard(page_applications, page, total_pages, lang)
            
            await callback.message.edit_text(
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            print(f"Error in _show_applications_page: {e}")

    async def _show_application_details(callback: CallbackQuery, app_details: Dict, lang: str):
        """Show application details and contact options"""
        try:
            status_emoji = _get_status_emoji(app_details.get('status', 'pending'))
            priority_emoji = "⚡" if app_details.get('priority') == 'urgent' else "📋"
            
            text = (
                f"📋 Ariza #{app_details['id']}\n\n"
                f"👤 Mijoz: {app_details.get('client_name', 'N/A')}\n"
                f"📱 Telefon: {app_details.get('client_phone', 'N/A')}\n"
                f"📍 Manzil: {app_details.get('address', 'N/A')}\n"
                f"📝 Izoh: {app_details.get('description', 'N/A')}\n"
                f"⚡ Daraja: {app_details.get('priority', 'medium')}\n"
                f"📊 Holat: {status_emoji} {app_details.get('status', 'pending')}\n"
                f"📅 Sana: {app_details.get('created_at', 'N/A')}\n\n"
                f"🔗 Mijoz bilan bog'lanish va tafsilotlarni kiritish uchun tugmalardan foydalaning:"
            ) if lang == 'uz' else (
                f"📋 Заявка #{app_details['id']}\n\n"
                f"👤 Клиент: {app_details.get('client_name', 'N/A')}\n"
                f"📱 Телефон: {app_details.get('client_phone', 'N/A')}\n"
                f"📍 Адрес: {app_details.get('address', 'N/A')}\n"
                f"📝 Описание: {app_details.get('description', 'N/A')}\n"
                f"⚡ Приоритет: {app_details.get('priority', 'medium')}\n"
                f"📊 Статус: {status_emoji} {app_details.get('status', 'pending')}\n"
                f"📅 Дата: {app_details.get('created_at', 'N/A')}\n\n"
                f"🔗 Используйте кнопки для связи с клиентом и ввода деталей:"
            )
            
            # Create contact keyboard
            keyboard = _create_contact_keyboard(app_details['id'], lang)
            
            await callback.message.edit_text(
                text,
                reply_markup=keyboard
            )
            
        except Exception as e:
            print(f"Error in _show_application_details: {e}")

    async def _handle_call_client(callback: CallbackQuery, state: FSMContext, lang: str):
        """Handle calling client"""
        try:
            # Get application ID from callback data
            app_id = int(callback.data.split("_")[-2])
            
            # Get application details
            app_details = await get_service_request_details_for_junior_manager(app_id)
            if not app_details:
                await callback.answer("Ariza topilmadi", show_alert=True)
                return
            
            phone = app_details.get('client_phone')
            if not phone:
                await callback.answer("Telefon raqam topilmadi", show_alert=True)
                return
            
            # Show call information
            text = (
                f"📞 Mijozni chaqirish:\n\n"
                f"👤 Mijoz: {app_details.get('client_name', 'N/A')}\n"
                f"📱 Telefon: {phone}\n"
                f"📋 Ariza: #{app_id}\n\n"
                f"📞 {phone} raqamiga qo'ng'iroq qiling va tafsilotlarni aniqlang.\n"
                f"Keyin 'Tafsilotlarni kiritish' tugmasini bosing."
            ) if lang == 'uz' else (
                f"📞 Звонок клиенту:\n\n"
                f"👤 Клиент: {app_details.get('client_name', 'N/A')}\n"
                f"📱 Телефон: {phone}\n"
                f"📋 Заявка: #{app_id}\n\n"
                f"📞 Позвоните на номер {phone} и уточните детали.\n"
                f"Затем нажмите кнопку 'Ввести детали'."
            )
            
            # Create keyboard with details input option
            keyboard = _create_details_input_keyboard(app_id, lang)
            
            await callback.message.edit_text(
                text,
                reply_markup=keyboard
            )
            
            await callback.answer("📞 Qo'ng'iroq qiling", show_alert=True)
            
        except Exception as e:
            print(f"Error in _handle_call_client: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    async def _handle_forward_to_controller(callback: CallbackQuery, state: FSMContext, lang: str):
        """Handle forwarding to controller"""
        try:
            # Get application ID from callback data
            app_id = int(callback.data.split("_")[-2])
            
            # Get application details
            app_details = await get_service_request_details_for_junior_manager(app_id)
            if not app_details:
                await callback.answer("Ariza topilmadi", show_alert=True)
                return
            
            # Update application status to forwarded
            # This would typically involve a database update
            # For now, we'll just show a success message
            
            text = (
                f"✅ Ariza controller-ga yuborildi!\n\n"
                f"📋 Ariza: #{app_id}\n"
                f"👤 Mijoz: {app_details.get('client_name', 'N/A')}\n"
                f"📱 Telefon: {app_details.get('client_phone', 'N/A')}\n\n"
                f"🔄 Ariza endi controller inbox-ida ko'rinadi."
            ) if lang == 'uz' else (
                f"✅ Заявка отправлена контроллеру!\n\n"
                f"📋 Заявка: #{app_id}\n"
                f"👤 Клиент: {app_details.get('client_name', 'N/A')}\n"
                f"📱 Телефон: {app_details.get('client_phone', 'N/A')}\n\n"
                f"🔄 Заявка теперь отображается в inbox контроллера."
            )
            
            # Create back to inbox keyboard
            from keyboards.junior_manager_buttons import get_back_to_inbox_keyboard
            await callback.message.edit_text(
                text,
                reply_markup=get_back_to_inbox_keyboard(lang=lang)
            )
            
            await callback.answer("✅ Yuborildi", show_alert=True)
            
        except Exception as e:
            print(f"Error in _handle_forward_to_controller: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    async def _refresh_inbox(callback: CallbackQuery, junior_manager_id: int, lang: str):
        """Refresh inbox view"""
        try:
            await junior_manager_inbox(callback, None)
            await callback.answer("✅ Yangilandi" if lang == 'uz' else "✅ Обновлено")
        except Exception as e:
            print(f"Error in _refresh_inbox: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    async def _handle_bulk_call(callback: CallbackQuery, junior_manager_id: int, lang: str):
        """Handle bulk call action"""
        try:
            # Get pending applications
            applications = await get_junior_manager_applications(junior_manager_id, limit=1000)
            pending_apps = [app for app in applications if app.get('status') == 'pending']
            
            if not pending_apps:
                await callback.answer(
                    "Kutilayotgan arizalar yo'q" if lang == 'uz' else "Нет ожидающих заявок",
                    show_alert=True
                )
                return
            
            # Show phone numbers for calling
            text = (
                f"📞 **Chaqirish uchun telefon raqamlar:**\n\n"
            ) if lang == 'uz' else (
                f"📞 **Номера для звонков:**\n\n"
            )
            
            for i, app in enumerate(pending_apps[:10], 1):  # Show first 10
                text += (
                    f"{i}. **{app.get('client_name', 'N/A')}**\n"
                    f"   📱 {app.get('client_phone', 'N/A')}\n"
                    f"   📋 Ariza #{app['id']}\n\n"
                ) if lang == 'uz' else (
                    f"{i}. **{app.get('client_name', 'N/A')}**\n"
                    f"   📱 {app.get('client_phone', 'N/A')}\n"
                    f"   📋 Заявка #{app['id']}\n\n"
                )
            
            if len(pending_apps) > 10:
                text += (
                    f"... va yana {len(pending_apps) - 10} ta ariza"
                ) if lang == 'uz' else (
                    f"... и еще {len(pending_apps) - 10} заявок"
                )
            
            # Create back keyboard
            from keyboards.junior_manager_buttons import get_back_to_inbox_keyboard
            await callback.message.edit_text(
                text,
                reply_markup=get_back_to_inbox_keyboard(lang=lang),
                parse_mode="Markdown"
            )
            
            await callback.answer(
                f"{len(pending_apps)} ta raqam ko'rsatildi" if lang == 'uz' else f"Показано {len(pending_apps)} номеров",
                show_alert=True
            )
            
        except Exception as e:
            print(f"Error in _handle_bulk_call: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    async def _handle_bulk_forward(callback: CallbackQuery, junior_manager_id: int, lang: str):
        """Handle bulk forward action"""
        try:
            # Get applications that can be forwarded
            applications = await get_junior_manager_applications(junior_manager_id, limit=1000)
            forwardable_apps = [app for app in applications if app.get('status') in ['pending', 'in_progress']]
            
            if not forwardable_apps:
                await callback.answer(
                    "Yuborish uchun arizalar yo'q" if lang == 'uz' else "Нет заявок для отправки",
                    show_alert=True
                )
                return
            
            # Forward all applications
            success_count = 0
            for app in forwardable_apps:
                success = await forward_application_to_controller(app['id'], junior_manager_id)
                if success:
                    success_count += 1
            
            text = (
                f"✅ **{success_count} ta ariza controller-ga yuborildi!**\n\n"
                f"📤 Yuborilgan: {success_count}\n"
                f"❌ Xatolik: {len(forwardable_apps) - success_count}\n\n"
                f"🔄 Ariza endi controller inbox-ida ko'rinadi."
            ) if lang == 'uz' else (
                f"✅ **{success_count} заявок отправлено контроллеру!**\n\n"
                f"📤 Отправлено: {success_count}\n"
                f"❌ Ошибка: {len(forwardable_apps) - success_count}\n\n"
                f"🔄 Заявки теперь отображаются в inbox контроллера."
            )
            
            # Create back keyboard
            from keyboards.junior_manager_buttons import get_back_to_inbox_keyboard
            await callback.message.edit_text(
                text,
                reply_markup=get_back_to_inbox_keyboard(lang=lang),
                parse_mode="Markdown"
            )
            
            await callback.answer(
                f"{success_count} ta yuborildi" if lang == 'uz' else f"Отправлено {success_count}",
                show_alert=True
            )
            
        except Exception as e:
            print(f"Error in _handle_bulk_forward: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    def _build_inbox_text(workload: Dict, recent_activity: List, lang: str) -> str:
        """Build inbox text with workload and recent activity"""
        text = (
            "📥 Kichik menejer inbox\n\n"
            f"📊 Ish yuki:\n"
            f"• Kutilayotgan: {workload.get('pending', 0)}\n"
            f"• Jarayonda: {workload.get('in_progress', 0)}\n"
            f"• Bajarilgan: {workload.get('completed', 0)}\n\n"
        ) if lang == 'uz' else (
            "📥 Inbox младшего менеджера\n\n"
            f"📊 Рабочая нагрузка:\n"
            f"• Ожидающие: {workload.get('pending', 0)}\n"
            f"• В процессе: {workload.get('in_progress', 0)}\n"
            f"• Завершенные: {workload.get('completed', 0)}\n\n"
        )
        
        if recent_activity:
            text += (
                "🕒 So'nggi faollik:\n"
            ) if lang == 'uz' else (
                "🕒 Последняя активность:\n"
            )
            
            for activity in recent_activity[:5]:
                time_ago = _get_time_ago(activity.get('created_at'), lang)
                text += f"• {activity.get('action', 'N/A')} - {time_ago}\n"
        
        return text

    def _create_inbox_keyboard(lang: str) -> InlineKeyboardMarkup:
        """Create inbox keyboard"""
        from keyboards.junior_manager_buttons import get_inbox_keyboard
        return get_inbox_keyboard(lang=lang)

    def _create_applications_keyboard(applications: List, current_page: int, total_pages: int, lang: str) -> InlineKeyboardMarkup:
        """Create applications keyboard with pagination and detailed buttons - 1 per page"""
        keyboard = []
        
        # Add action buttons first
        action_row = []
        action_row.append(InlineKeyboardButton(
            text="📞 Chaqirish" if lang == 'uz' else "📞 Позвонить",
            callback_data=f"jm_contact_call_{applications[0]['id']}"
        ))
        action_row.append(InlineKeyboardButton(
            text="📤 Yuborish" if lang == 'uz' else "📤 Отправить",
            callback_data=f"jm_contact_forward_{applications[0]['id']}"
        ))
        keyboard.append(action_row)
        
        # Add pagination buttons
        pagination_row = []
        if current_page > 1:
            pagination_row.append(InlineKeyboardButton(
                text="⬅️ Oldingi" if lang == 'uz' else "⬅️ Предыдущая",
                callback_data=f"jm_page_{current_page - 1}"
            ))
        
        if current_page < total_pages:
            pagination_row.append(InlineKeyboardButton(
                text="Keyingi ➡️" if lang == 'uz' else "Следующая ➡️",
                callback_data=f"jm_page_{current_page + 1}"
            ))
        
        if pagination_row:
            keyboard.append(pagination_row)
        
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    def _create_contact_keyboard(app_id: int, lang: str) -> InlineKeyboardMarkup:
        """Create contact keyboard for application"""
        keyboard = [
            [InlineKeyboardButton(
                text="📞 Mijozni chaqirish" if lang == 'uz' else "📞 Позвонить клиенту",
                callback_data=f"jm_contact_call_{app_id}"
            )],
            [InlineKeyboardButton(
                text="📤 Controller-ga yuborish" if lang == 'uz' else "📤 Отправить контроллеру",
                callback_data=f"jm_contact_forward_{app_id}"
            )],
            [InlineKeyboardButton(
                text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
                callback_data="jm_inbox_back"
            )]
        ]
        
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    def _create_details_input_keyboard(app_id: int, lang: str) -> InlineKeyboardMarkup:
        """Create keyboard for details input"""
        keyboard = [
            [InlineKeyboardButton(
                text="📝 Tafsilotlarni kiritish" if lang == 'uz' else "📝 Ввести детали",
                callback_data=f"jm_details_input_{app_id}"
            )],
            [InlineKeyboardButton(
                text="📤 Controller-ga yuborish" if lang == 'uz' else "📤 Отправить контроллеру",
                callback_data=f"jm_contact_forward_{app_id}"
            )],
            [InlineKeyboardButton(
                text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
                callback_data="jm_inbox_back"
            )]
        ]
        
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    def _get_status_emoji(status: str) -> str:
        """Get status emoji"""
        status_emojis = {
            'pending': '⏳',
            'in_progress': '🔄',
            'completed': '✅',
            'cancelled': '❌'
        }
        return status_emojis.get(status, '📋')

    def _get_time_ago(timestamp: datetime, lang: str) -> str:
        """Get time ago text"""
        if not timestamp:
            return "N/A"
        
        now = datetime.now()
        diff = now - timestamp
        
        if diff.days > 0:
            return f"{diff.days} kun oldin" if lang == 'uz' else f"{diff.days} дней назад"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} soat oldin" if lang == 'uz' else f"{hours} часов назад"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} daqiqa oldin" if lang == 'uz' else f"{minutes} минут назад"
        else:
            return "Hozir" if lang == 'uz' else "Сейчас"

    def _get_status_text(status: str, lang: str) -> str:
        """Get status text in user language"""
        status_texts = {
            'pending': {
                'uz': 'Kutilmoqda',
                'ru': 'Ожидает'
            },
            'in_progress': {
                'uz': 'Jarayonda',
                'ru': 'В процессе'
            },
            'completed': {
                'uz': 'Bajarilgan',
                'ru': 'Завершено'
            },
            'cancelled': {
                'uz': 'Bekor qilingan',
                'ru': 'Отменено'
            },
            'forwarded_to_controller': {
                'uz': 'Controller-ga yuborilgan',
                'ru': 'Отправлено контроллеру'
            }
        }
        
        return status_texts.get(status, {}).get(lang, status)

    return router 