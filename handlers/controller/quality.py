"""
Controller Quality Management - Simplified Implementation

This module handles controller quality management functionality.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.controllers_buttons import get_quality_keyboard, get_controller_back_keyboard
from typing import Dict, Any, List, Optional
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

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    return 'uz'

async def get_quality_metrics():
    """Mock get quality metrics"""
    return {
        'overall_quality_score': 4.2,
        'customer_satisfaction': 85,
        'response_time_score': 4.5,
        'resolution_rate': 92,
        'technician_ratings': 4.3,
        'total_reviews': 150,
        'positive_reviews': 128,
        'neutral_reviews': 15,
        'negative_reviews': 7
    }

async def get_quality_issues():
    """Mock get quality issues"""
    return [
        {
            'id': 1,
            'type': 'response_time',
            'severity': 'medium',
            'description': 'Javob vaqti sekin',
            'affected_applications': 5,
            'created_at': datetime.now(),
            'status': 'open'
        },
        {
            'id': 2,
            'type': 'technician_skill',
            'severity': 'low',
            'description': 'Texnik malakasi past',
            'affected_applications': 2,
            'created_at': datetime.now(),
            'status': 'resolved'
        },
        {
            'id': 3,
            'type': 'communication',
            'severity': 'high',
            'description': 'Mijoz bilan aloqa muammosi',
            'affected_applications': 8,
            'created_at': datetime.now(),
            'status': 'open'
        }
    ]

def get_quality_router():
    """Router for quality management functionality"""
    router = Router()

    @router.message(F.text.in_(["🏆 Sifat boshqaruvi", "🏆 Управление качеством"]))
    async def view_quality_management(message: Message, state: FSMContext):
        """Controller view quality management handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'controller':
                return
            
            lang = user.get('language', 'uz')
            
            # Get quality metrics
            metrics = await get_quality_metrics()
            
            quality_text = (
                "🏆 <b>Sifat boshqaruvi - To'liq ma'lumot</b>\n\n"
                "📊 <b>Asosiy ko'rsatkichlar:</b>\n"
                f"• Umumiy sifat balli: {metrics['overall_quality_score']}/5.0\n"
                f"• Mijoz mamnuniyati: {metrics['customer_satisfaction']}%\n"
                f"• Javob vaqti balli: {metrics['response_time_score']}/5.0\n"
                f"• Muammo hal qilish: {metrics['resolution_rate']}%\n"
                f"• Texniklar reytingi: {metrics['technician_ratings']}/5.0\n\n"
                f"📈 <b>Reytinglar:</b>\n"
                f"• Jami sharhlar: {metrics['total_reviews']}\n"
                f"• Ijobiy: {metrics['positive_reviews']}\n"
                f"• Neytral: {metrics['neutral_reviews']}\n"
                f"• Salbiy: {metrics['negative_reviews']}\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
                if lang == 'uz' else
                "🏆 <b>Управление качеством - Полная информация</b>\n\n"
                "📊 <b>Основные показатели:</b>\n"
                f"• Общий балл качества: {metrics['overall_quality_score']}/5.0\n"
                f"• Удовлетворенность клиентов: {metrics['customer_satisfaction']}%\n"
                f"• Балл времени ответа: {metrics['response_time_score']}/5.0\n"
                f"• Решение проблем: {metrics['resolution_rate']}%\n"
                f"• Рейтинг техников: {metrics['technician_ratings']}/5.0\n\n"
                f"📈 <b>Рейтинги:</b>\n"
                f"• Всего отзывов: {metrics['total_reviews']}\n"
                f"• Положительные: {metrics['positive_reviews']}\n"
                f"• Нейтральные: {metrics['neutral_reviews']}\n"
                f"• Отрицательные: {metrics['negative_reviews']}\n\n"
                "Выберите один из разделов ниже:"
            )
            
            sent_message = await message.answer(
                text=quality_text,
                reply_markup=get_quality_keyboard(lang),
                parse_mode='HTML'
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "view_quality_issues")
    async def view_quality_issues(callback: CallbackQuery, state: FSMContext):
        """View quality issues"""
        try:
            await callback.answer()
            
            # Get quality issues
            issues = await get_quality_issues()
            
            if not issues:
                no_issues_text = (
                    "✅ Sifat muammolari mavjud emas."
                    if callback.from_user.language_code == 'uz' else
                    "✅ Проблем с качеством нет."
                )
                
                await callback.message.edit_text(
                    text=no_issues_text,
                    reply_markup=get_controller_back_keyboard('uz')
                )
                return
            
            # Show first issue
            await show_quality_issue(callback, issues[0], issues, 0)
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    async def show_quality_issue(callback, issue, issues, index):
        """Show quality issue details with navigation"""
        try:
            # Format severity
            severity_emoji = {
                'low': '🟢',
                'medium': '🟡',
                'high': '🔴',
                'critical': '🔴'
            }.get(issue['severity'], '⚪')
            
            severity_text = {
                'low': 'Past',
                'medium': 'O\'rtacha',
                'high': 'Yuqori',
                'critical': 'Kritik'
            }.get(issue['severity'], 'Noma\'lum')
            
            # Format status
            status_emoji = {
                'open': '🔴',
                'in_progress': '🟡',
                'resolved': '🟢',
                'closed': '⚫'
            }.get(issue['status'], '⚪')
            
            status_text = {
                'open': 'Ochiq',
                'in_progress': 'Jarayonda',
                'resolved': 'Hal qilindi',
                'closed': 'Yopilgan'
            }.get(issue['status'], 'Noma\'lum')
            
            # Format date
            created_date = issue['created_at'].strftime('%d.%m.%Y %H:%M')
            
            # To'liq ma'lumot
            text = (
                f"🏆 <b>Sifat muammosi - To'liq ma'lumot</b>\n\n"
                f"🆔 <b>Muammo ID:</b> {issue['id']}\n"
                f"📋 <b>Turi:</b> {issue['type']}\n"
                f"{severity_emoji} <b>Jiddiylik:</b> {severity_text}\n"
                f"{status_emoji} <b>Holat:</b> {status_text}\n"
                f"📝 <b>Tavsif:</b> {issue['description']}\n"
                f"📊 <b>Ta'sir qilgan arizalar:</b> {issue['affected_applications']}\n"
                f"📅 <b>Yaratilgan:</b> {created_date}\n\n"
                f"📊 <b>Muammo #{index + 1} / {len(issues)}</b>"
            )
            
            # Create navigation keyboard
            keyboard = get_quality_issues_navigation_keyboard(index, len(issues))
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "quality_prev_issue")
    async def show_previous_quality_issue(callback: CallbackQuery, state: FSMContext):
        """Show previous quality issue"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_issue_index', 0)
            
            issues = await get_quality_issues()
            
            if current_index > 0:
                new_index = current_index - 1
                await state.update_data(current_issue_index=new_index)
                await show_quality_issue(callback, issues[new_index], issues, new_index)
            else:
                await callback.answer("Bu birinchi muammo")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "quality_next_issue")
    async def show_next_quality_issue(callback: CallbackQuery, state: FSMContext):
        """Show next quality issue"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_issue_index', 0)
            
            issues = await get_quality_issues()
            
            if current_index < len(issues) - 1:
                new_index = current_index + 1
                await state.update_data(current_issue_index=new_index)
                await show_quality_issue(callback, issues[new_index], issues, new_index)
            else:
                await callback.answer("Bu oxirgi muammo")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "view_quality_metrics")
    async def view_quality_metrics(callback: CallbackQuery, state: FSMContext):
        """View detailed quality metrics"""
        try:
            await callback.answer()
            
            # Get detailed quality metrics
            metrics = await get_quality_metrics()
            
            metrics_text = (
                "📊 <b>Batafsil sifat ko'rsatkichlari - To'liq ma'lumot</b>\n\n"
                "🏆 <b>Asosiy ballar:</b>\n"
                f"• Umumiy sifat: {metrics['overall_quality_score']}/5.0\n"
                f"• Javob vaqti: {metrics['response_time_score']}/5.0\n"
                f"• Texniklar: {metrics['technician_ratings']}/5.0\n\n"
                "📈 <b>Foizli ko'rsatkichlar:</b>\n"
                f"• Mijoz mamnuniyati: {metrics['customer_satisfaction']}%\n"
                f"• Muammo hal qilish: {metrics['resolution_rate']}%\n\n"
                "📊 <b>Reytinglar tahlili:</b>\n"
                f"• Jami sharhlar: {metrics['total_reviews']}\n"
                f"• Ijobiy: {metrics['positive_reviews']} ({(metrics['positive_reviews']/max(metrics['total_reviews'], 1)*100):.1f}%)\n"
                f"• Neytral: {metrics['neutral_reviews']} ({(metrics['neutral_reviews']/max(metrics['total_reviews'], 1)*100):.1f}%)\n"
                f"• Salbiy: {metrics['negative_reviews']} ({(metrics['negative_reviews']/max(metrics['total_reviews'], 1)*100):.1f}%)"
            )
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_quality")]
            ])
            
            await callback.message.edit_text(metrics_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "back_to_quality")
    async def back_to_quality(callback: CallbackQuery, state: FSMContext):
        """Back to quality menu"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            # Get quality metrics
            metrics = await get_quality_metrics()
            
            quality_text = (
                "🏆 <b>Sifat boshqaruvi - To'liq ma'lumot</b>\n\n"
                "📊 <b>Asosiy ko'rsatkichlar:</b>\n"
                f"• Umumiy sifat balli: {metrics['overall_quality_score']}/5.0\n"
                f"• Mijoz mamnuniyati: {metrics['customer_satisfaction']}%\n"
                f"• Javob vaqti balli: {metrics['response_time_score']}/5.0\n"
                f"• Muammo hal qilish: {metrics['resolution_rate']}%\n"
                f"• Texniklar reytingi: {metrics['technician_ratings']}/5.0\n\n"
                f"📈 <b>Reytinglar:</b>\n"
                f"• Jami sharhlar: {metrics['total_reviews']}\n"
                f"• Ijobiy: {metrics['positive_reviews']}\n"
                f"• Neytral: {metrics['neutral_reviews']}\n"
                f"• Salbiy: {metrics['negative_reviews']}\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
                if lang == 'uz' else
                "🏆 <b>Управление качеством - Полная информация</b>\n\n"
                "📊 <b>Основные показатели:</b>\n"
                f"• Общий балл качества: {metrics['overall_quality_score']}/5.0\n"
                f"• Удовлетворенность клиентов: {metrics['customer_satisfaction']}%\n"
                f"• Балл времени ответа: {metrics['response_time_score']}/5.0\n"
                f"• Решение проблем: {metrics['resolution_rate']}%\n"
                f"• Рейтинг техников: {metrics['technician_ratings']}/5.0\n\n"
                f"📈 <b>Рейтинги:</b>\n"
                f"• Всего отзывов: {metrics['total_reviews']}\n"
                f"• Положительные: {metrics['positive_reviews']}\n"
                f"• Нейтральные: {metrics['neutral_reviews']}\n"
                f"• Отрицательные: {metrics['negative_reviews']}\n\n"
                "Выберите один из разделов ниже:"
            )
            
            await callback.message.edit_text(
                text=quality_text,
                reply_markup=get_quality_keyboard(lang),
                parse_mode='HTML'
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    return router

def get_quality_issues_navigation_keyboard(current_index: int, total_issues: int):
    """Create navigation keyboard for quality issues"""
    keyboard = []
    
    # Navigation row
    nav_buttons = []
    
    # Previous button
    if current_index > 0:
        nav_buttons.append(InlineKeyboardButton(
            text="⬅️ Oldingi",
            callback_data="quality_prev_issue"
        ))
    
    # Next button
    if current_index < total_issues - 1:
        nav_buttons.append(InlineKeyboardButton(
            text="Keyingi ➡️",
            callback_data="quality_next_issue"
        ))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Back to menu
    keyboard.append([InlineKeyboardButton(text="🏠 Bosh sahifaquality", callback_data="back_to_main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_controller_quality_router():
    """Get controller quality router - alias for get_quality_router"""
    return get_quality_router()
