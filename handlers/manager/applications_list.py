"""
Applications List Handler - Soddalashtirilgan versiya

Bu modul manager uchun arizalar ro'yxati va navigatsiya funksionalligini o'z ichiga oladi.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.manager_buttons import get_manager_view_applications_keyboard, get_manager_back_keyboard
from typing import Dict, Any, List, Optional
from datetime import datetime

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'manager',
        'language': 'uz',
        'full_name': 'Test Manager',
        'phone_number': '+998901234567'
    }

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    return 'uz'

async def cleanup_user_inline_messages(user_id: int):
    """Mock cleanup user inline messages"""
    print(f"Mock: Cleaning up inline messages for user {user_id}")

# Mock workflow access control
class MockWorkflowAccessControl:
    """Mock workflow access control"""
    async def get_filtered_requests_for_role(self, user_id: int, user_role: str):
        """Mock get filtered requests for role"""
        from datetime import datetime
        return [
            {
                'id': 'req_001_2024_01_15',
                'workflow_type': 'connection_request',
                'current_status': 'in_progress',
                'role_current': 'manager',
                'contact_info': {
                    'full_name': 'Aziz Karimov',
                    'phone': '+998901234567'
                },
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'description': 'Internet ulanish arizasi',
                'location': 'Tashkent, Chorsu'
            },
            {
                'id': 'req_002_2024_01_16',
                'workflow_type': 'technical_service',
                'current_status': 'created',
                'role_current': 'manager',
                'contact_info': {
                    'full_name': 'Malika Toshmatova',
                    'phone': '+998901234568'
                },
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'description': 'TV signal muammosi',
                'location': 'Tashkent, Yunusabad'
            },
            {
                'id': 'req_003_2024_01_17',
                'workflow_type': 'call_center_direct',
                'current_status': 'completed',
                'role_current': 'manager',
                'contact_info': {
                    'full_name': 'Jahongir Azimov',
                    'phone': '+998901234569'
                },
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'description': 'Qo\'ng\'iroq markazi arizasi',
                'location': 'Tashkent, Sergeli'
            }
        ]

def get_applications_list_router():
    """Router for applications list and navigation functionality"""
    router = Router()

    @router.message(F.text.in_(["📋 Hammasini ko'rish"]))
    async def view_all_applications(message: Message, state: FSMContext):
        """Manager view all applications handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'manager':
                return
            
            lang = user.get('language', 'uz')
            
            # Use workflow access control to get filtered requests for manager role
            access_control = MockWorkflowAccessControl()
            requests = await access_control.get_filtered_requests_for_role(
                user_id=user['id'],
                user_role='manager'
            )
            
            if not requests:
                text = "Hozircha hech qanday ariza yo'q."
                
                # Use send_and_track for inline cleanup
                await message.answer(text, reply_markup=get_manager_back_keyboard(lang))
                return
            
            # Foydalanuvchi state'da joriy zayavka indeksini saqlash
            data = await state.get_data()
            current_index = data.get('current_application_index', 0)
            
            # Indeksni cheklash
            if current_index >= len(requests):
                current_index = 0
            elif current_index < 0:
                current_index = len(requests) - 1
            
            # Joriy zayavka ma'lumotlari
            current_request = requests[current_index]
            
            # Status belgilarini aniqlash
            status_emoji = {
                'created': '🆕',
                'in_progress': '⏳',
                'completed': '✅',
                'cancelled': '❌'
            }.get(current_request.get('current_status', 'created'), '📋')
            
            workflow_type = current_request.get('workflow_type', 'unknown')
            workflow_emoji = {
                'connection_request': '🔌',
                'technical_service': '🔧',
                'call_center_direct': '📞'
            }.get(workflow_type, '📋')
            
            # Zayavka turini formatlash
            workflow_type_text = {
                'connection_request': 'Ulanish arizasi',
                'technical_service': 'Texnik xizmat',
                'call_center_direct': 'Qo\'ng\'iroq markazi'
            }.get(workflow_type, 'Noma\'lum')
            
            # Mijoz ma'lumotlari
            client_name = current_request.get('contact_info', {}).get('full_name', 'N/A') if isinstance(current_request.get('contact_info'), dict) else 'N/A'
            client_phone = current_request.get('contact_info', {}).get('phone', 'N/A') if isinstance(current_request.get('contact_info'), dict) else 'N/A'
            
            # Vaqt ma'lumotlari
            created_at = current_request.get('created_at', 'N/A')
            updated_at = current_request.get('updated_at', 'N/A')
            
            # Vaqt hisoblash
            total_duration = "N/A"
            if created_at and created_at != 'N/A':
                try:
                    if isinstance(created_at, str):
                        created_dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    else:
                        created_dt = created_at
                    
                    current_time = datetime.now()
                    if created_dt.tzinfo is None:
                        created_dt = created_dt.replace(tzinfo=None)
                    
                    duration = current_time - created_dt
                    total_hours = int(duration.total_seconds() // 3600)
                    total_minutes = int((duration.total_seconds() % 3600) // 60)
                    
                    if total_hours > 0:
                        total_duration = f"{total_hours}s {total_minutes}d"
                    else:
                        total_duration = f"{total_minutes} daqiqa"
                except:
                    total_duration = "N/A"
            
            # Izoh va diagnostika
            description = current_request.get('description', 'Izoh yo\'q')
            location = current_request.get('location', 'Manzil ko\'rsatilmagan')
            
            # Joriy rol va status
            current_role = current_request.get('role_current', 'Noma\'lum')
            current_status = current_request.get('current_status', 'Noma\'lum')
            
            # Status matnini formatlash
            status_text = {
                'created': 'Yaratilgan',
                'in_progress': 'Jarayonda',
                'completed': 'Tugallangan',
                'cancelled': 'Bekor qilingan'
            }.get(current_status, current_status)
            
            text = f"""
📋 <b>Ariza #{current_index + 1} / {len(requests)}</b>

{status_emoji}{workflow_emoji} <b>{client_name}</b>
   📋 ID: {current_request['id'][:8]}...
   🏷️ Turi: {workflow_type_text}
   📊 Status: {status_text}
   👤 Joriy rol: {current_role}

📞 <b>Mijoz ma'lumotlari:</b>
   • Nomi: {client_name}
   • Telefon: {client_phone}
   • Manzil: {location}

⏰ <b>Vaqt ma'lumotlari:</b>
   • Yaratilgan: {created_at}
   • Yangilangan: {updated_at}
   • Umumiy vaqt: {total_duration}

📝 <b>Izoh va diagnostika:</b>
   {description}

🔧 <b>Texnik ma'lumotlar:</b>
   • Workflow type: {workflow_type}
   • Current status: {current_status}
   • Role current: {current_role}
"""
            
            # Navigatsiya tugmalari
            keyboard_buttons = []
            
            # Agar 1tadan ko'p zayavka bo'lsa, navigatsiya tugmalarini qo'shish
            if len(requests) > 1:
                keyboard_buttons.append([
                    InlineKeyboardButton(
                        text="◀️ Oldingi",
                        callback_data="mgr_prev_application"
                    ),
                    InlineKeyboardButton(
                        text="Keyingi ▶️",
                        callback_data="mgr_next_application"
                    )
                ])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
            
            # State'da joriy indeksni saqlash
            await state.update_data(current_application_index=current_index)
            
            # Use send_and_track for inline cleanup
            await message.answer(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            print(f"Error in view_all_applications: {e}")
            lang = await get_user_lang(message.from_user.id)
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    @router.callback_query(F.data == "mgr_prev_application")
    async def show_previous_application(callback: CallbackQuery, state: FSMContext):
        """Oldingi arizani ko'rsatish"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return

            # State'dan joriy indeksni olish
            data = await state.get_data()
            current_index = data.get('current_application_index', 0)
            
            # Oldingi indeksga o'tish
            await state.update_data(current_application_index=current_index - 1)
            
            # Ariza ro'yxatini qayta ko'rsatish
            try:
                await view_all_applications_callback(callback, state)
                
            except Exception as e:
                print(f"Error showing previous application: {e}")
                await callback.answer("Xatolik yuz berdi", show_alert=True)
                
        except Exception as e:
            print(f"Error in show_previous_application: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mgr_next_application")
    async def show_next_application(callback: CallbackQuery, state: FSMContext):
        """Keyingi arizani ko'rsatish"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return

            # State'dan joriy indeksni olish
            data = await state.get_data()
            current_index = data.get('current_application_index', 0)
            
            # Keyingi indeksga o'tish
            await state.update_data(current_application_index=current_index + 1)
            
            # Ariza ro'yxatini qayta ko'rsatish
            try:
                await view_all_applications_callback(callback, state)
                
            except Exception as e:
                print(f"Error showing next application: {e}")
                await callback.answer("Xatolik yuz berdi", show_alert=True)
                
        except Exception as e:
            print(f"Error in show_next_application: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    async def view_all_applications_callback(callback: CallbackQuery, state: FSMContext):
        """Callback uchun ariza ro'yxatini ko'rsatish"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            
            # Use workflow access control to get filtered requests for manager role
            access_control = MockWorkflowAccessControl()
            requests = await access_control.get_filtered_requests_for_role(
                user_id=user['id'],
                user_role='manager'
            )
            
            if not requests:
                text = "Hozircha hech qanday ariza yo'q."
                
                # Use edit_and_track for inline cleanup
                await callback.message.edit_text(text, reply_markup=get_manager_back_keyboard(lang))
                return
            
            # Foydalanuvchi state'da joriy zayavka indeksini saqlash
            data = await state.get_data()
            current_index = data.get('current_application_index', 0)
            
            # Indeksni cheklash
            if current_index >= len(requests):
                current_index = 0
            elif current_index < 0:
                current_index = len(requests) - 1
            
            # Joriy zayavka ma'lumotlari
            current_request = requests[current_index]
            
            # Status belgilarini aniqlash
            status_emoji = {
                'created': '🆕',
                'in_progress': '⏳',
                'completed': '✅',
                'cancelled': '❌'
            }.get(current_request.get('current_status', 'created'), '📋')
            
            workflow_type = current_request.get('workflow_type', 'unknown')
            workflow_emoji = {
                'connection_request': '🔌',
                'technical_service': '🔧',
                'call_center_direct': '📞'
            }.get(workflow_type, '📋')
            
            # Zayavka turini formatlash
            workflow_type_text = {
                'connection_request': 'Ulanish arizasi',
                'technical_service': 'Texnik xizmat',
                'call_center_direct': 'Qo\'ng\'iroq markazi'
            }.get(workflow_type, 'Noma\'lum')
            
            # Mijoz ma'lumotlari
            client_name = current_request.get('contact_info', {}).get('full_name', 'N/A') if isinstance(current_request.get('contact_info'), dict) else 'N/A'
            client_phone = current_request.get('contact_info', {}).get('phone', 'N/A') if isinstance(current_request.get('contact_info'), dict) else 'N/A'
            
            # Vaqt ma'lumotlari
            created_at = current_request.get('created_at', 'N/A')
            updated_at = current_request.get('updated_at', 'N/A')
            
            # Vaqt hisoblash
            total_duration = "N/A"
            if created_at and created_at != 'N/A':
                try:
                    if isinstance(created_at, str):
                        created_dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    else:
                        created_dt = created_at
                    
                    current_time = datetime.now()
                    if created_dt.tzinfo is None:
                        created_dt = created_dt.replace(tzinfo=None)
                    
                    duration = current_time - created_dt
                    total_hours = int(duration.total_seconds() // 3600)
                    total_minutes = int((duration.total_seconds() % 3600) // 60)
                    
                    if total_hours > 0:
                        total_duration = f"{total_hours}s {total_minutes}d"
                    else:
                        total_duration = f"{total_minutes} daqiqa"
                except:
                    total_duration = "N/A"
            
            # Izoh va diagnostika
            description = current_request.get('description', 'Izoh yo\'q')
            location = current_request.get('location', 'Manzil ko\'rsatilmagan')
            
            # Joriy rol va status
            current_role = current_request.get('role_current', 'Noma\'lum')
            current_status = current_request.get('current_status', 'Noma\'lum')
            
            # Status matnini formatlash
            status_text = {
                'created': 'Yaratilgan',
                'in_progress': 'Jarayonda',
                'completed': 'Tugallangan',
                'cancelled': 'Bekor qilingan'
            }.get(current_status, current_status)
            
            text = f"""
📋 <b>Ariza #{current_index + 1} / {len(requests)}</b>

{status_emoji}{workflow_emoji} <b>{client_name}</b>
   📋 ID: {current_request['id'][:8]}...
   🏷️ Turi: {workflow_type_text}
   📊 Status: {status_text}
   👤 Joriy rol: {current_role}

📞 <b>Mijoz ma'lumotlari:</b>
   • Nomi: {client_name}
   • Telefon: {client_phone}
   • Manzil: {location}

⏰ <b>Vaqt ma'lumotlari:</b>
   • Yaratilgan: {created_at}
   • Yangilangan: {updated_at}
   • Umumiy vaqt: {total_duration}

📝 <b>Izoh va diagnostika:</b>
   {description}

🔧 <b>Texnik ma'lumotlar:</b>
   • Workflow type: {workflow_type}
   • Current status: {current_status}
   • Role current: {current_role}
"""
            
            # Navigatsiya tugmalari
            keyboard_buttons = []
            
            # Agar 1tadan ko'p zayavka bo'lsa, navigatsiya tugmalarini qo'shish
            if len(requests) > 1:
                keyboard_buttons.append([
                    InlineKeyboardButton(
                        text="◀️ Oldingi",
                        callback_data="mgr_prev_application"
                    ),
                    InlineKeyboardButton(
                        text="Keyingi ▶️",
                        callback_data="mgr_next_application"
                    )
                ])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
            
            # State'da joriy indeksni saqlash
            await state.update_data(current_application_index=current_index)
            
            # Use edit_and_track for inline cleanup
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            print(f"Error in view_all_applications_callback: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    return router 