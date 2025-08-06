"""
Controller handlers for Technician management - Soddalashtirilgan versiya

Bu modul controller uchun texniklarni boshqarish handlerlarini o'z ichiga oladi.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

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

async def get_user_lang(user_id: int):
    """Mock user language"""
    return 'uz'

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

async def get_all_technicians():
    """Mock all technicians"""
    return [
        {
            'id': 1,
            'full_name': 'Ahmad Toshmatov',
            'phone_number': '+998901234567',
            'specialization': 'Internet',
            'is_active': True,
            'current_location': 'Tashkent'
        },
        {
            'id': 2,
            'full_name': 'Bekzod Karimov',
            'phone_number': '+998901234568',
            'specialization': 'TV',
            'is_active': True,
            'current_location': 'Tashkent'
        },
        {
            'id': 3,
            'full_name': 'Dilshod Mirzayev',
            'phone_number': '+998901234569',
            'specialization': 'Telefon',
            'is_active': False,
            'current_location': 'Samarkand'
        },
        {
            'id': 4,
            'full_name': 'Eldor Umarov',
            'phone_number': '+998901234570',
            'specialization': 'Internet',
            'is_active': True,
            'current_location': 'Tashkent'
        }
    ]

async def get_technician_performance(technician_id: int):
    """Mock technician performance"""
    performance_data = {
        1: {'active_orders': 3, 'completed_orders': 45, 'avg_rating': 4.8},
        2: {'active_orders': 2, 'completed_orders': 38, 'avg_rating': 4.6},
        3: {'active_orders': 0, 'completed_orders': 12, 'avg_rating': 4.2},
        4: {'active_orders': 1, 'completed_orders': 52, 'avg_rating': 4.9}
    }
    return performance_data.get(technician_id, {'active_orders': 0, 'completed_orders': 0, 'avg_rating': 0})

async def get_orders_by_status(statuses: list):
    """Mock orders by status"""
    return [
        {
            'id': 'ord_001',
            'client_name': 'Aziz Karimov',
            'description': 'Internet tezligi sekin',
            'status': 'new',
            'created_at': '2024-01-15 10:30'
        },
        {
            'id': 'ord_002',
            'client_name': 'Malika Toshmatova',
            'description': 'TV signal yo\'q',
            'status': 'pending',
            'created_at': '2024-01-15 11:45'
        },
        {
            'id': 'ord_003',
            'client_name': 'Jamshid Mirzayev',
            'description': 'Telefon ishlamayapti',
            'status': 'new',
            'created_at': '2024-01-15 12:15'
        }
    ]

async def assign_zayavka_to_technician(zayavka_id: str, technician_id: int):
    """Mock assign zayavka to technician"""
    return True

# Mock keyboards
def technicians_menu(lang: str):
    """Mock technicians menu keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📋 Texniklar ro'yxati", callback_data="show_technicians_list"),
            InlineKeyboardButton(text="📊 Samaradorlik", callback_data="show_technicians_performance")
        ],
        [
            InlineKeyboardButton(text="🎯 Vazifa tayinlash", callback_data="task_assignment"),
            InlineKeyboardButton(text="📈 Hisobot", callback_data="technicians_report")
        ],
        [
            InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_controllers")
        ]
    ])

def technician_assignment_keyboard(technicians: list, lang: str):
    """Mock technician assignment keyboard"""
    keyboard = []
    
    for tech in technicians:
        if tech['is_active']:
            status_emoji = "🟢" if tech['is_active'] else "🔴"
            button_text = f"{status_emoji} {tech['full_name']} ({tech['specialization']})"
            keyboard.append([
                InlineKeyboardButton(
                    text=button_text,
                    callback_data=f"assign_to_technician_{tech['id']}"
                )
            ])
    
    keyboard.append([
        InlineKeyboardButton(
            text="❌ Bekor qilish",
            callback_data="cancel_assignment"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def back_to_controllers_menu(lang: str):
    """Mock back to controllers menu keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="◀️ Asosiy menyu", callback_data="back_to_main")
        ]
    ])

# Mock states
class ControllerTechnicianStates:
    technicians_control = "technicians_control"
    assign_technicians = "assign_technicians"
    viewing_technician = "viewing_technician"

def get_controller_technician_router():
    """Get controller technician router"""
    from utils.role_system import get_role_router
    router = get_role_router("controller")

    @router.message(F.text.in_(["👨‍🔧 Texniklar nazorati"]))
    async def technicians_control_menu(message: Message, state: FSMContext):
        """Texniklar nazorati menyusi"""
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
            await state.set_state(ControllerTechnicianStates.technicians_control)
            
            try:
                # Texniklar ro'yxatini olish
                technicians = await get_all_technicians()
                
                active_count = len([t for t in technicians if t['is_active']])
                total_count = len(technicians)
                
                text = f"""👨‍🔧 <b>Texniklar nazorati</b>

📊 <b>Umumiy ma'lumot:</b>
• Jami texniklar: {total_count}
• Faol texniklar: {active_count}
• Nofaol texniklar: {total_count - active_count}

Kerakli amalni tanlang:"""
                
                await send_and_track(
                    message.answer,
                    text,
                    user_id,
                    reply_markup=technicians_menu(lang),
                    parse_mode='HTML'
                )
                
            except Exception as e:
                print(f"Error in technicians_control_menu: {e}")
                error_text = "Xatolik yuz berdi!"
                await send_and_track(
                    message.answer,
                    error_text,
                    user_id
                )
                
        except Exception as e:
            print(f"Error in technicians_control_menu: {e}")
            error_text = "Xatolik yuz berdi!"
            await send_and_track(
                message.answer,
                error_text,
                user_id
            )

    @router.message(F.text.in_(["📋 Texniklar ro'yxati"]))
    async def show_technicians_list(message: Message, state: FSMContext):
        """Texniklar ro'yxatini ko'rsatish"""
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
            
            try:
                technicians = await get_all_technicians()
                
                text = "📋 <b>Texniklar ro'yxati:</b>\n\n"
                
                if technicians:
                    for tech in technicians:
                        status_icon = "🟢" if tech['is_active'] else "🔴"
                        performance = await get_technician_performance(tech['id'])
                        
                        text += f"{status_icon} <b>{tech['full_name']}</b>\n"
                        text += f"📞 {tech.get('phone_number', 'Noma\'lum')}\n"
                        
                        text += f"📋 Faol vazifalar: {performance.get('active_orders', 0)}\n"
                        text += f"✅ Bajarilgan: {performance.get('completed_orders', 0)}\n"
                        text += f"⭐ Reyting: {performance.get('avg_rating', 0):.1f}\n\n"
                else:
                    text += "Texniklar topilmadi"
                
                await send_and_track(
                    message.answer,
                    text,
                    user_id,
                    parse_mode='HTML'
                )
                
            except Exception as e:
                print(f"Error in show_technicians_list: {e}")
                error_text = "Xatolik yuz berdi!"
                await send_and_track(
                    message.answer,
                    error_text,
                    user_id
                )
                
        except Exception as e:
            print(f"Error in show_technicians_list: {e}")
            error_text = "Xatolik yuz berdi!"
            await send_and_track(
                message.answer,
                error_text,
                user_id
            )

    @router.message(F.text.in_(["📊 Texniklar samaradorligi"]))
    async def show_technicians_performance(message: Message, state: FSMContext):
        """Texniklar samaradorligini ko'rsatish"""
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
            
            try:
                technicians = await get_all_technicians()
                
                # Samaradorlik bo'yicha tartiblash
                performance_data = []
                for tech in technicians:
                    performance = await get_technician_performance(tech['id'])
                    performance_data.append({
                        'name': tech['full_name'],
                        'completed': performance.get('completed_orders', 0),
                        'active': performance.get('active_orders', 0),
                        'rating': performance.get('avg_rating', 0),
                        'is_active': tech['is_active']
                    })
                
                # Bajarilgan vazifalar bo'yicha tartiblash
                performance_data.sort(key=lambda x: x['completed'], reverse=True)
                
                text = "📊 <b>Texniklar samaradorligi:</b>\n\n"
                
                for i, perf in enumerate(performance_data[:10], 1):
                    status_icon = "🟢" if perf['is_active'] else "🔴"
                    medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                    
                    text += f"{medal} {status_icon} <b>{perf['name']}</b>\n"
                    text += f"   ✅ Bajarilgan: {perf['completed']}\n"
                    text += f"   📋 Faol: {perf['active']}\n"
                    text += f"   ⭐ Reyting: {perf['rating']:.1f}\n\n"
                
                await send_and_track(
                    message.answer,
                    text,
                    user_id,
                    parse_mode='HTML'
                )
                
            except Exception as e:
                print(f"Error in show_technicians_performance: {e}")
                error_text = "Xatolik yuz berdi!"
                await send_and_track(
                    message.answer,
                    error_text,
                    user_id
                )
                
        except Exception as e:
            print(f"Error in show_technicians_performance: {e}")
            error_text = "Xatolik yuz berdi!"
            await send_and_track(
                message.answer,
                error_text,
                user_id
            )

    @router.message(F.text.in_(["🎯 Vazifa tayinlash"]))
    async def task_assignment_menu(message: Message, state: FSMContext):
        """Vazifa tayinlash menyusi"""
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
            await state.set_state(ControllerTechnicianStates.assign_technicians)
            
            try:
                # Tayinlanmagan buyurtmalarni olish
                unassigned_orders = await get_orders_by_status(['new', 'pending'])
                
                text = f"""🎯 <b>Vazifa tayinlash</b>

📋 <b>Tayinlanmagan buyurtmalar:</b> {len(unassigned_orders)}

Quyidagi buyurtmalarni texniklarga tayinlashingiz mumkin:"""
                
                if unassigned_orders:
                    text += "\n\n"
                    for order in unassigned_orders[:5]:  # Faqat 5 tasini ko'rsatish
                        client_name = order.get('client_name', 'Noma\'lum')
                        description = order.get('description', '')[:40] + "..." if len(order.get('description', '')) > 40 else order.get('description', '')
                        
                        text += f"🔹 <b>#{order['id']}</b> - {client_name}\n"
                        text += f"📝 {description}\n\n"
                else:
                    text += "\n\nTayinlanmagan buyurtmalar yo'q"
                
                await send_and_track(
                    message.answer,
                    text,
                    user_id,
                    parse_mode='HTML'
                )
                
            except Exception as e:
                print(f"Error in task_assignment_menu: {e}")
                error_text = "Xatolik yuz berdi!"
                await send_and_track(
                    message.answer,
                    error_text,
                    user_id
                )
                
        except Exception as e:
            print(f"Error in task_assignment_menu: {e}")
            error_text = "Xatolik yuz berdi!"
            await send_and_track(
                message.answer,
                error_text,
                user_id
            )

    @router.message(F.text.in_(["📈 Texniklar hisoboti"]))
    async def technicians_report(message: Message, state: FSMContext):
        """Texniklar hisoboti"""
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
            
            try:
                technicians = await get_all_technicians()
                
                # Umumiy statistika
                total_technicians = len(technicians)
                active_technicians = len([t for t in technicians if t['is_active']])
                
                total_completed = 0
                total_active = 0
                total_rating = 0
                rated_count = 0
                
                for tech in technicians:
                    performance = await get_technician_performance(tech['id'])
                    total_completed += performance.get('completed_orders', 0)
                    total_active += performance.get('active_orders', 0)
                    
                    rating = performance.get('avg_rating', 0)
                    if rating > 0:
                        total_rating += rating
                        rated_count += 1
                
                avg_rating = (total_rating / rated_count) if rated_count > 0 else 0
                
                text = f"""📈 <b>Texniklar hisoboti</b>

👥 <b>Texniklar soni:</b>
• Jami: {total_technicians}
• Faol: {active_technicians}
• Nofaol: {total_technicians - active_technicians}

📊 <b>Ish samaradorligi:</b>
• Jami bajarilgan: {total_completed}
• Hozir jarayonda: {total_active}
• O'rtacha reyting: {avg_rating:.1f}

📅 <b>Hisobot sanasi:</b> {message.date.strftime('%d.%m.%Y %H:%M')}"""
                
                await send_and_track(
                    message.answer,
                    text,
                    user_id,
                    parse_mode='HTML'
                )
                
            except Exception as e:
                print(f"Error in technicians_report: {e}")
                error_text = "Xatolik yuz berdi!"
                await send_and_track(
                    message.answer,
                    error_text,
                    user_id
                )
                
        except Exception as e:
            print(f"Error in technicians_report: {e}")
            error_text = "Xatolik yuz berdi!"
            await send_and_track(
                message.answer,
                error_text,
                user_id
            )

    return router
