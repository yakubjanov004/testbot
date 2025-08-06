"""
Controller Reports Handler
Manages reports for controller
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional
from filters.role_filter import RoleFilter
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
    """Mock get system statistics"""
    return {
        'total_orders': 150,
        'completed_orders': 120,
        'pending_orders': 30,
        'active_clients': 85,
        'active_technicians': 12,
        'revenue_today': 2500000,
        'avg_completion_time': 2.5
    }

async def get_all_technicians():
    """Mock get all technicians"""
    return [
        {
            'id': 1,
            'full_name': 'Aziz Karimov',
            'role': 'technician',
            'active_orders': 3,
            'completed_today': 2,
            'avg_rating': 4.8,
            'status': 'active'
        },
        {
            'id': 2,
            'full_name': 'Malika Yusupova',
            'role': 'technician',
            'active_orders': 1,
            'completed_today': 3,
            'avg_rating': 4.6,
            'status': 'active'
        },
        {
            'id': 3,
            'full_name': 'Bekzod Toirov',
            'role': 'technician',
            'active_orders': 0,
            'completed_today': 1,
            'avg_rating': 4.4,
            'status': 'inactive'
        }
    ]

async def get_technician_performance(tech_id: int):
    """Mock get technician performance"""
    return {
        'total_orders': 45,
        'completed_orders': 42,
        'avg_completion_time': '2.1 soat',
        'customer_satisfaction': 4.7,
        'response_time': '15 daqiqa'
    }

async def get_service_quality_metrics():
    """Mock get service quality metrics"""
    return {
        'overall_quality': 4.5,
        'response_time_score': 4.3,
        'resolution_rate': 94,
        'customer_satisfaction': 88,
        'rework_rate': 6
    }

async def get_all_orders(limit: int = 100):
    """Mock get all orders"""
    return [
        {
            'id': 1,
            'order_number': 'ORD-001',
            'client_name': 'Test Client 1',
            'service_type': 'Internet xizmati',
            'status': 'Bajarilgan',
            'created_at': '2024-01-15 10:30',
            'completed_at': '2024-01-15 14:30',
            'assigned_to': 'Aziz Karimov',
            'rating': 5
        },
        {
            'id': 2,
            'order_number': 'ORD-002',
            'client_name': 'Test Client 2',
            'service_type': 'TV xizmati',
            'status': 'Jarayonda',
            'created_at': '2024-01-15 09:15',
            'completed_at': None,
            'assigned_to': 'Malika Yusupova',
            'rating': None
        }
    ]

def reports_menu(lang: str):
    """Create reports menu"""
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
            InlineKeyboardButton(text="📊 Haftalik hisobot", callback_data="weekly_report"),
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_controllers")
        ]
    ])

def back_to_controllers_menu(lang: str):
    """Create back to controllers menu"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_controllers")]
    ])

class ControllerReportsStates:
    reports_menu = "reports_menu"

def get_controller_reports_router():
    """Get controller reports router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("controller")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["📊 Hisobotlar"]))
    async def reports_menu_handler(message: Message, state: FSMContext):
        """Handle reports menu"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            
            lang = user.get('language', 'uz')
            
            reports_text = (
                "📊 <b>Hisobotlar</b>\n\n"
                "Tizim hisobotlarini ko'rish uchun kerakli bo'limni tanlang:\n\n"
                "📈 Tizim hisoboti - Umumiy statistika\n"
                "👨‍🔧 Texniklar hisoboti - Texniklar faoliyati\n"
                "⭐ Sifat hisoboti - Xizmat sifatini baholash\n"
                "📅 Kunlik hisobot - Bugungi natijalar\n"
                "📊 Haftalik hisobot - Haftalik tahlil"
            )
            
            await message.answer(
                reports_text,
                reply_markup=reports_menu(lang),
                parse_mode='HTML'
            )
            await state.set_state(ControllerReportsStates.reports_menu)
            
        except Exception as e:
            print(f"Error in reports_menu_handler: {str(e)}")
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
                active_technicians = len([t for t in technicians if t['status'] == 'active'])
                
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
• O'rtacha baho: {quality_metrics.get('overall_quality') or 0:.1f}/5.0
• Jami sharhlar: {quality_metrics.get('total_reviews', 0)}
• Mijoz qoniqishi: {quality_metrics.get('customer_satisfaction', 0)}%

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
