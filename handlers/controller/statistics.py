"""
Statistics Handler for Controller

This module handles statistics functionality for controllers.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime, timedelta
import json

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

async def get_statistics_data(period: str = 'daily'):
    """Mock statistics data"""
    return {
        'total_requests': 150,
        'completed_requests': 120,
        'pending_requests': 30,
        'average_completion_time': 2.5,
        'technician_performance': [
            {'name': 'Texnik 1', 'completed': 25, 'rating': 4.8},
            {'name': 'Texnik 2', 'completed': 30, 'rating': 4.6},
            {'name': 'Texnik 3', 'completed': 20, 'rating': 4.9}
        ],
        'request_types': {
            'connection': 60,
            'technical': 90
        },
        'priority_breakdown': {
            'urgent': 15,
            'high': 35,
            'medium': 70,
            'low': 30
        }
    }

class ControllerStatisticsStates(StatesGroup):
    viewing_statistics = State()
    selecting_period = State()
    generating_report = State()

def get_controller_statistics_router():
    """Get controller statistics router"""
    from utils.role_system import get_role_router
    router = get_role_router("controller")

    @router.message(F.text.in_(["📊 Statistika", "📊 Статистика"]))
    async def show_statistics_menu(message: Message, state: FSMContext):
        """Show statistics menu"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'controller':
                await message.answer("❌ Sizda bu bo'limga kirish huquqi yo'q.")
                return

            lang = user.get('language', 'uz')
            
            text = "📊 <b>Statistika bo'limi</b>\n\nQaysi davr uchun statistikani ko'rmoqchisiz?" if lang == 'uz' else "📊 <b>Раздел статистики</b>\n\nЗа какой период вы хотите посмотреть статистику?"
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📅 Bugungi" if lang == 'uz' else "📅 Сегодня",
                        callback_data="ctrl_stats_today"
                    ),
                    InlineKeyboardButton(
                        text="📆 Haftalik" if lang == 'uz' else "📆 Неделя",
                        callback_data="ctrl_stats_week"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📊 Oylik" if lang == 'uz' else "📊 Месяц",
                        callback_data="ctrl_stats_month"
                    ),
                    InlineKeyboardButton(
                        text="📈 Yillik" if lang == 'uz' else "📈 Год",
                        callback_data="ctrl_stats_year"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="👨‍🔧 Texniklar bo'yicha" if lang == 'uz' else "👨‍🔧 По техникам",
                        callback_data="ctrl_stats_technicians"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📋 Hisobot yuklab olish" if lang == 'uz' else "📋 Скачать отчет",
                        callback_data="ctrl_stats_download"
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
            await state.set_state(ControllerStatisticsStates.viewing_statistics)

        except Exception as e:
            print(f"Error in show_statistics_menu: {str(e)}")
            await message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data.startswith("ctrl_stats_"))
    async def handle_statistics_selection(callback: CallbackQuery, state: FSMContext):
        """Handle statistics period selection"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'controller':
                return

            lang = user.get('language', 'uz')
            period = callback.data.split("_")[-1]
            
            if period == "download":
                await callback.message.answer("📥 Hisobot tayyorlanmoqda..." if lang == 'uz' else "📥 Отчет готовится...")
                # Here you would generate and send the report file
                return
            
            if period == "technicians":
                # Show technician statistics
                stats = await get_statistics_data()
                text = "👨‍🔧 <b>Texniklar statistikasi</b>\n\n" if lang == 'uz' else "👨‍🔧 <b>Статистика техников</b>\n\n"
                
                for tech in stats['technician_performance']:
                    text += f"• {tech['name']}: {tech['completed']} ta bajarilgan, ⭐ {tech['rating']}\n"
                
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(
                        text="◀️ Orqaga" if lang == 'uz' else "◀️ Назад",
                        callback_data="ctrl_stats_back"
                    )]
                ])
                
                await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                return
            
            # Get statistics for the selected period
            stats = await get_statistics_data(period)
            
            period_names = {
                'today': "Bugungi" if lang == 'uz' else "Сегодняшняя",
                'week': "Haftalik" if lang == 'uz' else "Недельная",
                'month': "Oylik" if lang == 'uz' else "Месячная",
                'year': "Yillik" if lang == 'uz' else "Годовая"
            }
            
            text = f"📊 <b>{period_names.get(period, period)} statistika</b>\n\n"
            text += f"📥 Jami arizalar: {stats['total_requests']}\n"
            text += f"✅ Bajarilgan: {stats['completed_requests']}\n"
            text += f"⏳ Kutilayotgan: {stats['pending_requests']}\n"
            text += f"⏱ O'rtacha bajarish vaqti: {stats['average_completion_time']} soat\n\n"
            
            text += "<b>Ariza turlari:</b>\n"
            text += f"🔌 Ulanish: {stats['request_types']['connection']}\n"
            text += f"🔧 Texnik: {stats['request_types']['technical']}\n\n"
            
            text += "<b>Muhimlik bo'yicha:</b>\n"
            text += f"🔴 Shoshilinch: {stats['priority_breakdown']['urgent']}\n"
            text += f"🟠 Yuqori: {stats['priority_breakdown']['high']}\n"
            text += f"🟡 O'rta: {stats['priority_breakdown']['medium']}\n"
            text += f"🟢 Past: {stats['priority_breakdown']['low']}\n"
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📥 Yuklab olish" if lang == 'uz' else "📥 Скачать",
                        callback_data=f"ctrl_download_stats_{period}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="◀️ Orqaga" if lang == 'uz' else "◀️ Назад",
                        callback_data="ctrl_stats_back"
                    )
                ]
            ])
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')

        except Exception as e:
            print(f"Error in handle_statistics_selection: {str(e)}")
            await callback.message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "ctrl_stats_back")
    async def back_to_statistics_menu(callback: CallbackQuery, state: FSMContext):
        """Go back to statistics menu"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'controller':
                return

            lang = user.get('language', 'uz')
            
            text = "📊 <b>Statistika bo'limi</b>\n\nQaysi davr uchun statistikani ko'rmoqchisiz?" if lang == 'uz' else "📊 <b>Раздел статистики</b>\n\nЗа какой период вы хотите посмотреть статистику?"
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📅 Bugungi" if lang == 'uz' else "📅 Сегодня",
                        callback_data="ctrl_stats_today"
                    ),
                    InlineKeyboardButton(
                        text="📆 Haftalik" if lang == 'uz' else "📆 Неделя",
                        callback_data="ctrl_stats_week"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📊 Oylik" if lang == 'uz' else "📊 Месяц",
                        callback_data="ctrl_stats_month"
                    ),
                    InlineKeyboardButton(
                        text="📈 Yillik" if lang == 'uz' else "📈 Год",
                        callback_data="ctrl_stats_year"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="👨‍🔧 Texniklar bo'yicha" if lang == 'uz' else "👨‍🔧 По техникам",
                        callback_data="ctrl_stats_technicians"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📋 Hisobot yuklab olish" if lang == 'uz' else "📋 Скачать отчет",
                        callback_data="ctrl_stats_download"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="◀️ Orqaga" if lang == 'uz' else "◀️ Назад",
                        callback_data="back_to_controller_main"
                    )
                ]
            ])

            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')

        except Exception as e:
            print(f"Error in back_to_statistics_menu: {str(e)}")
            await callback.message.answer("❌ Xatolik yuz berdi")

    return router