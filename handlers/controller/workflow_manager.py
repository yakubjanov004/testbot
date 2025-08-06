"""
Controller uchun workflow boshqaruvi - Soddalashtirilgan versiya

Bu modul controller uchun workflow boshqaruvi handlerlarini o'z ichiga oladi.
"""

from aiogram import F, Router
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

async def cleanup_user_inline_messages(user_id: int):
    """Mock cleanup function"""
    pass

async def get_controller_monitoring_data(db, user_id: int):
    """Mock controller monitoring data"""
    return {
        'today_total': 25,
        'today_assigned': 18,
        'today_completed': 12,
        'active_requests': 7,
        'active_technicians': 4,
        'total_technicians': 6
    }

async def get_pending_controller_requests(db):
    """Mock pending controller requests"""
    return [
        {
            'id': 'req_001',
            'client_name': 'Aziz Karimov',
            'description': 'Internet tezligi sekin',
            'priority': 'medium',
            'created_at': datetime.now()
        },
        {
            'id': 'req_002',
            'client_name': 'Malika Toshmatova',
            'description': 'TV signal yo\'q',
            'priority': 'high',
            'created_at': datetime.now()
        },
        {
            'id': 'req_003',
            'client_name': 'Jamshid Mirzayev',
            'description': 'Telefon ishlamayapti',
            'priority': 'urgent',
            'created_at': datetime.now()
        }
    ]

async def get_available_technicians(db):
    """Mock available technicians"""
    return [
        {
            'id': 1,
            'full_name': 'Ahmad Toshmatov',
            'phone': '+998901234567',
            'active_requests': 2,
            'is_active': True
        },
        {
            'id': 2,
            'full_name': 'Bekzod Karimov',
            'phone': '+998901234568',
            'active_requests': 0,
            'is_active': True
        },
        {
            'id': 3,
            'full_name': 'Dilshod Mirzayev',
            'phone': '+998901234569',
            'active_requests': 1,
            'is_active': False
        }
    ]

async def assign_request_to_technician(request_id: str, technician_id: int):
    """Mock assign request to technician"""
    return True

def get_controller_workflow_router():
    """Get controller workflow router"""
    router = get_role_router("controller")

    @router.message(F.text.in_(["🔄 Workflow boshqaruvi"]))
    async def workflow_management(message: Message, state: FSMContext):
        """Workflow boshqaruvi asosiy menyu"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                error_text = "Sizda ruxsat yo'q."
                await send_and_track(
                    message.answer,
                    error_text,
                    user_id
                )
                return

            lang = user.get('language', 'uz')
            
            try:
                # Monitoring ma'lumotlarini olish
                monitoring_data = await get_controller_monitoring_data(None, user['id'])
                
                workflow_text = f"""🔄 <b>Workflow boshqaruvi</b>

📊 <b>Bugungi statistika:</b>
• Jami ko'rilgan: {monitoring_data['today_total']}
• Texniklarga tayinlangan: {monitoring_data['today_assigned']}
• Yakunlangan: {monitoring_data['today_completed']}

⚡ <b>Joriy holat:</b>
• Faol zayavkalar: {monitoring_data['active_requests']}
• Faol texniklar: {monitoring_data['active_technicians']}/{monitoring_data['total_technicians']}

Kerakli amalni tanlang:"""
                
                # Workflow tugmalari
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="📋 Kutilayotgan zayavkalar", callback_data="ctrl_workflow_pending"),
                        InlineKeyboardButton(text="👨‍🔧 Texniklar holati", callback_data="ctrl_workflow_technicians")
                    ],
                    [
                        InlineKeyboardButton(text="📊 Umumiy monitoring", callback_data="ctrl_workflow_monitor")
                    ]
                ])
                
                await send_and_track(
                    message.answer,
                    workflow_text,
                    user_id,
                    parse_mode='HTML',
                    reply_markup=keyboard
                )
                
            except Exception as e:
                print(f"Error in workflow_management: {e}")
                error_text = "Xatolik yuz berdi"
                await send_and_track(
                    message.answer,
                    error_text,
                    user_id
                )
                
        except Exception as e:
            print(f"Error in workflow_management: {e}")
            error_text = "Xatolik yuz berdi"
            await send_and_track(
                message.answer,
                error_text,
                user_id
            )

    @router.callback_query(F.data == "ctrl_workflow_pending")
    async def show_pending_requests(callback: CallbackQuery):
        """Kutilayotgan zayavkalarni ko'rsatish"""
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return
                
            lang = user.get('language', 'uz')
            
            try:
                pending_requests = await get_pending_controller_requests(None)
                
                if not pending_requests:
                    no_pending_text = "📭 Kutilayotgan zayavkalar yo'q."
                    await edit_and_track(
                        callback.message.edit_text,
                        no_pending_text,
                        user_id,
                        parse_mode='HTML'
                    )
                    await callback.answer()
                    return
                
                # Pending requests ro'yxati
                pending_text = f"📋 <b>Kutilayotgan zayavkalar ({len(pending_requests)} ta):</b>\n\n"
                
                for i, request in enumerate(pending_requests[:10], 1):
                    priority_emoji = {
                        'low': '🟢',
                        'medium': '🟡', 
                        'high': '🟠',
                        'urgent': '🔴'
                    }.get(request.get('priority', 'medium'), '🟡')
                    
                    client_name = request.get('client_name', 'Noma\'lum')
                    desc = request.get('description', 'Tavsif yo\'q')[:50] + '...' if len(request.get('description', '')) > 50 else request.get('description', 'Tavsif yo\'q')
                    created = request['created_at'].strftime('%d.%m %H:%M') if request.get('created_at') else '-'
                    
                    pending_text += f"{i}. {priority_emoji} {client_name}\n"
                    pending_text += f"   📄 {desc}\n"
                    pending_text += f"   📅 {created}\n\n"
                
                # Tugmalar
                keyboard_buttons = []
                for i, request in enumerate(pending_requests[:5], 1):
                    button_text = f"{i}. {request.get('client_name', 'Noma\'lum')[:15]}..."
                    keyboard_buttons.append([
                        InlineKeyboardButton(
                            text=button_text,
                            callback_data=f"ctrl_process_pending_{request['id']}"
                        )
                    ])
                
                keyboard_buttons.append([
                    InlineKeyboardButton(text="◀️ Orqaga", callback_data="ctrl_workflow_back")
                ])
                
                keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
                
                await edit_and_track(
                    callback.message.edit_text,
                    pending_text,
                    user_id,
                    parse_mode='HTML',
                    reply_markup=keyboard
                )
                await callback.answer()
                
            except Exception as e:
                print(f"Error showing pending requests: {e}")
                error_text = "Xatolik yuz berdi"
                await callback.answer(error_text, show_alert=True)
                
        except Exception as e:
            print(f"Error showing pending requests: {e}")
            error_text = "Xatolik yuz berdi"
            await callback.answer(error_text, show_alert=True)

    @router.callback_query(F.data.startswith("ctrl_process_pending_"))
    async def process_pending_request(callback: CallbackQuery):
        """Kutilayotgan zayavkani qayta ishlash"""
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return
                
            lang = user.get('language', 'uz')
            request_id = callback.data.split("_")[-1]
            
            try:
                # Mock request info
                request_info = {
                    'id': request_id,
                    'client_name': 'Test Client',
                    'client_phone': '+998901234567',
                    'description': 'Test description',
                    'priority': 'O\'rta'
                }
                
                # Zayavka tafsilotlari
                process_text = f"""📋 <b>Zayavkani qayta ishlash</b>

🆔 <b>ID:</b> {request_info['id'][:8]}...
👤 <b>Mijoz:</b> {request_info.get('client_name', 'Noma\'lum')}
📞 <b>Telefon:</b> {request_info.get('client_phone', 'Noma\'lum')}
📄 <b>Ta'rif:</b> {request_info.get('description', 'Tavsif yo\'q')}
⚡ <b>Muhimlik:</b> {request_info.get('priority', 'O\'rta')}

Amalni tanlang:"""
                
                # Amallar tugmalari
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="👨‍🔧 Texnikka tayinlash", callback_data=f"ctrl_assign_tech_{request_id}"),
                        InlineKeyboardButton(text="📋 Batafsil ko'rish", callback_data=f"ctrl_view_request_{request_id}")
                    ],
                    [
                        InlineKeyboardButton(
                            text="📄 Word hujjat",
                            callback_data=f"ctrl_word_doc_{request_id[:20]}"
                        )
                    ],
                    [
                        InlineKeyboardButton(text="◀️ Orqaga", callback_data="ctrl_workflow_pending")
                    ]
                ])
                
                await edit_and_track(
                    callback.message.edit_text,
                    process_text,
                    user_id,
                    parse_mode='HTML',
                    reply_markup=keyboard
                )
                await callback.answer()
                
            except Exception as e:
                print(f"Error processing pending request: {e}")
                error_text = "Xatolik yuz berdi"
                await callback.answer(error_text, show_alert=True)
                
        except Exception as e:
            print(f"Error processing pending request: {e}")
            error_text = "Xatolik yuz berdi"
            await callback.answer(error_text, show_alert=True)

    @router.callback_query(F.data == "ctrl_workflow_technicians")
    async def show_technicians_status(callback: CallbackQuery):
        """Texniklar holatini ko'rsatish"""
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return
                
            lang = user.get('language', 'uz')
            
            try:
                technicians = await get_available_technicians(None)
                
                if not technicians:
                    no_tech_text = "Texniklar topilmadi."
                    await edit_and_track(
                        callback.message.edit_text,
                        no_tech_text,
                        user_id,
                        parse_mode='HTML'
                    )
                    await callback.answer()
                    return
                
                # Texniklar holati
                tech_text = f"👨‍🔧 <b>Texniklar holati ({len(technicians)} ta):</b>\n\n"
                
                for tech in technicians:
                    status_emoji = "🟢" if tech['active_requests'] == 0 else "🟡" if tech['active_requests'] < 3 else "🔴"
                    activity_emoji = "✅" if tech['is_active'] else "❌"
                    
                    tech_text += f"{status_emoji} {activity_emoji} <b>{tech['full_name']}</b>\n"
                    tech_text += f"   📱 {tech.get('phone', 'Noma\'lum')}\n"
                    tech_text += f"   📊 Faol zayavkalar: {tech['active_requests']}\n\n"
                
                # Legend
                tech_text += "\n📖 <b>Belgilar:</b>\n"
                tech_text += "🟢 - Bo'sh  🟡 - Kam yuklangan  🔴 - Ko'p yuklangan\n"
                tech_text += "✅ - Faol  ❌ - Nofaol"
                
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="◀️ Orqaga", callback_data="ctrl_workflow_back")]
                ])
                
                await edit_and_track(
                    callback.message.edit_text,
                    tech_text,
                    user_id,
                    parse_mode='HTML',
                    reply_markup=keyboard
                )
                await callback.answer()
                
            except Exception as e:
                print(f"Error showing technicians status: {e}")
                error_text = "Xatolik yuz berdi"
                await callback.answer(error_text, show_alert=True)
                
        except Exception as e:
            print(f"Error showing technicians status: {e}")
            error_text = "Xatolik yuz berdi"
            await callback.answer(error_text, show_alert=True)

    @router.callback_query(F.data == "ctrl_workflow_monitor")
    async def show_general_monitoring(callback: CallbackQuery):
        """Umumiy monitoring ko'rsatish"""
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return
                
            lang = user.get('language', 'uz')
            
            try:
                monitoring_data = await get_controller_monitoring_data(None, user['id'])
                
                # Mock qo'shimcha statistika
                weekly_stats = {'total_week': 45, 'completed_week': 38}
                avg_completion = 2.5
                completion_percent = (weekly_stats['completed_week']/max(weekly_stats['total_week'], 1)*100) if weekly_stats and weekly_stats['total_week'] > 0 else 0
                
                monitor_text = f"""📊 <b>Umumiy monitoring</b>

📈 <b>Bugungi ko'rsatkichlar:</b>
• Jami ko'rilgan: {monitoring_data['today_total']}
• Tayinlangan: {monitoring_data['today_assigned']}
• Yakunlangan: {monitoring_data['today_completed']}

📊 <b>Haftalik statistika:</b>
• Jami zayavkalar: {weekly_stats['total_week']}
• Yakunlangan: {weekly_stats['completed_week']}
• Yakunlash foizi: {completion_percent:.1f}%

⚡ <b>Tizim holati:</b>
• Faol zayavkalar: {monitoring_data['active_requests']}
• Faol texniklar: {monitoring_data['active_technicians']}/{monitoring_data['total_technicians']}
• O'rtacha bajarish vaqti: {avg_completion:.1f} soat

🕐 <b>Yangilangan:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}"""
                
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="🔄 Yangilash", callback_data="ctrl_workflow_monitor"),
                        InlineKeyboardButton(text="◀️ Orqaga", callback_data="ctrl_workflow_back")
                    ]
                ])
                
                await edit_and_track(
                    callback.message.edit_text,
                    monitor_text,
                    user_id,
                    parse_mode='HTML',
                    reply_markup=keyboard
                )
                await callback.answer()
                
            except Exception as e:
                print(f"Error showing general monitoring: {e}")
                error_text = "Xatolik yuz berdi"
                await callback.answer(error_text, show_alert=True)
                
        except Exception as e:
            print(f"Error showing general monitoring: {e}")
            error_text = "Xatolik yuz berdi"
            await callback.answer(error_text, show_alert=True)

    @router.callback_query(F.data == "ctrl_workflow_back")
    async def workflow_back(callback: CallbackQuery):
        """Workflow menyusiga qaytish"""
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return
            
            try:
                await workflow_management(callback.message, None)
                await callback.answer()
                
            except Exception as e:
                print(f"Error in workflow_back: {e}")
                await callback.answer("Xatolik yuz berdi", show_alert=True)
                
        except Exception as e:
            print(f"Error in workflow_back: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("ctrl_word_doc_"))
    async def controller_generate_word(callback: CallbackQuery):
        """Generate Word document for controller"""
        user_id = callback.from_user.id
        
        try:
            await callback.answer()
            
            # Extract request_id
            request_id = callback.data.replace("ctrl_word_doc_", "")
            
            await callback.message.answer("📄 Word hujjat yaratilmoqda...")
            
            # Mock Word document generation
            await callback.message.answer(
                f"✅ Word hujjat tayyor!\n\nZayavka ID: {request_id[:8]}\nTuri: connection"
            )
            
        except Exception as e:
            print(f"Error generating Word document for controller: {e}")
            await callback.message.answer(f"Xatolik: {str(e)}")

    return router