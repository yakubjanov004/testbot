from aiogram import F
from aiogram.types import Message, CallbackQuery
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

async def get_service_quality_metrics():
    """Mock service quality metrics"""
    return {
        'avg_rating': 4.2,
        'total_reviews': 150,
        'satisfaction_rate': 85,
        'rating_distribution': {
            5: 80,
            4: 45,
            3: 15,
            2: 8,
            1: 2
        }
    }

async def get_unresolved_issues():
    """Mock unresolved issues"""
    return [
        {
            'id': 1,
            'client_name': 'Client 1',
            'description': 'Problem with order 1',
            'days_pending': 3
        },
        {
            'id': 2,
            'client_name': 'Client 2',
            'description': 'Problem with order 2',
            'days_pending': 5
        }
    ]

async def get_recent_feedback(days: int = 7):
    """Mock recent feedback"""
    return [
        {
            'id': 1,
            'client_name': 'Client 1',
            'rating': 5,
            'comment': 'Ajoyib xizmat!',
            'created_at': '2024-01-15 10:30:00'
        },
        {
            'id': 2,
            'client_name': 'Client 2',
            'rating': 4,
            'comment': 'Yaxshi ishlagan',
            'created_at': '2024-01-14 15:20:00'
        },
        {
            'id': 3,
            'client_name': 'Client 3',
            'rating': 3,
            'comment': 'O\'rtacha',
            'created_at': '2024-01-13 09:15:00'
        }
    ]

async def get_quality_trends():
    """Mock quality trends"""
    return [
        {
            'period': 'Hafta 1',
            'avg_rating': 4.1,
            'change': 0.2,
            'review_count': 25
        },
        {
            'period': 'Hafta 2',
            'avg_rating': 4.3,
            'change': 0.1,
            'review_count': 30
        },
        {
            'period': 'Hafta 3',
            'avg_rating': 4.2,
            'change': -0.1,
            'review_count': 28
        }
    ]

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

# Mock keyboards
def quality_control_menu(lang: str):
    """Mock quality control menu keyboard"""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💬 Mijoz fikrlari", callback_data="customer_feedback"),
            InlineKeyboardButton(text="⚠️ Muammoli holatlar", callback_data="unresolved_issues")
        ],
        [
            InlineKeyboardButton(text="📊 Sifat baholash", callback_data="quality_assessment"),
            InlineKeyboardButton(text="📈 Sifat tendensiyalari", callback_data="quality_trends")
        ],
        [
            InlineKeyboardButton(text="📋 Sifat hisoboti", callback_data="quality_report")
        ],
        [
            InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_controllers")
        ]
    ])

def back_to_controllers_menu():
    """Mock back to controllers menu keyboard"""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_controllers")]
    ])

# Mock states
class ControllerQualityStates:
    quality_control = "quality_control"
    viewing_feedback = "viewing_feedback"
    viewing_issues = "viewing_issues"

def get_controller_quality_router():
    """Get controller quality router"""
    from utils.role_system import get_role_router
    router = get_role_router("controller")

    @router.message(F.text.in_(["🎯 Sifat nazorati"]))
    async def quality_control_menu_handler(message: Message, state: FSMContext):
        """Sifat nazorati menyusi"""
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
            await state.set_state(ControllerQualityStates.quality_control)
            
            # Sifat ko'rsatkichlarini olish
            quality_metrics = await get_service_quality_metrics()
            
            text = f"""🎯 <b>Sifat nazorati</b>

⭐ <b>Xizmat sifati ko'rsatkichlari:</b>
• O'rtacha baho: {quality_metrics.get('avg_rating') or 0:.1f}/5.0
• Jami sharhlar: {quality_metrics.get('total_reviews', 0)}
• Mijoz qoniqishi: {quality_metrics.get('satisfaction_rate', 0)}%

Kerakli bo'limni tanlang:"""
            
            await send_and_track(
                message.answer,
                text,
                user_id,
                reply_markup=quality_control_menu(lang),
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in quality_control_menu_handler: {e}")
            error_text = "Xatolik yuz berdi"
            await send_and_track(
                message.answer,
                error_text,
                user_id
            )

    @router.message(F.text.in_(["💬 Mijoz fikrlari"]))
    async def customer_feedback_view(message: Message, state: FSMContext):
        """Mijoz fikrlarini ko'rish"""
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
            feedback_list = await get_recent_feedback(days=7)
            
            text = "💬 <b>So'nggi mijoz fikrlari (7 kun):</b>\n\n"
            
            if feedback_list:
                for feedback in feedback_list[:10]:
                    stars = "⭐" * feedback['rating']
                    client_name = feedback.get('client_name', 'Noma\'lum')
                    comment = feedback.get('comment', '')
                    created_date = feedback.get('created_at', '')
                    
                    text += f"{stars} <b>{client_name}</b>\n"
                    if comment:
                        comment_preview = comment[:80] + "..." if len(comment) > 80 else comment
                        text += f"💭 {comment_preview}\n"
                    text += f"📅 {created_date}\n\n"
            else:
                no_feedback_text = "So'nggi fikrlar topilmadi"
                text += no_feedback_text
            
            await send_and_track(
                message.answer,
                text,
                user_id,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in customer_feedback_view: {e}")
            error_text = "Xatolik yuz berdi"
            await send_and_track(
                message.answer,
                error_text,
                user_id
            )

    @router.message(F.text.in_(["⚠️ Muammoli holatlar"]))
    async def unresolved_issues_view(message: Message, state: FSMContext):
        """Muammoli holatlarni ko'rish"""
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
            issues = await get_unresolved_issues()
            
            text = "⚠️ <b>Hal etilmagan muammolar:</b>\n\n"
            
            if issues:
                for issue in issues[:10]:
                    order_id = issue.get('id', 'N/A')
                    client_name = issue.get('client_name', 'Noma\'lum')
                    description = issue.get('description', '')
                    days_pending = issue.get('days_pending', 0)
                    
                    urgency_icon = "🔴" if days_pending > 5 else "🟡" if days_pending > 2 else "🟢"
                    
                    text += f"{urgency_icon} <b>#{order_id}</b> - {client_name}\n"
                    if description:
                        desc_preview = description[:60] + "..." if len(description) > 60 else description
                        text += f"📝 {desc_preview}\n"
                    
                    pending_text = "kun kutmoqda"
                    text += f"⏱️ {days_pending} {pending_text}\n\n"
            else:
                no_issues_text = "Hal etilmagan muammolar yo'q"
                text += no_issues_text
            
            await send_and_track(
                message.answer,
                text,
                user_id,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in unresolved_issues_view: {e}")
            error_text = "Xatolik yuz berdi"
            await send_and_track(
                message.answer,
                error_text,
                user_id
            )

    @router.message(F.text.in_(["📊 Sifat baholash"]))
    async def service_quality_assessment(message: Message, state: FSMContext):
        """Xizmat sifatini baholash"""
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
            quality_metrics = await get_service_quality_metrics()
            
            text = f"""📊 <b>Xizmat sifatini baholash</b>

⭐ <b>Umumiy ko'rsatkichlar:</b>
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
            
            # Tavsiyalar
            recommendations_text = "\n\n💡 <b>Tavsiyalar:</b>"
            text += recommendations_text
            
            avg_rating = float(quality_metrics.get('avg_rating') or 0)
            if avg_rating < 3.0:
                rec_text = "\n• Xizmat sifatini yaxshilash zarur"
                text += rec_text
            elif avg_rating < 4.0:
                rec_text = "\n• Yaxshi natija, lekin yaxshilash mumkin"
                text += rec_text
            else:
                rec_text = "\n• A'lo xizmat sifati saqlanmoqda"
                text += rec_text
            
            await send_and_track(
                message.answer,
                text,
                user_id,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in service_quality_assessment: {e}")
            error_text = "Xatolik yuz berdi"
            await send_and_track(
                message.answer,
                error_text,
                user_id
            )

    @router.message(F.text.in_(["📈 Sifat tendensiyalari"]))
    async def quality_trends_view(message: Message, state: FSMContext):
        """Sifat tendensiyalarini ko'rish"""
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
            trends = await get_quality_trends()
            
            text = "📈 <b>Sifat tendensiyalari:</b>\n\n"
            
            if trends:
                for period in trends[:8]:  # So'nggi 8 hafta
                    period_name = period.get('period', '')
                    rating = float(period.get('avg_rating') or 0)
                    change = period.get('change', 0)
                    review_count = period.get('review_count', 0)
                    
                    trend_icon = "📈" if change > 0 else "📉" if change < 0 else "➡️"
                    
                    text += f"{trend_icon} <b>{period_name}</b>\n"
                    text += f"⭐ Baho: {rating:.1f}"
                    
                    if change != 0:
                        change_text = f" ({change:+.1f})"
                        text += change_text
                    
                    reviews_text = "sharh"
                    text += f"\n💬 {review_count} {reviews_text}\n\n"
            else:
                no_trends_text = "Tendensiya ma'lumotlari yo'q"
                text += no_trends_text
            
            await send_and_track(
                message.answer,
                text,
                user_id,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in quality_trends_view: {e}")
            error_text = "Xatolik yuz berdi"
            await send_and_track(
                message.answer,
                error_text,
                user_id
            )

    @router.message(F.text.in_(["📋 Sifat hisoboti"]))
    async def quality_report(message: Message, state: FSMContext):
        """Sifat hisoboti yaratish"""
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
            
            # Ma'lumotlarni yig'ish
            quality_metrics = await get_service_quality_metrics()
            recent_feedback = await get_recent_feedback(days=30)
            unresolved_issues = await get_unresolved_issues()
            
            text = f"""📋 <b>Sifat hisoboti</b>
📅 <b>Sana:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}

⭐ <b>Umumiy ko'rsatkichlar:</b>
• O'rtacha baho: {quality_metrics.get('avg_rating') or 0:.1f}/5.0
• Jami sharhlar: {quality_metrics.get('total_reviews', 0)}
• Mijoz qoniqishi: {quality_metrics.get('satisfaction_rate', 0)}%

📈 <b>So'nggi 30 kun faolligi:</b>
• Yangi fikrlar: {len(recent_feedback)}
• Hal etilmagan muammolar: {len(unresolved_issues)}

💡 <b>Tavsiyalar:</b>"""
            
            # Tavsiyalar
            avg_rating = float(quality_metrics.get('avg_rating') or 0)
            if avg_rating < 3.0:
                rec_text = "\n• Xizmat sifatini yaxshilash zarur"
                text += rec_text
            elif avg_rating < 4.0:
                rec_text = "\n• Yaxshi natija, lekin yaxshilash mumkin"
                text += rec_text
            else:
                rec_text = "\n• A'lo xizmat sifati saqlanmoqda"
                text += rec_text
            
            if len(unresolved_issues) > 5:
                urgent_text = "\n• Hal etilmagan muammolarga e'tibor bering"
                text += urgent_text
            
            await send_and_track(
                message.answer,
                text,
                user_id,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in quality_report: {e}")
            error_text = "Xatolik yuz berdi"
            await send_and_track(
                message.answer,
                error_text,
                user_id
            )

    return router
