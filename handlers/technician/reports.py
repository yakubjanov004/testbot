from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from datetime import datetime

def get_reports_router():
    """Technician reports router - Simplified Implementation"""
    router = Router()

    @router.message(F.text == "📊 Hisobotlar")
    async def show_reports_menu(message: Message, state: FSMContext):
        """Show reports menu handler"""
        try:
            text = """
📊 <b>Hisobotlar</b>

📈 Kunlik hisobot
📊 Haftalik hisobot
📋 Oylik hisobot
📋 Ish natijalari

Kerakli hisobotni tanlang:
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📈 Kunlik hisobot", callback_data="tech_daily_report")],
                [InlineKeyboardButton(text="📊 Haftalik hisobot", callback_data="tech_weekly_report")],
                [InlineKeyboardButton(text="📋 Oylik hisobot", callback_data="tech_monthly_report")],
                [InlineKeyboardButton(text="📋 Ish natijalari", callback_data="tech_performance_report")]
            ])
            
            await message.answer(text.strip(), parse_mode='HTML', reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "tech_daily_report")
    async def daily_report(callback: CallbackQuery):
        """Daily report handler"""
        try:
            # Mock stats data
            stats = {
                'total': 15,
                'completed': 12,
                'in_progress': 2,
                'new': 1,
                'completion_rate': 80,
                'avg_time': 2.5
            }
            
            text = f"""
📈 <b>Kunlik hisobot</b>
📅 {datetime.now().strftime('%d.%m.%Y')}

📊 <b>Statistika:</b>
• Jami vazifalar: {stats.get('total', 0)}
• Bajarilgan: {stats.get('completed', 0)}
• Jarayonda: {stats.get('in_progress', 0)}
• Yangi: {stats.get('new', 0)}

📈 <b>Samaradorlik:</b>
• Bajarish foizi: {stats.get('completion_rate', 0)}%
• O'rtacha vaqt: {stats.get('avg_time', 0)} soat
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="tech_back_to_reports")]
            ])
            
            await callback.message.edit_text(text.strip(), reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "tech_weekly_report")
    async def weekly_report(callback: CallbackQuery):
        """Weekly report handler"""
        try:
            # Mock stats data
            stats = {
                'total': 85,
                'completed': 72,
                'in_progress': 8,
                'new': 5,
                'completion_rate': 85,
                'avg_time': 2.3
            }
            
            text = f"""
📊 <b>Haftalik hisobot</b>
📅 {datetime.now().strftime('%d.%m.%Y')}

📊 <b>Statistika:</b>
• Jami vazifalar: {stats.get('total', 0)}
• Bajarilgan: {stats.get('completed', 0)}
• Jarayonda: {stats.get('in_progress', 0)}
• Yangi: {stats.get('new', 0)}

📈 <b>Samaradorlik:</b>
• Bajarish foizi: {stats.get('completion_rate', 0)}%
• O'rtacha vaqt: {stats.get('avg_time', 0)} soat
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="tech_back_to_reports")]
            ])
            
            await callback.message.edit_text(text.strip(), reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "tech_monthly_report")
    async def monthly_report(callback: CallbackQuery):
        """Monthly report handler"""
        try:
            # Mock stats data
            stats = {
                'total': 320,
                'completed': 285,
                'in_progress': 25,
                'new': 10,
                'completion_rate': 89,
                'avg_time': 2.1
            }
            
            text = f"""
📋 <b>Oylik hisobot</b>
📅 {datetime.now().strftime('%d.%m.%Y')}

📊 <b>Statistika:</b>
• Jami vazifalar: {stats.get('total', 0)}
• Bajarilgan: {stats.get('completed', 0)}
• Jarayonda: {stats.get('in_progress', 0)}
• Yangi: {stats.get('new', 0)}

📈 <b>Samaradorlik:</b>
• Bajarish foizi: {stats.get('completion_rate', 0)}%
• O'rtacha vaqt: {stats.get('avg_time', 0)} soat
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="tech_back_to_reports")]
            ])
            
            await callback.message.edit_text(text.strip(), reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "tech_performance_report")
    async def performance_report(callback: CallbackQuery):
        """Performance report handler"""
        try:
            # Mock performance data
            performance = {
                'total_orders': 150,
                'completed_orders': 135,
                'avg_completion_time': 2.5,
                'customer_satisfaction': 4.8,
                'quality_score': 95,
                'efficiency_rating': 92
            }
            
            text = f"""
📋 <b>Ish natijalari</b>
📅 {datetime.now().strftime('%d.%m.%Y')}

📊 <b>Umumiy ko'rsatkichlar:</b>
• Jami buyurtmalar: {performance.get('total_orders', 0)}
• Bajarilgan: {performance.get('completed_orders', 0)}
• O'rtacha vaqt: {performance.get('avg_completion_time', 0)} soat

📈 <b>Baholash:</b>
• Mijozlar mamnuniyati: {performance.get('customer_satisfaction', 0)}/5
• Sifat ko'rsatkichi: {performance.get('quality_score', 0)}%
• Samaradorlik: {performance.get('efficiency_rating', 0)}%
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="tech_back_to_reports")]
            ])
            
            await callback.message.edit_text(text.strip(), reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "tech_back_to_reports")
    async def back_to_reports(callback: CallbackQuery):
        """Back to reports handler"""
        try:
            text = """
📊 <b>Hisobotlar</b>

📈 Kunlik hisobot
📊 Haftalik hisobot
📋 Oylik hisobot
📋 Ish natijalari

Kerakli hisobotni tanlang:
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📈 Kunlik hisobot", callback_data="tech_daily_report")],
                [InlineKeyboardButton(text="📊 Haftalik hisobot", callback_data="tech_weekly_report")],
                [InlineKeyboardButton(text="📋 Oylik hisobot", callback_data="tech_monthly_report")],
                [InlineKeyboardButton(text="📋 Ish natijalari", callback_data="tech_performance_report")]
            ])
            
            await callback.message.edit_text(text.strip(), parse_mode='HTML', reply_markup=keyboard)
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router
