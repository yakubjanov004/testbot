"""
Quality Handler for Controller

This module handles quality control and quality management functionality for controllers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime, timedelta
import json
from keyboards.controllers_buttons import get_quality_keyboard

# Mock database functions
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'controller',
        'language': 'uz',
        'full_name': 'Test Controller'
    }

async def get_quality_issues():
    """Mock quality issues data"""
    return [
        {
            'id': 1,
            'request_id': 'REQ001',
            'issue': 'Mijoz xizmat sifatidan norozi',
            'status': 'open',
            'created_at': datetime.now() - timedelta(hours=2)
        },
        {
            'id': 2,
            'request_id': 'REQ002',
            'issue': 'Texnik vaqtida kelmadi',
            'status': 'resolved',
            'created_at': datetime.now() - timedelta(days=1)
        }
    ]

async def get_quality_metrics():
    """Mock quality metrics data"""
    return {
        'average_rating': 4.5,
        'total_feedbacks': 150,
        'positive_feedbacks': 120,
        'negative_feedbacks': 30,
        'resolution_rate': 85,
        'response_time': 2.5
    }

# States
class ControllerQualityStates(StatesGroup):
    viewing_quality = State()
    viewing_issues = State()
    viewing_metrics = State()
    viewing_reports = State()

def get_controller_quality_router():
    """Get controller quality router"""
    from utils.role_system import get_role_router
    router = get_role_router("controller")

    @router.message(F.text.in_(["🎯 Sifat nazorati", "🎯 Контроль качества"]))
    async def show_quality_control_menu(message: Message, state: FSMContext):
        """Show quality control menu"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'controller':
                await message.answer("❌ Sizda bu bo'limga kirish huquqi yo'q.")
                return

            lang = user.get('language', 'uz')
            
            # Get quality metrics
            metrics = await get_quality_metrics()
            
            text = f"""🎯 <b>Sifat nazorati</b>

📊 <b>Asosiy ko'rsatkichlar:</b>
• O'rtacha baho: ⭐ {metrics['average_rating']}/5
• Jami fikrlar: {metrics['total_feedbacks']}
• Ijobiy fikrlar: ✅ {metrics['positive_feedbacks']}
• Salbiy fikrlar: ❌ {metrics['negative_feedbacks']}
• Muammolarni hal qilish: {metrics['resolution_rate']}%

Quyidagi bo'limlardan birini tanlang:""" if lang == 'uz' else f"""🎯 <b>Контроль качества</b>

📊 <b>Основные показатели:</b>
• Средняя оценка: ⭐ {metrics['average_rating']}/5
• Всего отзывов: {metrics['total_feedbacks']}
• Положительные отзывы: ✅ {metrics['positive_feedbacks']}
• Отрицательные отзывы: ❌ {metrics['negative_feedbacks']}
• Решение проблем: {metrics['resolution_rate']}%

Выберите один из разделов:"""
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="💬 Mijoz fikrlari" if lang == 'uz' else "💬 Отзывы клиентов",
                        callback_data="ctrl_qc_feedbacks"
                    ),
                    InlineKeyboardButton(
                        text="⚠️ Muammolar" if lang == 'uz' else "⚠️ Проблемы",
                        callback_data="ctrl_qc_issues"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📊 Ko'rsatkichlar" if lang == 'uz' else "📊 Показатели",
                        callback_data="ctrl_qc_metrics"
                    ),
                    InlineKeyboardButton(
                        text="📈 Tendensiyalar" if lang == 'uz' else "📈 Тенденции",
                        callback_data="ctrl_qc_trends"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📋 Hisobotlar" if lang == 'uz' else "📋 Отчеты",
                        callback_data="ctrl_qc_reports"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="◀️ Orqaga" if lang == 'uz' else "◀️ Назад",
                        callback_data="back_to_controller_main"
                    )
                ]
            ])

            await message.answer(text, reply_markup=keyboard, parse_mode='HTML')
            await state.set_state(ControllerQualityStates.viewing_quality)

        except Exception as e:
            print(f"Error in show_quality_control_menu: {str(e)}")
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text.in_(["🏆 Sifat boshqaruvi", "🏆 Управление качеством"]))
    async def show_quality_management_menu(message: Message, state: FSMContext):
        """Show quality management menu"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'controller':
                await message.answer("❌ Sizda bu bo'limga kirish huquqi yo'q.")
                return

            lang = user.get('language', 'uz')
            
            # Get quality data
            issues = await get_quality_issues()
            metrics = await get_quality_metrics()
            
            text = f"""🏆 <b>Sifat boshqaruvi - To'liq ma'lumot</b>

📊 <b>Umumiy ko'rsatkichlar:</b>
• Faol muammolar: {len([i for i in issues if i['status'] == 'open'])}
• Hal qilingan muammolar: {len([i for i in issues if i['status'] == 'resolved'])}
• O'rtacha baho: ⭐ {metrics['average_rating']}/5
• Muammolarni hal qilish tezligi: {metrics['resolution_rate']}%

Quyidagi amallardan birini tanlang:""" if lang == 'uz' else f"""🏆 <b>Управление качеством - Полная информация</b>

📊 <b>Общие показатели:</b>
• Активные проблемы: {len([i for i in issues if i['status'] == 'open'])}
• Решенные проблемы: {len([i for i in issues if i['status'] == 'resolved'])}
• Средняя оценка: ⭐ {metrics['average_rating']}/5
• Скорость решения проблем: {metrics['resolution_rate']}%

Выберите одно из действий:"""
            
            keyboard = get_quality_keyboard(lang)
            await message.answer(text, reply_markup=keyboard, parse_mode='HTML')
            await state.set_state(ControllerQualityStates.viewing_quality)

        except Exception as e:
            print(f"Error in show_quality_management_menu: {str(e)}")
            await message.answer("❌ Xatolik yuz berdi")

    return router
