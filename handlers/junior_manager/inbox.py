"""
Junior Manager Inbox Handler - Soddalashtirilgan versiya

Bu modul junior manager uchun inbox funksionalligini o'z ichiga oladi,
kiruvchi arizalar va vazifalarni ko'rish va boshqarish.
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

async def send_and_track(message_func, text: str, user_id: int, **kwargs):
    """Mock send and track"""
    return await message_func(text, **kwargs)

async def edit_and_track(message_func, text: str, user_id: int, **kwargs):
    """Mock edit and track"""
    return await message_func(text, **kwargs)

async def cleanup_user_inline_messages(user_id: int):
    """Mock cleanup function"""
    pass

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

def get_junior_manager_inbox_router():
    """Get router for junior manager inbox handlers"""
    router = get_role_router("junior_manager")

    @router.message(F.text.in_(["📥 Inbox", "Inbox"]))
    async def handle_inbox_message(message: Message, state: FSMContext):
        """Handle inbox message command"""
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
                await send_and_track(send_method(error_text), user_id)
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
            await send_and_track(
                send_method(text, reply_markup=keyboard),
                user_id
            )
            
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
                await edit_and_track(
                    callback.message.edit_text(
                        text,
                        reply_markup=get_back_to_inbox_keyboard(lang=lang)
                    ),
                    callback.from_user.id
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
                await edit_and_track(
                    callback.message.edit_text(
                        text,
                        reply_markup=get_back_to_inbox_keyboard(lang=lang)
                    ),
                    callback.from_user.id
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
                await edit_and_track(
                    callback.message.edit_text(
                        text,
                        reply_markup=get_back_to_inbox_keyboard(lang=lang)
                    ),
                    callback.from_user.id
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
                await edit_and_track(
                    callback.message.edit_text(
                        text,
                        reply_markup=get_back_to_inbox_keyboard(lang=lang)
                    ),
                    callback.from_user.id
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
            
            text = f"""🔸 **Ariza #{app['id']}**

👤 **Mijoz:** {app.get('client_name', 'N/A')}
📱 **Telefon:** {app.get('client_phone', 'N/A')}
📍 **Manzil:** {app.get('address', 'N/A')}
📝 **Izoh:** {app.get('description', 'N/A')}
⚡ **Daraja:** {priority_emoji} {priority_text}
📊 **Holat:** {status_emoji} {status_text}
📅 **Sana:** {date_str}

📋 Sahifa {page}/{total_pages}"""
            
            # Create keyboard with pagination
            keyboard = _create_applications_keyboard(page_applications, page, total_pages, lang)
            
            await edit_and_track(
                callback.message.edit_text(
                    text,
                    reply_markup=keyboard,
                    parse_mode="Markdown"
                ),
                callback.from_user.id
            )
            
        except Exception as e:
            print(f"Error in _show_applications_page: {e}")

    async def _refresh_inbox(callback: CallbackQuery, junior_manager_id: int, lang: str):
        """Refresh inbox view"""
        try:
            await junior_manager_inbox(callback, None)
            await callback.answer("✅ Yangilandi")
        except Exception as e:
            print(f"Error in _refresh_inbox: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    def _build_inbox_text(workload: Dict, recent_activity: List, lang: str) -> str:
        """Build inbox text with workload and recent activity"""
        text = f"""📥 Kichik menejer inbox

📊 Ish yuki:
• Kutilayotgan: {workload.get('pending', 0)}
• Jarayonda: {workload.get('in_progress', 0)}
• Bajarilgan: {workload.get('completed', 0)}

"""
        
        if recent_activity:
            text += "🕒 So'nggi faollik:\n"
            
            for activity in recent_activity[:5]:
                time_ago = _get_time_ago(activity.get('created_at'), lang)
                text += f"• {activity.get('action', 'N/A')} - {time_ago}\n"
        
        return text

    def _create_inbox_keyboard(lang: str) -> InlineKeyboardMarkup:
        """Create inbox keyboard"""
        return get_inbox_keyboard(lang=lang)

    def _create_applications_keyboard(applications: List, current_page: int, total_pages: int, lang: str) -> InlineKeyboardMarkup:
        """Create applications keyboard with pagination and detailed buttons - 1 per page"""
        keyboard = []
        
        # Add action buttons first
        action_row = []
        action_row.append(InlineKeyboardButton(
            text="📞 Chaqirish",
            callback_data=f"jm_contact_call_{applications[0]['id']}"
        ))
        action_row.append(InlineKeyboardButton(
            text="📤 Yuborish",
            callback_data=f"jm_contact_forward_{applications[0]['id']}"
        ))
        keyboard.append(action_row)
        
        # Add pagination buttons
        pagination_row = []
        if current_page > 1:
            pagination_row.append(InlineKeyboardButton(
                text="⬅️ Oldingi",
                callback_data=f"jm_page_{current_page - 1}"
            ))
        
        if current_page < total_pages:
            pagination_row.append(InlineKeyboardButton(
                text="Keyingi ➡️",
                callback_data=f"jm_page_{current_page + 1}"
            ))
        
        if pagination_row:
            keyboard.append(pagination_row)
        
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
            return f"{diff.days} kun oldin"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} soat oldin"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} daqiqa oldin"
        else:
            return "Hozir"

    def _get_status_text(status: str, lang: str) -> str:
        """Get status text in user language"""
        status_texts = {
            'pending': 'Kutilmoqda',
            'in_progress': 'Jarayonda',
            'completed': 'Bajarilgan',
            'cancelled': 'Bekor qilingan',
            'forwarded_to_controller': 'Controller-ga yuborilgan'
        }
        
        return status_texts.get(status, status)

    return router