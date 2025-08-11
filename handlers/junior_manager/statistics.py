"""
Junior Manager Statistics - Simplified Implementation

This module handles junior manager statistics functionality.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter
from keyboards.junior_manager_buttons import (
    get_statistics_keyboard,
    get_detailed_statistics_keyboard
)
from typing import Dict, Any, List, Optional
from datetime import datetime

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'junior_manager',
        'language': 'uz',
        'full_name': 'Test Junior Manager',
        'phone_number': '+998901234567'
    }

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    return 'uz'

async def get_junior_manager_statistics(user_id: int):
    """Mock get junior manager statistics"""
    return {
        'total_applications': 45,
        'pending_applications': 8,
        'in_progress_applications': 12,
        'completed_applications': 25,
        'cancelled_applications': 2,
        'avg_processing_time': '2.5 kun',
        'success_rate': '92%',
        'monthly_stats': {
            'january': 15,
            'february': 18,
            'march': 22,
            'april': 20
        },
        'top_services': [
            {'service': 'Internet ulanish', 'count': 20},
            {'service': 'TV xizmat', 'count': 12},
            {'service': 'Texnik xizmat', 'count': 8},
            {'service': 'Call Center', 'count': 5}
        ]
    }

def get_junior_manager_statistics_router():
    """Router for junior manager statistics functionality"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("junior_manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["📊 Hisobotlar", "📊 Отчеты"]))
    async def view_statistics(message: Message, state: FSMContext):
        """Junior manager view statistics handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'junior_manager':
                return
            
            lang = user.get('language', 'uz')
            
            # Get junior manager statistics
            stats = await get_junior_manager_statistics(message.from_user.id)
            
            statistics_text = (
                "📊 <b>Junior Manager statistikasi - To'liq ma'lumot</b>\n\n"
                "📈 <b>Asosiy ko'rsatkichlar:</b>\n"
                f"• Jami arizalar: {stats['total_applications']}\n"
                f"• Kutilmoqda: {stats['pending_applications']}\n"
                f"• Jarayonda: {stats['in_progress_applications']}\n"
                f"• Bajarilgan: {stats['completed_applications']}\n"
                f"• Bekor qilingan: {stats['cancelled_applications']}\n\n"
                f"⏰ <b>O'rtacha ishlov berish vaqti:</b> {stats['avg_processing_time']}\n"
                f"📈 <b>Muvaffaqiyat darajasi:</b> {stats['success_rate']}\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
                if lang == 'uz' else
                "📊 <b>Статистика Junior Manager - Полная информация</b>\n\n"
                "📈 <b>Основные показатели:</b>\n"
                f"• Всего заявок: {stats['total_applications']}\n"
                f"• Ожидающие: {stats['pending_applications']}\n"
                f"• В процессе: {stats['in_progress_applications']}\n"
                f"• Завершенные: {stats['completed_applications']}\n"
                f"• Отмененные: {stats['cancelled_applications']}\n\n"
                f"⏰ <b>Среднее время обработки:</b> {stats['avg_processing_time']}\n"
                f"📈 <b>Уровень успеха:</b> {stats['success_rate']}\n\n"
                "Выберите один из разделов ниже:"
            )
            
            sent_message = await message.answer(
                text=statistics_text,
                reply_markup=get_statistics_keyboard(lang),
                parse_mode='HTML'
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "view_detailed_statistics")
    async def view_detailed_statistics(callback: CallbackQuery, state: FSMContext):
        """View detailed statistics"""
        try:
            await callback.answer()
            
            # Get detailed statistics
            stats = await get_junior_manager_statistics(callback.from_user.id)
            
            detailed_stats_text = (
                "📊 <b>Batafsil statistika - To'liq ma'lumot</b>\n\n"
                "📅 <b>Oylik ko'rsatkichlar:</b>\n"
                f"• Yanvar: {stats['monthly_stats']['january']} ariza\n"
                f"• Fevral: {stats['monthly_stats']['february']} ariza\n"
                f"• Mart: {stats['monthly_stats']['march']} ariza\n"
                f"• Aprel: {stats['monthly_stats']['april']} ariza\n\n"
                "🏆 <b>Eng ko'p so'raladigan xizmatlar:</b>\n"
            )
            
            # Add top services
            for i, service in enumerate(stats['top_services'], 1):
                detailed_stats_text += f"• {i}. {service['service']}: {service['count']} ta\n"
            
            detailed_stats_text += (
                f"\n📈 <b>Umumiy tahlil:</b>\n"
                f"• O'rtacha kunlik: {stats['total_applications'] // 30} ariza\n"
                f"• Eng faol oy: Mart ({stats['monthly_stats']['march']} ariza)\n"
                f"• Muvaffaqiyat darajasi: {stats['success_rate']}"
            )
            
            keyboard = get_detailed_statistics_keyboard(lang)
            
            await callback.message.edit_text(detailed_stats_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "back_to_statistics")
    async def back_to_statistics(callback: CallbackQuery, state: FSMContext):
        """Back to statistics menu"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            # Get statistics
            stats = await get_junior_manager_statistics(callback.from_user.id)
            
            statistics_text = (
                "📊 <b>Junior Manager statistikasi - To'liq ma'lumot</b>\n\n"
                "📈 <b>Asosiy ko'rsatkichlar:</b>\n"
                f"• Jami arizalar: {stats['total_applications']}\n"
                f"• Kutilmoqda: {stats['pending_applications']}\n"
                f"• Jarayonda: {stats['in_progress_applications']}\n"
                f"• Bajarilgan: {stats['completed_applications']}\n"
                f"• Bekor qilingan: {stats['cancelled_applications']}\n\n"
                f"⏰ <b>O'rtacha ishlov berish vaqti:</b> {stats['avg_processing_time']}\n"
                f"📈 <b>Muvaffaqiyat darajasi:</b> {stats['success_rate']}\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
                if lang == 'uz' else
                "📊 <b>Статистика Junior Manager - Полная информация</b>\n\n"
                "📈 <b>Основные показатели:</b>\n"
                f"• Всего заявок: {stats['total_applications']}\n"
                f"• Ожидающие: {stats['pending_applications']}\n"
                f"• В процессе: {stats['in_progress_applications']}\n"
                f"• Завершенные: {stats['completed_applications']}\n"
                f"• Отмененные: {stats['cancelled_applications']}\n\n"
                f"⏰ <b>Среднее время обработки:</b> {stats['avg_processing_time']}\n"
                f"📈 <b>Уровень успеха:</b> {stats['success_rate']}\n\n"
                "Выберите один из разделов ниже:"
            )
            
            await callback.message.edit_text(
                text=statistics_text,
                reply_markup=get_statistics_keyboard(lang),
                parse_mode='HTML'
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    return router