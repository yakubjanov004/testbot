"""
Menejer uchun real vaqtda kuzatish handleri - Soddalashtirilgan versiya
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
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



# Mock database functions
async def get_manager_realtime_dashboard(user_id: int):
    """Mock get manager realtime dashboard"""
    return {
        'total_active_requests': 5,
        'urgent_requests': 2,
        'normal_requests': 3,
        'requests': [
            {
                'id': 'req_001',
                'client_name': 'Ahmad Toshmatov',
                'workflow_type': 'connection_request',
                'status': 'in_progress',
                'current_role_actor_name': 'Umar Azimov',
                'current_role_actor_role': 'technician',
                'current_duration_text': '45 daqiqa',
                'created_at': '2024-01-15 10:30',
                'location': 'Toshkent sh., Chilonzor t.',
                'workflow_steps': 3,
                'total_duration_text': '2 soat 15 daqiqa',
                'status_emoji': '🟡',
                'realtime': {
                    'current_role_duration_minutes': 45
                }
            },
            {
                'id': 'req_002',
                'client_name': 'Malika Karimova',
                'workflow_type': 'technical_service',
                'status': 'urgent',
                'current_role_actor_name': 'Jahongir Karimov',
                'current_role_actor_role': 'junior_manager',
                'current_duration_text': '90 daqiqa',
                'created_at': '2024-01-15 09:15',
                'location': 'Toshkent sh., Sergeli t.',
                'workflow_steps': 4,
                'total_duration_text': '3 soat 30 daqiqa',
                'status_emoji': '🔴',
                'realtime': {
                    'current_role_duration_minutes': 90
                }
            }
        ]
    }

async def get_manager_detailed_requests(user_id: int):
    """Mock get manager detailed requests"""
    return {
        'requests': [
            {
                'id': 'req_001',
                'client_name': 'Ahmad Toshmatov',
                'workflow_type': 'connection_request',
                'status': 'in_progress',
                'current_role_actor_name': 'Umar Azimov',
                'current_role_actor_role': 'technician',
                'current_duration_text': '45 daqiqa',
                'created_at': '2024-01-15 10:30',
                'location': 'Toshkent sh., Chilonzor t.',
                'workflow_steps': 3,
                'total_duration_text': '2 soat 15 daqiqa',
                'status_emoji': '🟡'
            },
            {
                'id': 'req_002',
                'client_name': 'Malika Karimova',
                'workflow_type': 'technical_service',
                'status': 'urgent',
                'current_role_actor_name': 'Jahongir Karimov',
                'current_role_actor_role': 'junior_manager',
                'current_duration_text': '90 daqiqa',
                'created_at': '2024-01-15 09:15',
                'location': 'Toshkent sh., Sergeli t.',
                'workflow_steps': 4,
                'total_duration_text': '3 soat 30 daqiqa',
                'status_emoji': '🔴'
            }
        ],
        'total_count': 2
    }

async def get_workflow_time_summary(request_id: str):
    """Mock get workflow time summary"""
    return {
        'client_name': 'Ahmad Toshmatov',
        'total_duration_hours': 2,
        'total_duration_minutes': 15,
        'current_role': 'technician',
        'current_role_duration_minutes': 45
    }

async def get_request_workflow_summary(request_id: str):
    """Mock get request workflow summary"""
    return {
        'client_name': 'Ahmad Toshmatov',
        'workflow_type': 'connection_request',
        'current_status': 'in_progress',
        'total_steps': 3,
        'total_duration_hours': 2,
        'total_duration_minutes': 15,
        'workflow_steps': [
            {
                'step': 1,
                'role': 'client',
                'actor': 'Ahmad Toshmatov',
                'arrived': '2024-01-15 10:30',
                'left': '2024-01-15 10:45',
                'duration': '15 daqiqa',
                'is_current': False
            },
            {
                'step': 2,
                'role': 'controller',
                'actor': 'Controller User',
                'arrived': '2024-01-15 10:45',
                'left': '2024-01-15 11:00',
                'duration': '15 daqiqa',
                'is_current': False
            },
            {
                'step': 3,
                'role': 'technician',
                'actor': 'Umar Azimov',
                'arrived': '2024-01-15 11:00',
                'left': None,
                'duration': '45 daqiqa',
                'is_current': True
            }
        ]
    }

def get_manager_realtime_monitoring_router():
    router = Router()

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
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="📋 Zayavkalar ro'yxati",
                            callback_data="mgr_realtime_requests"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="🚨 Shoshilinch zayavkalar",
                            callback_data="mgr_realtime_urgent"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="⏰ Vaqt kuzatish",
                            callback_data="mgr_time_tracking"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="📊 Workflow tarix",
                            callback_data="mgr_workflow_history"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="🔄 Yangilash",
                            callback_data="mgr_refresh_realtime"
                        )
                    ]
                ])

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
                total_count = detailed_data.get('total_count', 0)
                
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
                
                keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
                
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

    @router.callback_query(F.data == "mgr_request_info")
    async def show_request_info(callback: CallbackQuery, state: FSMContext):
        """Zayavka haqida ma'lumot"""
        await callback.answer("Bu zayavka haqida ma'lumot", show_alert=True)

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
                duration = request.get('realtime', {}).get('current_role_duration_minutes', 0)
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
            duration = current_request.get('realtime', {}).get('current_role_duration_minutes', 0)
            hours = int(duration // 60)
            minutes = int(duration % 60)
            
            # Zayavka ma'lumotlarini formatlash
            urgent_text = f"""
🚨 <b>Shoshilinch zayavka</b>

🔴 <b>{current_request.get('client_name', 'Noma\'lum')}</b>
   ⏰ {hours}s {minutes}d o'tdi
   📋 ID: {current_request.get('id', '')[:8]}...
   👤 Joriy: {current_request.get('realtime', {}).get('current_role_actor_name', 'Noma\'lum')} ({current_request.get('realtime', {}).get('current_role_actor_role', 'Noma\'lum')})
   📍 Manzil: {current_request.get('location', 'Manzil ko\'rsatilmagan')}
   📅 Yaratilgan: {current_request.get('created_at', 'Noma\'lum')}
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
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
            
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

    @router.callback_query(F.data == "mgr_prev_urgent")
    async def show_previous_urgent(callback: CallbackQuery, state: FSMContext):
        """Oldingi shoshilinch zayavkani ko'rsatish"""
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user['role'] != 'manager':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return

        # State'dan joriy indeksni olish
        data = await state.get_data()
        current_index = data.get('current_urgent_index', 0)
        
        # Oldingi indeksga o'tish
        await state.update_data(current_urgent_index=current_index - 1)
        
        # Zayavkani qayta ko'rsatish
        try:
            await show_urgent_requests(callback, state)
        except Exception as e:
            print(f"Error showing previous urgent: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mgr_next_urgent")
    async def show_next_urgent(callback: CallbackQuery, state: FSMContext):
        """Keyingi shoshilinch zayavkani ko'rsatish"""
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user['role'] != 'manager':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return

        # State'dan joriy indeksni olish
        data = await state.get_data()
        current_index = data.get('current_urgent_index', 0)
        
        # Keyingi indeksga o'tish
        await state.update_data(current_urgent_index=current_index + 1)
        
        # Zayavkani qayta ko'rsatish
        try:
            await show_urgent_requests(callback, state)
        except Exception as e:
            print(f"Error showing next urgent: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mgr_urgent_info")
    async def show_urgent_info(callback: CallbackQuery, state: FSMContext):
        """Shoshilinch zayavka haqida ma'lumot"""
        await callback.answer("Bu shoshilinch zayavka haqida ma'lumot", show_alert=True)

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
            time_summary = await get_workflow_time_summary(request_id)
            
            if "error" in time_summary:
                await callback.answer("Zayavka ma'lumotlarini olishda xatolik", show_alert=True)
                return
            
            # Zayavka ma'lumotlarini formatlash
            client_name = time_summary.get('client_name', 'Noma\'lum')
            total_hours = time_summary.get('total_duration_hours', 0)
            total_minutes = time_summary.get('total_duration_minutes', 0)
            current_role = time_summary.get('current_role', 'Noma\'lum')
            current_minutes = time_summary.get('current_role_duration_minutes', 0)
            
            # Vaqt formatlash
            total_time_text = f"{total_hours}s {total_minutes}d" if total_hours > 0 else f"{total_minutes} daqiqa"
            current_time_text = f"{current_minutes} daqiqa"
            
            # Status belgisini aniqlash
            status_emoji = "🟢" if current_minutes <= 30 else "🟡" if current_minutes <= 60 else "🔴"
            
            time_text = f"""
⏰ <b>Vaqt kuzatish #{current_index + 1} / {len(requests)}</b>

{status_emoji} <b>{client_name}</b>
   ⏰ Umumiy vaqt: {total_time_text}
   🔄 Joriy rol: {current_role} ({current_time_text})
   📋 ID: {request_id[:8]}...

📊 <b>Vaqt tahlili:</b>
   • Umumiy soat: {total_hours}
   • Umumiy daqiqa: {total_minutes}
   • Joriy rolda: {current_minutes} daqiqa
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
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
            
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

    @router.callback_query(F.data == "mgr_prev_time")
    async def show_previous_time(callback: CallbackQuery, state: FSMContext):
        """Oldingi vaqt kuzatishni ko'rsatish"""
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user['role'] != 'manager':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return

        # State'dan joriy indeksni olish
        data = await state.get_data()
        current_index = data.get('current_time_index', 0)
        
        # Oldingi indeksga o'tish
        await state.update_data(current_time_index=current_index - 1)
        
        # Vaqt kuzatishni qayta ko'rsatish
        try:
            await show_time_tracking(callback, state)
        except Exception as e:
            print(f"Error showing previous time: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mgr_next_time")
    async def show_next_time(callback: CallbackQuery, state: FSMContext):
        """Keyingi vaqt kuzatishni ko'rsatish"""
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user['role'] != 'manager':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return

        # State'dan joriy indeksni olish
        data = await state.get_data()
        current_index = data.get('current_time_index', 0)
        
        # Keyingi indeksga o'tish
        await state.update_data(current_time_index=current_index + 1)
        
        # Vaqt kuzatishni qayta ko'rsatish
        try:
            await show_time_tracking(callback, state)
        except Exception as e:
            print(f"Error showing next time: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mgr_refresh_realtime")
    async def refresh_realtime_dashboard(callback: CallbackQuery, state: FSMContext):
        """Real vaqtda dashboard yangilash"""
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user['role'] != 'manager':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return

        lang = user.get('language', 'uz')
        
        try:
            dashboard_data = await get_manager_realtime_dashboard(user['id'])
            
            if "error" in dashboard_data:
                await callback.answer("Yangilashda xatolik", show_alert=True)
                return
            
            # Yangilangan xabar
            dashboard_text = f"""
🕐 <b>Real vaqtda kuzatish</b>

📊 <b>Joriy holat:</b>
• Faol zayavkalar: {dashboard_data.get('total_active_requests', 0)}
• Shoshilinch: {dashboard_data.get('urgent_requests', 0)}
• Normal: {dashboard_data.get('normal_requests', 0)}

⏰ <b>Yangilangan:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}
"""
            
            # Klaviatura
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📋 Zayavkalar ro'yxati",
                        callback_data="mgr_realtime_requests"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🚨 Shoshilinch zayavkalar",
                        callback_data="mgr_realtime_urgent"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="⏰ Vaqt kuzatish",
                        callback_data="mgr_time_tracking"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📊 Workflow tarix",
                        callback_data="mgr_workflow_history"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔄 Yangilash",
                        callback_data="mgr_refresh_realtime"
                    )
                ]
            ])

            await callback.message.edit_text(dashboard_text, reply_markup=keyboard, parse_mode='HTML')
            await callback.answer()
            
        except Exception as e:
            print(f"Error refreshing realtime dashboard: {e}")
            await callback.answer("Yangilashda xatolik", show_alert=True)

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
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
            
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

    @router.callback_query(F.data == "mgr_prev_workflow")
    async def show_previous_workflow(callback: CallbackQuery, state: FSMContext):
        """Oldingi workflow tarixini ko'rsatish"""
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user['role'] != 'manager':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return

        # State'dan joriy indeksni olish
        data = await state.get_data()
        current_index = data.get('current_workflow_index', 0)
        
        # Oldingi indeksga o'tish
        await state.update_data(current_workflow_index=current_index - 1)
        
        # Workflow tarixini qayta ko'rsatish
        try:
            await show_workflow_history(callback, state)
        except Exception as e:
            print(f"Error showing previous workflow: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mgr_next_workflow")
    async def show_next_workflow(callback: CallbackQuery, state: FSMContext):
        """Keyingi workflow tarixini ko'rsatish"""
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user['role'] != 'manager':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return

        # State'dan joriy indeksni olish
        data = await state.get_data()
        current_index = data.get('current_workflow_index', 0)
        
        # Keyingi indeksga o'tish
        await state.update_data(current_workflow_index=current_index + 1)
        
        # Workflow tarixini qayta ko'rsatish
        try:
            await show_workflow_history(callback, state)
        except Exception as e:
            print(f"Error showing next workflow: {e}")
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
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📋 Zayavkalar ro'yxati",
                        callback_data="mgr_realtime_requests"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🚨 Shoshilinch zayavkalar",
                        callback_data="mgr_realtime_urgent"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="⏰ Vaqt kuzatish",
                        callback_data="mgr_time_tracking"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📊 Workflow tarix",
                        callback_data="mgr_workflow_history"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔄 Yangilash",
                        callback_data="mgr_refresh_realtime"
                    )
                ]
            ])

            await callback.message.edit_text(dashboard_text, reply_markup=keyboard, parse_mode='HTML')
            await callback.answer()
            
        except Exception as e:
            print(f"Error going back to realtime dashboard: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    return router 