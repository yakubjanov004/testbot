"""
Controller uchun realtime monitoring handleri - Soddalashtirilgan versiya
"""

from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from datetime import datetime

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

async def get_controller_realtime_dashboard(user_id: int):
    """Mock realtime dashboard data"""
    return {
        'total_active_requests': 15,
        'urgent_requests': 3,
        'normal_requests': 12,
        'requests': [
            {
                'id': 'req_001',
                'client_name': 'Client 1',
                'realtime': {
                    'current_role_duration_minutes': 45,
                    'current_role_actor_name': 'Technician 1',
                    'current_role_actor_role': 'technician'
                },
                'location': 'Tashkent, Chorsu',
                'created_at': '2024-01-15 10:30:00'
            },
            {
                'id': 'req_002',
                'client_name': 'Client 2',
                'realtime': {
                    'current_role_duration_minutes': 120,
                    'current_role_actor_name': 'Manager 1',
                    'current_role_actor_role': 'manager'
                },
                'location': 'Tashkent, Yunusabad',
                'created_at': '2024-01-15 09:15:00'
            },
            {
                'id': 'req_003',
                'client_name': 'Client 3',
                'realtime': {
                    'current_role_duration_minutes': 30,
                    'current_role_actor_name': 'Controller 1',
                    'current_role_actor_role': 'controller'
                },
                'location': 'Tashkent, Sergeli',
                'created_at': '2024-01-15 11:00:00'
            }
        ]
    }

async def get_workflow_time_summary(request_id: str):
    """Mock workflow time summary"""
    return {
        'client_name': 'Test Client',
        'total_duration_hours': 2,
        'total_duration_minutes': 30,
        'current_role': 'technician',
        'current_role_duration_minutes': 45
    }

async def get_request_workflow_summary(request_id: str):
    """Mock request workflow summary"""
    return {
        'client_name': 'Test Client',
        'workflow_type': 'technical_service',
        'current_status': 'in_progress',
        'total_steps': 5,
        'total_duration_hours': 2,
        'total_duration_minutes': 30,
        'workflow_steps': [
            {
                'step': 1,
                'role': 'client',
                'actor': 'Client Name',
                'arrived': '10:30',
                'left': '10:45',
                'duration': '15 daqiqa',
                'is_current': False
            },
            {
                'step': 2,
                'role': 'controller',
                'actor': 'Controller Name',
                'arrived': '10:45',
                'left': '11:00',
                'duration': '15 daqiqa',
                'is_current': False
            },
            {
                'step': 3,
                'role': 'technician',
                'actor': 'Technician Name',
                'arrived': '11:00',
                'left': None,
                'duration': '45 daqiqa',
                'is_current': True
            }
        ]
    }

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

def get_controller_realtime_monitoring_router():
    """Realtime monitoring router - Soddalashtirilgan"""
    from utils.role_system import get_role_router
    router = get_role_router("controller")

    @router.message(F.text.in_(["🕐 Real vaqtda kuzatish"]))
    async def show_realtime_dashboard(message: Message, state: FSMContext):
        """Real vaqtda dashboard ko'rsatish"""
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
            
            # Dashboard ma'lumotlarini olish
            dashboard_data = await get_controller_realtime_dashboard(user['id'])
            
            if "error" in dashboard_data:
                error_text = "Ma'lumotlarni olishda xatolik"
                await send_and_track(
                    message.answer,
                    error_text,
                    user_id
                )
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
                        callback_data="ctrl_realtime_requests"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🚨 Shoshilinch zayavkalar",
                        callback_data="ctrl_realtime_urgent"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="⏰ Vaqt kuzatish",
                        callback_data="ctrl_time_tracking"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📊 Workflow tarix",
                        callback_data="ctrl_workflow_history"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔄 Yangilash",
                        callback_data="ctrl_refresh_realtime"
                    )
                ]
            ])

            await send_and_track(
                message.answer,
                dashboard_text,
                user_id,
                reply_markup=keyboard,
                parse_mode='HTML'
            )

        except Exception as e:
            print(f"Error in controller realtime dashboard: {e}")
            error_text = "Xatolik yuz berdi"
            await send_and_track(
                message.answer,
                error_text,
                user_id
            )

    @router.callback_query(F.data == "ctrl_realtime_requests")
    async def show_realtime_requests(callback: CallbackQuery, state: FSMContext):
        """Real vaqtda zayavkalar ro'yxatini ko'rsatish"""
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await callback.answer("Sizda controller huquqi yo'q!", show_alert=True)
                return

            lang = user.get('language', 'uz')
            
            dashboard_data = await get_controller_realtime_dashboard(user['id'])
            
            if "error" in dashboard_data:
                await callback.answer("Xatolik yuz berdi", show_alert=True)
                return
            
            requests = dashboard_data.get('requests', [])
            
            if not requests:
                no_requests_text = "Faol zayavkalar yo'q"
                await callback.answer(no_requests_text, show_alert=True)
                return
            
            # Zayavkalar ro'yxati
            requests_text = "📋 <b>Faol zayavkalar:</b>\n\n"
            
            for request in requests[:10]:  # Faqat 10 tasi
                duration = request.get('realtime', {}).get('current_role_duration_minutes', 0)
                hours = int(duration // 60)
                minutes = int(duration % 60)
                
                status_emoji = "🚨" if duration > 30 else "⏳" if duration > 15 else "✅"
                
                requests_text += (
                    f"{status_emoji} {request.get('client_name', 'Noma\'lum')}\n"
                    f"   ⏰ {hours}s {minutes}d | ID: {request.get('id', '')[:8]}...\n\n"
                )
            
            # Orqaga qaytish tugmasi
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="⬅️ Orqaga",
                        callback_data="ctrl_back_to_realtime"
                    )
                ]
            ])
            
            await edit_and_track(
                callback.message.edit_text,
                requests_text,
                user_id,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            await callback.answer()
            
        except Exception as e:
            print(f"Error showing controller realtime requests: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "ctrl_realtime_urgent")
    async def show_urgent_requests(callback: CallbackQuery, state: FSMContext):
        """Shoshilinch zayavkalarni ko'rsatish"""
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await callback.answer("Sizda controller huquqi yo'q!", show_alert=True)
                return

            lang = user.get('language', 'uz')
            
            dashboard_data = await get_controller_realtime_dashboard(user['id'])
            
            if "error" in dashboard_data:
                await callback.answer("Xatolik yuz berdi", show_alert=True)
                return
            
            requests = dashboard_data.get('requests', [])
            urgent_requests = []
            
            # Shoshilinch zayavkalarni filtrlash (60 daqiqadan ko'p)
            for request in requests:
                duration = request.get('realtime', {}).get('current_role_duration_minutes', 0)
                if duration > 60:  # 60 daqiqadan ko'p
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
                        callback_data="ctrl_prev_urgent"
                    ),
                    InlineKeyboardButton(
                        text="Keyingi ▶️",
                        callback_data="ctrl_next_urgent"
                    )
                ])
            
            # Orqaga qaytish tugmasi har doim
            keyboard_buttons.append([
                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data="ctrl_back_to_realtime"
                )
            ])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
            
            # State'da joriy indeksni saqlash
            await state.update_data(current_urgent_index=current_index)
            
            try:
                await edit_and_track(
                    callback.message.edit_text,
                    urgent_text,
                    user_id,
                    reply_markup=keyboard,
                    parse_mode='HTML'
                )
            except Exception as e:
                if "message is not modified" in str(e):
                    await callback.answer()
                else:
                    await edit_and_track(
                        callback.message.edit_text,
                        urgent_text,
                        user_id,
                        reply_markup=keyboard,
                        parse_mode='HTML'
                    )
            
            await callback.answer()
            
        except Exception as e:
            print(f"Error showing controller urgent requests: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "ctrl_prev_urgent")
    async def show_previous_urgent(callback: CallbackQuery, state: FSMContext):
        """Oldingi shoshilinch zayavkani ko'rsatish"""
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await callback.answer("Sizda controller huquqi yo'q!", show_alert=True)
                return

            # State'dan joriy indeksni olish
            data = await state.get_data()
            current_index = data.get('current_urgent_index', 0)
            
            # Oldingi indeksga o'tish
            await state.update_data(current_urgent_index=current_index - 1)
            
            # Zayavkani qayta ko'rsatish
            await show_urgent_requests(callback, state)
            
        except Exception as e:
            print(f"Error showing previous urgent: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "ctrl_next_urgent")
    async def show_next_urgent(callback: CallbackQuery, state: FSMContext):
        """Keyingi shoshilinch zayavkani ko'rsatish"""
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await callback.answer("Sizda controller huquqi yo'q!", show_alert=True)
                return

            # State'dan joriy indeksni olish
            data = await state.get_data()
            current_index = data.get('current_urgent_index', 0)
            
            # Keyingi indeksga o'tish
            await state.update_data(current_urgent_index=current_index + 1)
            
            # Zayavkani qayta ko'rsatish
            await show_urgent_requests(callback, state)
            
        except Exception as e:
            print(f"Error showing next urgent: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "ctrl_time_tracking")
    async def show_time_tracking(callback: CallbackQuery, state: FSMContext):
        """Zayavka vaqt kuzatish ko'rsatish"""
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await callback.answer("Sizda controller huquqi yo'q!", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            
            # Dashboard ma'lumotlarini olish
            dashboard_data = await get_controller_realtime_dashboard(user['id'])
            
            if "error" in dashboard_data:
                error_text = "Xatolik yuz berdi"
                await callback.answer(error_text, show_alert=True)
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
                error_text = "Zayavka ma'lumotlarini olishda xatolik"
                await callback.answer(error_text, show_alert=True)
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
                        callback_data="ctrl_prev_time"
                    ),
                    InlineKeyboardButton(
                        text="Keyingi ▶️",
                        callback_data="ctrl_next_time"
                    )
                ])
            
            # Orqaga qaytish tugmasi har doim
            keyboard_buttons.append([
                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data="ctrl_back_to_realtime"
                )
            ])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
            
            # State'da joriy indeksni saqlash
            await state.update_data(current_time_index=current_index)
            
            await edit_and_track(
                callback.message.edit_text,
                time_text,
                user_id,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in show_time_tracking: {e}")
            error_text = "Xatolik yuz berdi"
            await callback.answer(error_text, show_alert=True)

    @router.callback_query(F.data == "ctrl_prev_time")
    async def show_previous_time(callback: CallbackQuery, state: FSMContext):
        """Oldingi vaqt kuzatishni ko'rsatish"""
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await callback.answer("Sizda controller huquqi yo'q!", show_alert=True)
                return
            
            # State'dan joriy indeksni olish
            data = await state.get_data()
            current_index = data.get('current_time_index', 0)
            
            # Oldingi indeksga o'tish
            new_index = current_index - 1
            await state.update_data(current_time_index=new_index)
            
            # Vaqt kuzatishni qayta ko'rsatish
            await show_time_tracking(callback, state)
            
        except Exception as e:
            print(f"Error in show_previous_time: {e}")
            error_text = "Xatolik yuz berdi"
            await callback.answer(error_text, show_alert=True)

    @router.callback_query(F.data == "ctrl_next_time")
    async def show_next_time(callback: CallbackQuery, state: FSMContext):
        """Keyingi vaqt kuzatishni ko'rsatish"""
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await callback.answer("Sizda controller huquqi yo'q!", show_alert=True)
                return
            
            # State'dan joriy indeksni olish
            data = await state.get_data()
            current_index = data.get('current_time_index', 0)
            
            # Keyingi indeksga o'tish
            new_index = current_index + 1
            await state.update_data(current_time_index=new_index)
            
            # Vaqt kuzatishni qayta ko'rsatish
            await show_time_tracking(callback, state)
            
        except Exception as e:
            print(f"Error in show_next_time: {e}")
            error_text = "Xatolik yuz berdi"
            await callback.answer(error_text, show_alert=True)

    @router.callback_query(F.data == "ctrl_workflow_history")
    async def show_workflow_history(callback: CallbackQuery, state: FSMContext):
        """Zayavka workflow tarixini ko'rsatish"""
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await callback.answer("Sizda controller huquqi yo'q!", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            
            # Dashboard ma'lumotlarini olish
            dashboard_data = await get_controller_realtime_dashboard(user['id'])
            
            if "error" in dashboard_data:
                error_text = "Xatolik yuz berdi"
                await callback.answer(error_text, show_alert=True)
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
                error_text = "Zayavka ma'lumotlarini olishda xatolik"
                await callback.answer(error_text, show_alert=True)
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
                        callback_data="ctrl_prev_workflow"
                    ),
                    InlineKeyboardButton(
                        text="Keyingi ▶️",
                        callback_data="ctrl_next_workflow"
                    )
                ])
            
            # Orqaga qaytish tugmasi har doim
            keyboard_buttons.append([
                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data="ctrl_back_to_realtime"
                )
            ])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
            
            # State'da joriy indeksni saqlash
            await state.update_data(current_workflow_index=current_index)
            
            await edit_and_track(
                callback.message.edit_text,
                history_text,
                user_id,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in show_workflow_history: {e}")
            error_text = "Xatolik yuz berdi"
            await callback.answer(error_text, show_alert=True)

    @router.callback_query(F.data == "ctrl_prev_workflow")
    async def show_previous_workflow(callback: CallbackQuery, state: FSMContext):
        """Oldingi workflow tarixini ko'rsatish"""
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await callback.answer("Sizda controller huquqi yo'q!", show_alert=True)
                return
            
            # State'dan joriy indeksni olish
            data = await state.get_data()
            current_index = data.get('current_workflow_index', 0)
            
            # Oldingi indeksga o'tish
            new_index = current_index - 1
            await state.update_data(current_workflow_index=new_index)
            
            # Workflow tarixini qayta ko'rsatish
            await show_workflow_history(callback, state)
            
        except Exception as e:
            print(f"Error in show_previous_workflow: {e}")
            error_text = "Xatolik yuz berdi"
            await callback.answer(error_text, show_alert=True)

    @router.callback_query(F.data == "ctrl_next_workflow")
    async def show_next_workflow(callback: CallbackQuery, state: FSMContext):
        """Keyingi workflow tarixini ko'rsatish"""
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await callback.answer("Sizda controller huquqi yo'q!", show_alert=True)
                return
            
            # State'dan joriy indeksni olish
            data = await state.get_data()
            current_index = data.get('current_workflow_index', 0)
            
            # Keyingi indeksga o'tish
            new_index = current_index + 1
            await state.update_data(current_workflow_index=new_index)
            
            # Workflow tarixini qayta ko'rsatish
            await show_workflow_history(callback, state)
            
        except Exception as e:
            print(f"Error in show_next_workflow: {e}")
            error_text = "Xatolik yuz berdi"
            await callback.answer(error_text, show_alert=True)

    @router.callback_query(F.data == "ctrl_refresh_realtime")
    async def refresh_realtime_dashboard(callback: CallbackQuery, state: FSMContext):
        """Real vaqtda dashboard yangilash"""
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await callback.answer("Sizda controller huquqi yo'q!", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            
            dashboard_data = await get_controller_realtime_dashboard(user['id'])
            
            if "error" in dashboard_data:
                error_text = "Yangilashda xatolik"
                await callback.answer(error_text, show_alert=True)
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
                        callback_data="ctrl_realtime_requests"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🚨 Shoshilinch zayavkalar",
                        callback_data="ctrl_realtime_urgent"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="⏰ Vaqt kuzatish",
                        callback_data="ctrl_time_tracking"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📊 Workflow tarix",
                        callback_data="ctrl_workflow_history"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔄 Yangilash",
                        callback_data="ctrl_refresh_realtime"
                    )
                ]
            ])

            await edit_and_track(
                callback.message.edit_text,
                dashboard_text,
                user_id,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in refresh_realtime_dashboard: {e}")
            error_text = "Yangilashda xatolik"
            await callback.answer(error_text, show_alert=True)

    @router.callback_query(F.data == "ctrl_back_to_realtime")
    async def back_to_realtime_dashboard(callback: CallbackQuery, state: FSMContext):
        """Asosiy realtime dashboardga qaytish"""
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await callback.answer("Sizda controller huquqi yo'q!", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            
            dashboard_data = await get_controller_realtime_dashboard(user['id'])
            
            if "error" in dashboard_data:
                error_text = "Xatolik yuz berdi"
                await callback.answer(error_text, show_alert=True)
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
                        callback_data="ctrl_realtime_requests"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🚨 Shoshilinch zayavkalar",
                        callback_data="ctrl_realtime_urgent"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="⏰ Vaqt kuzatish",
                        callback_data="ctrl_time_tracking"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📊 Workflow tarix",
                        callback_data="ctrl_workflow_history"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔄 Yangilash",
                        callback_data="ctrl_refresh_realtime"
                    )
                ]
            ])

            await edit_and_track(
                callback.message.edit_text,
                dashboard_text,
                user_id,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error going back to controller realtime dashboard: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    return router 