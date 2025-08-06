from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

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

async def get_system_statistics():
    """Mock system statistics"""
    return {
        'total_orders': 150,
        'completed_orders': 120,
        'pending_orders': 30,
        'active_clients': 45,
        'active_technicians': 12,
        'revenue_today': 2500000,
        'avg_completion_time': 2.5
    }

async def get_all_technicians():
    """Mock technicians data"""
    return [
        {
            'id': 1,
            'full_name': 'Technician 1',
            'is_active': True
        },
        {
            'id': 2,
            'full_name': 'Technician 2',
            'is_active': True
        },
        {
            'id': 3,
            'full_name': 'Technician 3',
            'is_active': False
        }
    ]

async def get_technician_performance(tech_id: int):
    """Mock technician performance"""
    return {
        'completed_orders': 25,
        'active_orders': 3,
        'avg_rating': 4.5
    }

async def get_service_quality_metrics():
    """Mock quality metrics"""
    return {
        'avg_rating': 4.3,
        'total_reviews': 85,
        'satisfaction_rate': 92,
        'rating_distribution': {
            5: 45,
            4: 25,
            3: 10,
            2: 3,
            1: 2
        }
    }

async def get_all_orders(limit: int = 100):
    """Mock orders data"""
    return [
        {
            'id': 1,
            'status': 'completed',
            'created_at': datetime.now() - timedelta(hours=2)
        },
        {
            'id': 2,
            'status': 'in_progress',
            'created_at': datetime.now() - timedelta(hours=1)
        },
        {
            'id': 3,
            'status': 'new',
            'created_at': datetime.now()
        }
    ]

async def get_role_router(role: str):
    """Mock role router"""
    from aiogram import Router
    return Router()

# Mock keyboards
def reports_menu(lang: str):
    """Mock reports menu keyboard"""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📈 Tizim hisoboti", callback_data="system_report"),
            InlineKeyboardButton(text="👨‍🔧 Texniklar hisoboti", callback_data="technicians_report")
        ],
        [
            InlineKeyboardButton(text="⭐ Sifat hisoboti", callback_data="quality_report"),
            InlineKeyboardButton(text="📅 Kunlik hisobot", callback_data="daily_report")
        ],
        [
            InlineKeyboardButton(text="📊 Haftalik hisobot", callback_data="weekly_report")
        ],
        [
            InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_controllers")
        ]
    ])

def back_to_controllers_menu(lang: str):
    """Mock back to controllers menu keyboard"""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_controllers")
        ]
    ])

# Mock states
class ControllerReportsStates:
    reports_menu = "reports_menu"

def get_controller_reports_router():
    """Get controller reports router"""
    from utils.role_system import get_role_router
    router = get_role_router("controller")

    @router.message(F.text.in_(["📊 Hisobotlar"]))
    async def reports_menu_handler(message: Message, state: FSMContext):
        """Hisobotlar menyusi"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            
            lang = user.get('language', 'uz')
            await state.set_state(ControllerReportsStates.reports_menu)
            
            text = """📊 <b>Hisobotlar bo'limi</b>

Quyidagi hisobotlarni olishingiz mumkin:

• Tizim hisoboti
• Texniklar hisoboti  
• Sifat hisoboti
• Kunlik hisobot
• Haftalik hisobot

Kerakli hisobotni tanlang:"""
            
            await message.answer(
                text,
                reply_markup=reports_menu(lang),
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in reports menu handler: {e}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    @router.message(F.text.in_(["📈 Tizim hisoboti"]))
    async def system_report(message: Message, state: FSMContext):
        """Tizim hisoboti"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            
            lang = user.get('language', 'uz')
            
            try:
                # Get real system statistics from database
                stats = await get_system_statistics()
                
                text = f"""📈 <b>Tizim hisoboti</b>
📅 <b>Sana:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}

📊 <b>Buyurtmalar:</b>
• Jami buyurtmalar: {stats.get('total_orders', 0)}
• Bajarilgan buyurtmalar: {stats.get('completed_orders', 0)}
• Kutilayotgan buyurtmalar: {stats.get('pending_orders', 0)}

👥 <b>Foydalanuvchilar:</b>
• Faol mijozlar: {stats.get('active_clients', 0)}
• Faol texniklar: {stats.get('active_technicians', 0)}

💰 <b>Moliyaviy ko'rsatkichlar:</b>
• Bugungi tushum: {stats.get('revenue_today', 0):,} so'm
• O'rtacha bajarish vaqti: {stats.get('avg_completion_time', 0)} soat

📊 <b>Samaradorlik:</b>
• Bajarish foizi: {(stats.get('completed_orders', 0) / max(stats.get('total_orders', 1), 1) * 100):.1f}%"""
                
                await message.answer(
                    text,
                    parse_mode='HTML'
                )
                
            except Exception as e:
                print(f"Error in system report: {e}")
                error_text = "Hisobotni olishda xatolik"
                await message.answer(error_text)
                
        except Exception as e:
            print(f"Error in system report: {e}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    @router.message(F.text.in_(["👨‍🔧 Texniklar hisoboti"]))
    async def technicians_report(message: Message, state: FSMContext):
        """Texniklar hisoboti"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            
            lang = user.get('language', 'uz')
            
            try:
                # Get real technicians data from database
                technicians = await get_all_technicians()
                
                # Statistikani hisoblash
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
                
                text = f"""👨‍🔧 <b>Texniklar hisoboti</b>
📅 <b>Sana:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}

👥 <b>Texniklar soni:</b>
• Jami texniklar: {total_technicians}
• Faol texniklar: {active_technicians}
• Nofaol texniklar: {total_technicians - active_technicians}

📊 <b>Ish samaradorligi:</b>
• Jami bajarilgan vazifalar: {total_completed}
• Hozir jarayonda: {total_active}
• O'rtacha reyting: {avg_rating:.1f}/5.0

📈 <b>Eng faol texniklar:</b>"""
                
                # Eng faol texniklar
                performance_data = []
                for tech in technicians:
                    performance = await get_technician_performance(tech['id'])
                    performance_data.append({
                        'name': tech['full_name'],
                        'completed': performance.get('completed_orders', 0),
                        'rating': performance.get('avg_rating', 0)
                    })
                
                performance_data.sort(key=lambda x: x['completed'], reverse=True)
                
                for i, perf in enumerate(performance_data[:5], 1):
                    text += f"\n{i}. {perf['name']} - {perf['completed']} vazifa (⭐{perf['rating']:.1f})"
                
                await message.answer(
                    text,
                    parse_mode='HTML'
                )
                
            except Exception as e:
                print(f"Error in technicians report: {e}")
                error_text = "Hisobotni olishda xatolik"
                await message.answer(error_text)
                
        except Exception as e:
            print(f"Error in technicians report: {e}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    @router.message(F.text.in_(["⭐ Sifat hisoboti"]))
    async def quality_report(message: Message, state: FSMContext):
        """Sifat hisoboti"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            
            lang = user.get('language', 'uz')
            
            try:
                # Get real quality metrics from database
                quality_metrics = await get_service_quality_metrics()
                
                text = f"""⭐ <b>Sifat hisoboti</b>
📅 <b>Sana:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}

📊 <b>Umumiy ko'rsatkichlar:</b>
• O'rtacha baho: {quality_metrics.get('avg_rating') or 0:.1f}/5.0
• Jami sharhlar: {quality_metrics.get('total_reviews', 0)}
• Mijoz qoniqishi: {quality_metrics.get('satisfaction_rate', 0)}%

📈 <b>Baholar taqsimoti:</b>"""
                
                # Baholar taqsimoti
                rating_distribution = quality_metrics.get('rating_distribution', {})
                total_reviews = quality_metrics.get('total_reviews', 0)
                
                for rating in range(5, 0, -1):
                    count = rating_distribution.get(rating, 0)
                    percentage = (count / total_reviews * 100) if total_reviews > 0 else 0
                    stars = "⭐" * rating
                    text += f"\n{stars} {count} ({percentage:.1f}%)"
                
                await message.answer(
                    text,
                    parse_mode='HTML'
                )
                
            except Exception as e:
                print(f"Error in quality report: {e}")
                error_text = "Hisobotni olishda xatolik"
                await message.answer(error_text)
                
        except Exception as e:
            print(f"Error in quality report: {e}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    @router.message(F.text.in_(["📅 Kunlik hisobot"]))
    async def daily_report(message: Message, state: FSMContext):
        """Kunlik hisobot"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            
            lang = user.get('language', 'uz')
            
            try:
                # Get real daily data from database
                today = datetime.now().date()
                orders = await get_all_orders(limit=100)
                today_orders = [o for o in orders if o.get('created_at') and o['created_at'].date() == today]
                
                completed_today = len([o for o in today_orders if o['status'] == 'completed'])
                new_today = len([o for o in today_orders if o['status'] == 'new'])
                in_progress_today = len([o for o in today_orders if o['status'] == 'in_progress'])
                
                text = f"""📅 <b>Kunlik hisobot</b>
📅 <b>Sana:</b> {today.strftime('%d.%m.%Y')}

📊 <b>Bugungi buyurtmalar:</b>
• Jami yangi: {new_today}
• Jarayonda: {in_progress_today}
• Bajarilgan: {completed_today}
• Jami: {len(today_orders)}

📈 <b>Samaradorlik:</b>
• Bajarish foizi: {(completed_today / max(len(today_orders), 1) * 100):.1f}%

⏰ <b>Hisobot vaqti:</b> {datetime.now().strftime('%H:%M')}"""
                
                await message.answer(
                    text,
                    parse_mode='HTML'
                )
                
            except Exception as e:
                print(f"Error in daily report: {e}")
                error_text = "Hisobotni olishda xatolik"
                await message.answer(error_text)
                
        except Exception as e:
            print(f"Error in daily report: {e}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    @router.message(F.text.in_(["📊 Haftalik hisobot"]))
    async def weekly_report(message: Message, state: FSMContext):
        """Haftalik hisobot"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            
            lang = user.get('language', 'uz')
            
            try:
                # Get real weekly data from database
                today = datetime.now().date()
                week_ago = today - timedelta(days=7)
                
                orders = await get_all_orders(limit=200)
                week_orders = [o for o in orders if o.get('created_at') and o['created_at'].date() >= week_ago]
                
                completed_week = len([o for o in week_orders if o['status'] == 'completed'])
                new_week = len([o for o in week_orders if o['status'] == 'new'])
                
                text = f"""📊 <b>Haftalik hisobot</b>
📅 <b>Davr:</b> {week_ago.strftime('%d.%m.%Y')} - {today.strftime('%d.%m.%Y')}

📊 <b>Haftalik buyurtmalar:</b>
• Jami yangi: {new_week}
• Bajarilgan: {completed_week}
• Jami: {len(week_orders)}

📈 <b>Haftalik samaradorlik:</b>
• Bajarish foizi: {(completed_week / max(len(week_orders), 1) * 100):.1f}%
• Kunlik o'rtacha: {len(week_orders) / 7:.1f} buyurtma

⏰ <b>Hisobot vaqti:</b> {datetime.now().strftime('%H:%M')}"""
                
                await message.answer(
                    text,
                    parse_mode='HTML'
                )
                
            except Exception as e:
                print(f"Error in weekly report: {e}")
                error_text = "Hisobotni olishda xatolik"
                await message.answer(error_text)
                
        except Exception as e:
            print(f"Error in weekly report: {e}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    return router
