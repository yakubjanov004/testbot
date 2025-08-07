"""
Menejer uchun real vaqtda kuzatish handleri - Yaxshilangan versiya
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta
from filters.role_filter import RoleFilter
from keyboards.manager_buttons import (
    get_manager_realtime_keyboard,
    get_realtime_navigation_keyboard,
    get_realtime_refresh_keyboard
)

def calculate_time_duration(start_time: datetime, end_time: datetime = None) -> str:
    """Calculate time duration between start and end time"""
    if end_time is None:
        end_time = datetime.now()
    
    duration = end_time - start_time
    total_seconds = int(duration.total_seconds())
    
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    
    if hours > 0:
        return f"{hours}s {minutes}d"
    else:
        return f"{minutes} daqiqa"

def get_priority_emoji(priority: str) -> str:
    """Get priority emoji based on priority level"""
    priority_emojis = {
        'urgent': '🔴',
        'high': '🟠', 
        'normal': '🟡',
        'low': '🟢'
    }
    return priority_emojis.get(priority, '⚪')

def get_status_emoji(duration_minutes: int) -> str:
    """Get status emoji based on duration"""
    if duration_minutes <= 30:
        return '🟢'
    elif duration_minutes <= 60:
        return '🟡'
    else:
        return '🔴'

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

# Mock database functions
async def get_manager_realtime_dashboard(user_id: int):
    """Mock get manager realtime dashboard"""
    now = datetime.now()
    
    return {
        'total_active_requests': 12,
        'urgent_requests': 4,
        'normal_requests': 6,
        'low_priority_requests': 2,
        'requests': [
            {
                'id': 'req_001_2024_01_15',
                'client_name': 'Aziz Karimov',
                'workflow_type': 'connection_request',
                'status': 'in_progress',
                'current_role_actor_name': 'Umar Azimov',
                'current_role_actor_role': 'technician',
                'start_time': now - timedelta(hours=2, minutes=30),
                'current_role_start_time': now - timedelta(minutes=45),
                'current_duration_text': calculate_time_duration(now - timedelta(minutes=45)),
                'created_at': '2024-01-15 10:30',
                'location': 'Toshkent sh., Chilonzor t., 15-uy',
                'workflow_steps': 3,
                'total_duration_text': calculate_time_duration(now - timedelta(hours=2, minutes=30)),
                'status_emoji': get_status_emoji(45),
                'priority': 'high',
                'tariff': '100 Mbps',
                'connection_type': 'B2C',
                'duration_minutes': 150,
                'current_role_minutes': 45,
                'realtime': {
                    'current_role_duration_minutes': 45,
                    'total_duration_minutes': 135,
                    'estimated_completion': '15:45'
                }
            },
            {
                'id': 'req_002_2024_01_16',
                'client_name': 'Malika Toshmatova',
                'workflow_type': 'technical_service',
                'status': 'urgent',
                'current_role_actor_name': 'Jahongir Karimov',
                'current_role_actor_role': 'junior_manager',
                'current_duration_text': '90 daqiqa',
                'created_at': '2024-01-15 09:15',
                'location': 'Toshkent sh., Sergeli t., 45-uy',
                'workflow_steps': 4,
                'total_duration_text': '3 soat 30 daqiqa',
                'status_emoji': '🔴',
                'priority': 'urgent',
                'issue_type': 'TV signal yo\'q',
                'duration_minutes': 210,
                'current_role_minutes': 90,
                'realtime': {
                    'current_role_duration_minutes': 90,
                    'total_duration_minutes': 210,
                    'estimated_completion': '16:30'
                }
            },
            {
                'id': 'req_003_2024_01_17',
                'client_name': 'Jasur Rahimov',
                'workflow_type': 'connection_request',
                'status': 'in_progress',
                'current_role_actor_name': 'Shavkat Mirziyoyev',
                'current_role_actor_role': 'technician',
                'current_duration_text': '30 daqiqa',
                'created_at': '2024-01-15 11:00',
                'location': 'Toshkent sh., Yunusabad t., 78-uy',
                'workflow_steps': 2,
                'total_duration_text': '1 soat 45 daqiqa',
                'status_emoji': '🟡',
                'priority': 'normal',
                'tariff': '50 Mbps',
                'connection_type': 'B2B',
                'duration_minutes': 105,
                'current_role_minutes': 30,
                'realtime': {
                    'current_role_duration_minutes': 30,
                    'total_duration_minutes': 105,
                    'estimated_completion': '14:15'
                }
            },
            {
                'id': 'req_004_2024_01_18',
                'client_name': 'Dilfuza Karimova',
                'workflow_type': 'call_center_direct',
                'status': 'urgent',
                'current_role_actor_name': 'Ahmad Toshmatov',
                'current_role_actor_role': 'call_center_supervisor',
                'current_duration_text': '120 daqiqa',
                'created_at': '2024-01-15 08:45',
                'location': 'Toshkent sh., Chilanzar t., 23-uy',
                'workflow_steps': 5,
                'total_duration_text': '4 soat 20 daqiqa',
                'status_emoji': '🔴',
                'priority': 'urgent',
                'issue_type': 'Internet sekin ishlaydi',
                'duration_minutes': 260,
                'current_role_minutes': 120,
                'realtime': {
                    'current_role_duration_minutes': 120,
                    'total_duration_minutes': 260,
                    'estimated_completion': '17:00'
                }
            },
            {
                'id': 'req_005_2024_01_19',
                'client_name': 'Asadbek Abdullayev',
                'workflow_type': 'technical_service',
                'status': 'in_progress',
                'current_role_actor_name': 'Malika Karimova',
                'current_role_actor_role': 'technician',
                'current_duration_text': '15 daqiqa',
                'created_at': '2024-01-15 12:30',
                'location': 'Toshkent sh., Shayxontohur t., 67-uy',
                'workflow_steps': 2,
                'total_duration_text': '45 daqiqa',
                'status_emoji': '🟡',
                'priority': 'high',
                'issue_type': 'Router ishlamayapti',
                'duration_minutes': 45,
                'current_role_minutes': 15,
                'realtime': {
                    'current_role_duration_minutes': 15,
                    'total_duration_minutes': 45,
                    'estimated_completion': '13:30'
                }
            }
        ]
    }

async def get_manager_detailed_requests(user_id: int):
    """Mock get manager detailed requests"""
    return {
        'requests': [
            {
                'id': 'req_001_2024_01_15',
                'client_name': 'Aziz Karimov',
                'workflow_type': 'connection_request',
                'status': 'in_progress',
                'current_role_actor_name': 'Umar Azimov',
                'current_role_actor_role': 'technician',
                'current_duration_text': '45 daqiqa',
                'created_at': '2024-01-15 10:30',
                'location': 'Toshkent sh., Chilonzor t., 15-uy',
                'workflow_steps': 3,
                'total_duration_text': '2 soat 15 daqiqa',
                'status_emoji': '🟡',
                'priority': 'high',
                'tariff': '100 Mbps',
                'connection_type': 'B2C',
                'phone': '+998901234567',
                'description': 'Internet ulanish arizasi - yangi mijoz'
            },
            {
                'id': 'req_002_2024_01_16',
                'client_name': 'Malika Toshmatova',
                'workflow_type': 'technical_service',
                'status': 'urgent',
                'current_role_actor_name': 'Jahongir Karimov',
                'current_role_actor_role': 'junior_manager',
                'current_duration_text': '90 daqiqa',
                'created_at': '2024-01-15 09:15',
                'location': 'Toshkent sh., Sergeli t., 45-uy',
                'workflow_steps': 4,
                'total_duration_text': '3 soat 30 daqiqa',
                'status_emoji': '🔴',
                'priority': 'urgent',
                'issue_type': 'TV signal yo\'q',
                'phone': '+998901234568',
                'description': 'TV signal yo\'q - kabel uzilgan'
            },
            {
                'id': 'req_003_2024_01_17',
                'client_name': 'Jasur Rahimov',
                'workflow_type': 'connection_request',
                'status': 'in_progress',
                'current_role_actor_name': 'Shavkat Mirziyoyev',
                'current_role_actor_role': 'technician',
                'current_duration_text': '30 daqiqa',
                'created_at': '2024-01-15 11:00',
                'location': 'Toshkent sh., Yunusabad t., 78-uy',
                'workflow_steps': 2,
                'total_duration_text': '1 soat 45 daqiqa',
                'status_emoji': '🟡',
                'priority': 'normal',
                'tariff': '50 Mbps',
                'connection_type': 'B2B',
                'phone': '+998901234569',
                'description': 'Internet ulanish arizasi - korxona mijoz'
            }
        ]
    }

async def get_workflow_time_summary(request_id: str):
    """Mock get workflow time summary"""
    return {
        'client_name': 'Aziz Karimov',
        'total_duration_hours': 2,
        'total_duration_minutes': 15,
        'current_role': 'technician',
        'current_role_duration_minutes': 45,
        'estimated_completion_minutes': 30,
        'time_per_role': [
            {'role': 'call_center', 'duration_minutes': 30, 'role_name': 'Qo\'ng\'iroq markazi'},
            {'role': 'junior_manager', 'duration_minutes': 60, 'role_name': 'Kichik menejer'},
            {'role': 'technician', 'duration_minutes': 45, 'role_name': 'Texnik'}
        ],
        'average_time_per_role': 45,
        'total_roles_involved': 3,
        'next_role': 'warehouse'
    }

async def get_request_workflow_summary(request_id: str):
    """Mock get request workflow summary"""
    return {
        'client_name': 'Aziz Karimov',
        'workflow_type': 'connection_request',
        'current_status': 'in_progress',
        'total_steps': 4,
        'total_duration_hours': 2,
        'total_duration_minutes': 15,
        'priority': 'high',
        'tariff': '100 Mbps',
        'connection_type': 'B2C',
        'workflow_steps': [
            {
                'step': 1,
                'role': 'client',
                'actor': 'Aziz Karimov',
                'arrived': '2024-01-15 10:30',
                'left': '2024-01-15 10:45',
                'duration': '15 daqiqa',
                'is_current': False,
                'status': 'completed'
            },
            {
                'step': 2,
                'role': 'call_center',
                'actor': 'Malika Rahimova',
                'arrived': '2024-01-15 10:45',
                'left': '2024-01-15 11:15',
                'duration': '30 daqiqa',
                'is_current': False,
                'status': 'completed'
            },
            {
                'step': 3,
                'role': 'junior_manager',
                'actor': 'Jahongir Karimov',
                'arrived': '2024-01-15 11:15',
                'left': '2024-01-15 12:15',
                'duration': '60 daqiqa',
                'is_current': False,
                'status': 'completed'
            },
            {
                'step': 4,
                'role': 'technician',
                'actor': 'Umar Azimov',
                'arrived': '2024-01-15 12:15',
                'left': None,
                'duration': '45 daqiqa',
                'is_current': True,
                'status': 'in_progress'
            }
        ]
    }

def get_manager_realtime_monitoring_router():
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🕐 Real vaqtda kuzatish"]))
    async def show_realtime_dashboard(message: Message, state: FSMContext):
        """Manager realtime monitoring handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'manager':
                error_text = "Sizda ruxsat yo'q."
                await message.answer(error_text)
                return

            lang = user.get('language', 'uz')
            
            try:
                # Dashboard ma'lumotlarini olish
                dashboard_data = await get_manager_realtime_dashboard(user['id'])
                
                if "error" in dashboard_data:
                    error_text = "Ma'lumotlarni olishda xatolik"
                    await message.answer(error_text)
                    return
                
                # Xabar formatlash
                dashboard_text = f"""
🕐 <b>Real vaqtda kuzatish</b>

📊 <b>Joriy holat:</b>
• Faol zayavkalar: {dashboard_data.get('total_active_requests', 0)}
• Shoshilinch: {dashboard_data.get('urgent_requests', 0)}
• Normal: {dashboard_data.get('normal_requests', 0)}

⏰ <b>Yangilangan:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}
"""
                
                # Klaviatura
                keyboard = get_manager_realtime_keyboard(lang)

                await message.answer(dashboard_text, reply_markup=keyboard, parse_mode='HTML')

            except Exception as e:
                print(f"Error in realtime dashboard: {e}")
                error_text = "Dashboard ko'rsatishda xatolik"
                await message.answer(error_text)
                
        except Exception as e:
            print(f"Error in show_realtime_dashboard: {str(e)}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    @router.callback_query(F.data == "mgr_realtime_requests")
    async def show_realtime_requests(callback: CallbackQuery, state: FSMContext):
        """Real vaqtda zayavkalar ro'yxatini ko'rsatish"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return

            lang = user.get('language', 'uz')
            
            try:
                # Batafsil zayavkalar ma'lumotlarini olish
                detailed_data = await get_manager_detailed_requests(user['id'])
                
                if "error" in detailed_data:
                    await callback.answer("Xatolik yuz berdi", show_alert=True)
                    return
                
                requests = detailed_data.get('requests', [])
                total_count = len(requests)
                
                if not requests:
                    no_requests_text = "Faol zayavkalar yo'q"
                    await callback.answer(no_requests_text, show_alert=True)
                    return
                
                # Foydalanuvchi state'da joriy zayavka indeksini saqlash
                current_index = await state.get_data()
                current_index = current_index.get('current_request_index', 0)
                
                # Indeksni cheklash
                if current_index >= len(requests):
                    current_index = 0
                elif current_index < 0:
                    current_index = len(requests) - 1
                
                # Joriy zayavka ma'lumotlari
                current_request = requests[current_index]
                
                # Zayavka ma'lumotlarini formatlash
                request_text = f"""
📋 <b>Zayavka #{current_index + 1} / {total_count}</b>

{current_request['status_emoji']} <b>{current_request['client_name']}</b>
   📋 ID: {current_request['id'][:8]}...
   🏷️ Turi: {current_request['workflow_type']}
   📊 Status: {current_request['status']}
   👤 Joriy: {current_request['current_role_actor_name']} ({current_request['current_role_actor_role']})
   ⏰ Joriy rolda: {current_request['current_duration_text']}
   📅 Yaratilgan: {current_request['created_at']}
   📍 Manzil: {current_request['location']}

📊 <b>Umumiy ma'lumot:</b>
   • Jami qadamlar: {current_request['workflow_steps']}
   • Umumiy vaqt: {current_request['total_duration_text']}
"""
                
                # Navigatsiya tugmalari
                keyboard_buttons = []
                
                # Agar 1tadan ko'p zayavka bo'lsa, navigatsiya tugmalarini qo'shish
                if total_count > 1:
                    keyboard_buttons.append([
                        InlineKeyboardButton(
                            text="◀️ Oldingi",
                            callback_data="mgr_prev_request"
                        ),
                        InlineKeyboardButton(
                            text=f"{current_index + 1}/{total_count}",
                            callback_data="mgr_request_info"
                        ),
                        InlineKeyboardButton(
                            text="Keyingi ▶️",
                            callback_data="mgr_next_request"
                        )
                    ])
                else:
                    # Agar faqat 1ta zayavka bo'lsa, faqat raqamni ko'rsatish
                    keyboard_buttons.append([
                        InlineKeyboardButton(
                            text=f"1/1",
                            callback_data="mgr_request_info"
                        )
                    ])
                
                # Orqaga qaytish tugmasi har doim
                keyboard_buttons.append([
                    InlineKeyboardButton(
                        text="⬅️ Orqaga",
                        callback_data="mgr_back_to_realtime"
                    )
                ])
                
                keyboard = get_realtime_navigation_keyboard(lang=user.get('language', 'uz'))
                
                # State'da joriy indeksni saqlash
                await state.update_data(current_request_index=current_index)
                
                try:
                    await callback.message.edit_text(request_text, reply_markup=keyboard, parse_mode='HTML')
                except Exception as e:
                    if "message is not modified" in str(e):
                        # Xabar o'zgartirilmagan bo'lsa, faqat answer qilish
                        await callback.answer()
                    else:
                        # Boshqa xatolik bo'lsa, qayta urinish
                        await callback.message.edit_text(request_text, reply_markup=keyboard, parse_mode='HTML')
                
                await callback.answer()
                
            except Exception as e:
                print(f"Error showing detailed requests: {e}")
                await callback.answer("Xatolik yuz berdi", show_alert=True)
                
        except Exception as e:
            print(f"Error in show_realtime_requests: {str(e)}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mgr_prev_request")
    async def show_previous_request(callback: CallbackQuery, state: FSMContext):
        """Oldingi zayavkani ko'rsatish"""
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user['role'] != 'manager':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return

        # State'dan joriy indeksni olish
        data = await state.get_data()
        current_index = data.get('current_request_index', 0)
        
        # Oldingi indeksga o'tish
        await state.update_data(current_request_index=current_index - 1)
        
        # Zayavkani qayta ko'rsatish
        try:
            await show_realtime_requests(callback, state)
        except Exception as e:
            print(f"Error showing previous request: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mgr_next_request")
    async def show_next_request(callback: CallbackQuery, state: FSMContext):
        """Keyingi zayavkani ko'rsatish"""
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user['role'] != 'manager':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return

        # State'dan joriy indeksni olish
        data = await state.get_data()
        current_index = data.get('current_request_index', 0)
        
        # Keyingi indeksga o'tish
        await state.update_data(current_request_index=current_index + 1)
        
        # Zayavkani qayta ko'rsatish
        try:
            await show_realtime_requests(callback, state)
        except Exception as e:
            print(f"Error showing next request: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mgr_realtime_urgent")
    async def show_urgent_requests(callback: CallbackQuery, state: FSMContext):
        """Shoshilinch zayavkalarni ko'rsatish"""
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user['role'] != 'manager':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return

        lang = user.get('language', 'uz')
        
        try:
            dashboard_data = await get_manager_realtime_dashboard(user['id'])
            
            if "error" in dashboard_data:
                await callback.answer("Xatolik yuz berdi", show_alert=True)
                return
            
            requests = dashboard_data.get('requests', [])
            urgent_requests = []
            
            # Shoshilinch zayavkalarni filtrlash
            for request in requests:
                # Try both nested and direct field access for backwards compatibility
                duration = request.get('realtime', {}).get('current_role_duration_minutes', 0)
                if duration == 0:  # If nested structure doesn't have duration, try direct field
                    duration = request.get('current_role_minutes', 0)
                if duration > 60:  # 1 soatdan ko'p
                    urgent_requests.append(request)
            
            if not urgent_requests:
                no_urgent_text = "Shoshilinch zayavkalar yo'q"
                await callback.answer(no_urgent_text, show_alert=True)
                return
            
            # Foydalanuvchi state'da joriy zayavka indeksini saqlash
            data = await state.get_data()
            current_index = data.get('current_urgent_index', 0)
            
            # Indeksni cheklash
            if current_index >= len(urgent_requests):
                current_index = 0
            elif current_index < 0:
                current_index = len(urgent_requests) - 1
            
            # Joriy zayavka ma'lumotlari
            current_request = urgent_requests[current_index]
            duration_minutes = current_request.get('current_role_minutes', 0)
            total_duration = current_request.get('total_duration_text', 'Noma\'lum')
            current_role_duration = current_request.get('current_duration_text', 'Noma\'lum')
            
            # Zayavka ma'lumotlarini formatlash
            urgent_text = f"""
🚨 <b>Shoshilinch zayavka</b>

{get_status_emoji(duration_minutes)} <b>{current_request.get('client_name', 'Noma\'lum')}</b>
   ⏰ Joriy rolda: {current_role_duration}
   ⏰ Umumiy vaqt: {total_duration}
   📋 ID: {current_request.get('id', '')[:8]}...
   👤 Joriy: {current_request.get('current_role_actor_name', 'Noma\'lum')} ({current_request.get('current_role_actor_role', 'Noma\'lum')})
   📍 Manzil: {current_request.get('location', 'Manzil ko\'rsatilmagan')}
   📅 Yaratilgan: {current_request.get('created_at', 'Noma\'lum')}
   🏷️ Turi: {current_request.get('workflow_type', 'Noma\'lum')}
"""
            
            # Navigatsiya tugmalari
            keyboard_buttons = []
            
            # Agar 1tadan ko'p shoshilinch zayavka bo'lsa, navigatsiya tugmalarini qo'shish
            if len(urgent_requests) > 1:
                keyboard_buttons.append([
                    InlineKeyboardButton(
                        text="◀️ Oldingi",
                        callback_data="mgr_prev_urgent"
                    ),
                    InlineKeyboardButton(
                        text="Keyingi ▶️",
                        callback_data="mgr_next_urgent"
                    )
                ])
            
            # Orqaga qaytish tugmasi har doim
            keyboard_buttons.append([
                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data="mgr_back_to_realtime"
                )
            ])
            
            keyboard = get_realtime_navigation_keyboard(lang=user.get('language', 'uz'))
            
            # State'da joriy indeksni saqlash
            await state.update_data(current_urgent_index=current_index)
            
            try:
                await callback.message.edit_text(urgent_text, reply_markup=keyboard, parse_mode='HTML')
            except Exception as e:
                if "message is not modified" in str(e):
                    await callback.answer()
                else:
                    await callback.message.edit_text(urgent_text, reply_markup=keyboard, parse_mode='HTML')
            
            await callback.answer()
            
        except Exception as e:
            print(f"Error showing urgent requests: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mgr_time_tracking")
    async def show_time_tracking(callback: CallbackQuery, state: FSMContext):
        """Zayavka vaqt kuzatish ko'rsatish"""
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user['role'] != 'manager':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return

        lang = user.get('language', 'uz')
        
        try:
            # Dashboard ma'lumotlarini olish
            dashboard_data = await get_manager_realtime_dashboard(user['id'])
            
            if "error" in dashboard_data:
                await callback.answer("Xatolik yuz berdi", show_alert=True)
                return
            
            requests = dashboard_data.get('requests', [])
            
            if not requests:
                no_requests_text = "Faol zayavkalar yo'q"
                await callback.answer(no_requests_text, show_alert=True)
                return
            
            # Foydalanuvchi state'da joriy zayavka indeksini saqlash
            data = await state.get_data()
            current_index = data.get('current_time_index', 0)
            
            # Indeksni cheklash
            if current_index >= len(requests):
                current_index = 0
            elif current_index < 0:
                current_index = len(requests) - 1
            
            # Joriy zayavka ma'lumotlari
            current_request = requests[current_index]
            request_id = current_request.get('id')
            
            # Zayavka ma'lumotlarini formatlash
            client_name = current_request.get('client_name', 'Noma\'lum')
            total_duration = current_request.get('total_duration_text', 'Noma\'lum')
            current_role_duration = current_request.get('current_duration_text', 'Noma\'lum')
            current_role = current_request.get('current_role_actor_role', 'Noma\'lum')
            current_actor = current_request.get('current_role_actor_name', 'Noma\'lum')
            duration_minutes = current_request.get('current_role_minutes', 0)
            
            # Status belgisini aniqlash
            status_emoji = get_status_emoji(duration_minutes)
            priority_emoji = get_priority_emoji(current_request.get('priority', 'normal'))
            
            time_text = f"""
⏰ <b>Vaqt kuzatish #{current_index + 1} / {len(requests)}</b>

{status_emoji} <b>{client_name}</b>
   {priority_emoji} {current_request.get('workflow_type', 'Noma\'lum')}
   ⏰ Umumiy vaqt: {total_duration}
   🔄 Joriy rol: {current_role} ({current_role_duration})
   👤 Joriy: {current_actor}
   📋 ID: {request_id[:8]}...

📊 <b>Vaqt tahlili:</b>
   • Joriy rolda: {duration_minutes} daqiqa
   • Status: {current_request.get('status', 'Noma\'lum')}
   • Priority: {current_request.get('priority', 'Noma\'lum')}
"""
            
            # Navigatsiya tugmalari
            keyboard_buttons = []
            
            # Agar 1tadan ko'p zayavka bo'lsa, navigatsiya tugmalarini qo'shish
            if len(requests) > 1:
                keyboard_buttons.append([
                    InlineKeyboardButton(
                        text="◀️ Oldingi",
                        callback_data="mgr_prev_time"
                    ),
                    InlineKeyboardButton(
                        text="Keyingi ▶️",
                        callback_data="mgr_next_time"
                    )
                ])
            
            # Orqaga qaytish tugmasi har doim
            keyboard_buttons.append([
                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data="mgr_back_to_realtime"
                )
            ])
            
            keyboard = get_realtime_navigation_keyboard(lang=user.get('language', 'uz'))
            
            # State'da joriy indeksni saqlash
            await state.update_data(current_time_index=current_index)
            
            try:
                await callback.message.edit_text(time_text, reply_markup=keyboard, parse_mode='HTML')
            except Exception as e:
                if "message is not modified" in str(e):
                    await callback.answer()
                else:
                    await callback.message.edit_text(time_text, reply_markup=keyboard, parse_mode='HTML')
            
            await callback.answer()
            
        except Exception as e:
            print(f"Error showing time tracking: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mgr_workflow_history")
    async def show_workflow_history(callback: CallbackQuery, state: FSMContext):
        """Zayavka workflow tarixini ko'rsatish"""
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user['role'] != 'manager':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return

        lang = user.get('language', 'uz')
        
        try:
            # Dashboard ma'lumotlarini olish
            dashboard_data = await get_manager_realtime_dashboard(user['id'])
            
            if "error" in dashboard_data:
                await callback.answer("Xatolik yuz berdi", show_alert=True)
                return
            
            requests = dashboard_data.get('requests', [])
            
            if not requests:
                no_requests_text = "Faol zayavkalar yo'q"
                await callback.answer(no_requests_text, show_alert=True)
                return
            
            # Foydalanuvchi state'da joriy zayavka indeksini saqlash
            data = await state.get_data()
            current_index = data.get('current_workflow_index', 0)
            
            # Indeksni cheklash
            if current_index >= len(requests):
                current_index = 0
            elif current_index < 0:
                current_index = len(requests) - 1
            
            # Joriy zayavka ma'lumotlari
            current_request = requests[current_index]
            request_id = current_request.get('id')
            workflow_summary = await get_request_workflow_summary(request_id)
            
            if "error" in workflow_summary:
                await callback.answer("Zayavka ma'lumotlarini olishda xatolik", show_alert=True)
                return
            
            # Zayavka ma'lumotlarini formatlash
            client_name = workflow_summary.get('client_name', 'Noma\'lum')
            workflow_type = workflow_summary.get('workflow_type', 'Noma\'lum')
            current_status = workflow_summary.get('current_status', 'Noma\'lum')
            total_steps = workflow_summary.get('total_steps', 0)
            total_hours = workflow_summary.get('total_duration_hours', 0)
            total_minutes = workflow_summary.get('total_duration_minutes', 0)
            
            # Zayavka turini formatlash
            workflow_type_text = {
                'connection_request': 'Ulanish arizasi',
                'technical_service': 'Texnik xizmat',
                'call_center_direct': 'Qo\'ng\'iroq markazi'
            }.get(workflow_type, workflow_type)
            
            # Status belgisini aniqlash
            status_emoji = "🟢" if current_status == 'completed' else "🟡" if current_status == 'in_progress' else "🔴"
            
            history_text = f"""
📊 <b>Workflow tarix #{current_index + 1} / {len(requests)}</b>

{status_emoji} <b>{client_name}</b>
   🏷️ Turi: {workflow_type_text}
   📊 Status: {current_status}
   📋 Qadamlar: {total_steps}
   ⏰ Umumiy: {total_hours}s {total_minutes}d
   📋 ID: {request_id[:8]}...

📋 <b>Workflow qadamlar:</b>
"""
            
            # Har bir qadam uchun
            for step in workflow_summary.get('workflow_steps', [])[:5]:
                step_num = step['step']
                role = step['role']
                actor = step['actor']
                arrived = step['arrived']
                left = step['left']
                duration = step['duration']
                is_current = step['is_current']
                
                # Rol belgilarini aniqlash
                role_emoji = {
                    'client': '👤',
                    'controller': '🎛️',
                    'manager': '👨‍💼',
                    'junior_manager': '👨‍💼',
                    'technician': '🔧',
                    'call_center': '📞',
                    'warehouse': '📦'
                }.get(role.lower(), '👤')
                
                current_mark = " 🔄" if is_current else ""
                
                # Vaqt formatlash
                if arrived and left:
                    time_info = f"📅 {arrived} → {left}"
                elif arrived:
                    time_info = f"📅 {arrived} → hali tugamagan"
                else:
                    time_info = "📅 Vaqt ma'lum emas"
                
                history_text += (
                    f"   {step_num}. {role_emoji} {role} ({actor})\n"
                    f"      {time_info}\n"
                    f"      ⏰ {duration}{current_mark}\n\n"
                )
            
            # Navigatsiya tugmalari
            keyboard_buttons = []
            
            # Agar 1tadan ko'p zayavka bo'lsa, navigatsiya tugmalarini qo'shish
            if len(requests) > 1:
                keyboard_buttons.append([
                    InlineKeyboardButton(
                        text="◀️ Oldingi",
                        callback_data="mgr_prev_workflow"
                    ),
                    InlineKeyboardButton(
                        text="Keyingi ▶️",
                        callback_data="mgr_next_workflow"
                    )
                ])
            
            # Orqaga qaytish tugmasi har doim
            keyboard_buttons.append([
                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data="mgr_back_to_realtime"
                )
            ])
            
            keyboard = get_realtime_navigation_keyboard(lang=user.get('language', 'uz'))
            
            # State'da joriy indeksni saqlash
            await state.update_data(current_workflow_index=current_index)
            
            try:
                await callback.message.edit_text(history_text, reply_markup=keyboard, parse_mode='HTML')
            except Exception as e:
                if "message is not modified" in str(e):
                    await callback.answer()
                else:
                    await callback.message.edit_text(history_text, reply_markup=keyboard, parse_mode='HTML')
            
            await callback.answer()
            
        except Exception as e:
            print(f"Error showing workflow history: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mgr_back_to_realtime")
    async def back_to_realtime_dashboard(callback: CallbackQuery, state: FSMContext):
        """Asosiy realtime dashboardga qaytish"""
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user['role'] != 'manager':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return

        lang = user.get('language', 'uz')
        
        try:
            dashboard_data = await get_manager_realtime_dashboard(user['id'])
            
            if "error" in dashboard_data:
                await callback.answer("Xatolik yuz berdi", show_alert=True)
                return
            
            # Asosiy dashboard xabari
            dashboard_text = f"""
🕐 <b>Real vaqtda kuzatish</b>

📊 <b>Joriy holat:</b>
• Faol zayavkalar: {dashboard_data.get('total_active_requests', 0)}
• Shoshilinch: {dashboard_data.get('urgent_requests', 0)}
• Normal: {dashboard_data.get('normal_requests', 0)}

⏰ <b>Yangilangan:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}
"""
            
            # Klaviatura
            keyboard = get_manager_realtime_keyboard(lang)

            await callback.message.edit_text(dashboard_text, reply_markup=keyboard, parse_mode='HTML')
            await callback.answer()
            
        except Exception as e:
            print(f"Error going back to realtime dashboard: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    # Navigation handlers for different sections
    @router.callback_query(F.data.startswith("mgr_prev_"))
    async def show_previous_item(callback: CallbackQuery, state: FSMContext):
        """Oldingi elementni ko'rsatish"""
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user['role'] != 'manager':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return

        # State'dan joriy indeksni olish
        data = await state.get_data()
        item_type = callback.data.replace("mgr_prev_", "")
        
        if item_type == "request":
            current_index = data.get('current_request_index', 0)
            await state.update_data(current_request_index=current_index - 1)
            await show_realtime_requests(callback, state)
        elif item_type == "urgent":
            current_index = data.get('current_urgent_index', 0)
            await state.update_data(current_urgent_index=current_index - 1)
            await show_urgent_requests(callback, state)
        elif item_type == "time":
            current_index = data.get('current_time_index', 0)
            await state.update_data(current_time_index=current_index - 1)
            await show_time_tracking(callback, state)
        elif item_type == "workflow":
            current_index = data.get('current_workflow_index', 0)
            await state.update_data(current_workflow_index=current_index - 1)
            await show_workflow_history(callback, state)

    @router.callback_query(F.data.startswith("mgr_next_"))
    async def show_next_item(callback: CallbackQuery, state: FSMContext):
        """Keyingi elementni ko'rsatish"""
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user['role'] != 'manager':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return

        # State'dan joriy indeksni olish
        data = await state.get_data()
        item_type = callback.data.replace("mgr_next_", "")
        
        if item_type == "request":
            current_index = data.get('current_request_index', 0)
            await state.update_data(current_request_index=current_index + 1)
            await show_realtime_requests(callback, state)
        elif item_type == "urgent":
            current_index = data.get('current_urgent_index', 0)
            await state.update_data(current_urgent_index=current_index + 1)
            await show_urgent_requests(callback, state)
        elif item_type == "time":
            current_index = data.get('current_time_index', 0)
            await state.update_data(current_time_index=current_index + 1)
            await show_time_tracking(callback, state)
        elif item_type == "workflow":
            current_index = data.get('current_workflow_index', 0)
            await state.update_data(current_workflow_index=current_index + 1)
            await show_workflow_history(callback, state)

    @router.callback_query(F.data.startswith("mgr_request_info"))
    async def show_request_info(callback: CallbackQuery, state: FSMContext):
        """Zayavka haqida ma'lumot"""
        await callback.answer("Bu zayavka haqida ma'lumot", show_alert=True)

    return router