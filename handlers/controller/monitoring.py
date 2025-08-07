"""
Controller Monitoring - Simplified Implementation

This module handles controller monitoring functionality.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.controllers_buttons import get_monitoring_keyboard, get_controller_back_keyboard, get_monitoring_detailed_keyboard
from typing import Dict, Any, List, Optional
from datetime import datetime
from filters.role_filter import RoleFilter

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

async def get_monitoring_data():
    """Mock get monitoring data"""
    return {
        'total_applications': 150,
        'pending': 25,
        'in_progress': 45,
        'completed': 70,
        'cancelled': 10,
        'active_technicians': 8,
        'total_technicians': 12,
        'avg_response_time': '2.5 soat',
        'success_rate': '85%',
        'today_applications': 15,
        'today_completed': 12,
        'weekly_applications': 95,
        'weekly_completed': 82
    }

async def get_system_status():
    """Mock get system status"""
    return {
        'system_status': 'online',
        'database_status': 'healthy',
        'api_status': 'operational',
        'notification_status': 'active',
        'last_backup': '2024-01-15 23:00',
        'uptime': '99.8%'
    }

def get_monitoring_router():
    """Router for monitoring functionality"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("controller")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["📊 Monitoring", "📊 Мониторинг"]))
    async def view_monitoring(message: Message, state: FSMContext):
        """Controller view monitoring handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'controller':
                return
            
            lang = user.get('language', 'uz')
            
            # Get monitoring data
            monitoring_data = await get_monitoring_data()
            
            monitoring_text = (
                "📊 <b>Monitoring - To'liq ma'lumot</b>\n\n"
                "📈 <b>Umumiy statistika:</b>\n"
                f"• Jami arizalar: {monitoring_data['total_applications']}\n"
                f"• Kutilmoqda: {monitoring_data['pending']}\n"
                f"• Jarayonda: {monitoring_data['in_progress']}\n"
                f"• Bajarilgan: {monitoring_data['completed']}\n"
                f"• Bekor qilingan: {monitoring_data['cancelled']}\n\n"
                f"👨‍🔧 <b>Texniklar:</b> {monitoring_data['active_technicians']}/{monitoring_data['total_technicians']}\n"
                f"⏰ <b>O'rtacha javob vaqti:</b> {monitoring_data['avg_response_time']}\n"
                f"📈 <b>Muvaffaqiyat darajasi:</b> {monitoring_data['success_rate']}\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
                if lang == 'uz' else
                "📊 <b>Мониторинг - Полная информация</b>\n\n"
                "📈 <b>Общая статистика:</b>\n"
                f"• Всего заявок: {monitoring_data['total_applications']}\n"
                f"• Ожидающие: {monitoring_data['pending']}\n"
                f"• В процессе: {monitoring_data['in_progress']}\n"
                f"• Завершенные: {monitoring_data['completed']}\n"
                f"• Отмененные: {monitoring_data['cancelled']}\n\n"
                f"👨‍🔧 <b>Техники:</b> {monitoring_data['active_technicians']}/{monitoring_data['total_technicians']}\n"
                f"⏰ <b>Среднее время ответа:</b> {monitoring_data['avg_response_time']}\n"
                f"📈 <b>Уровень успеха:</b> {monitoring_data['success_rate']}\n\n"
                "Выберите один из разделов ниже:"
            )
            
            sent_message = await message.answer(
                text=monitoring_text,
                reply_markup=get_monitoring_keyboard(lang),
                parse_mode='HTML'
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "view_detailed_statistics")
    async def view_detailed_statistics(callback: CallbackQuery, state: FSMContext):
        """View detailed statistics"""
        try:
            await callback.answer()
            
            # Get detailed monitoring data
            monitoring_data = await get_monitoring_data()
            
            stats_text = (
                "📊 <b>Batafsil statistika - To'liq ma'lumot</b>\n\n"
                "📅 <b>Bugungi ko'rsatkichlar:</b>\n"
                f"• Yangi arizalar: {monitoring_data['today_applications']}\n"
                f"• Bajarilgan: {monitoring_data['today_completed']}\n"
                f"• Bajarish foizi: {(monitoring_data['today_completed']/max(monitoring_data['today_applications'], 1)*100):.1f}%\n\n"
                "📅 <b>Haftalik ko'rsatkichlar:</b>\n"
                f"• Jami arizalar: {monitoring_data['weekly_applications']}\n"
                f"• Bajarilgan: {monitoring_data['weekly_completed']}\n"
                f"• Bajarish foizi: {(monitoring_data['weekly_completed']/max(monitoring_data['weekly_applications'], 1)*100):.1f}%\n\n"
                "📈 <b>Umumiy ko'rsatkichlar:</b>\n"
                f"• Jami arizalar: {monitoring_data['total_applications']}\n"
                f"• Bajarilgan: {monitoring_data['completed']}\n"
                f"• Muvaffaqiyat darajasi: {monitoring_data['success_rate']}\n"
                f"• O'rtacha javob vaqti: {monitoring_data['avg_response_time']}"
            )
            
            keyboard = get_monitoring_detailed_keyboard(lang)
            
            await callback.message.edit_text(stats_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "view_system_status")
    async def view_system_status(callback: CallbackQuery, state: FSMContext):
        """View system status"""
        try:
            await callback.answer()
            
            # Get system status
            system_status = await get_system_status()
            
            # Format status emojis
            status_emoji = {
                'online': '🟢',
                'offline': '🔴',
                'maintenance': '🟡'
            }.get(system_status['system_status'], '⚪')
            
            db_status_emoji = {
                'healthy': '🟢',
                'warning': '🟡',
                'error': '🔴'
            }.get(system_status['database_status'], '⚪')
            
            api_status_emoji = {
                'operational': '🟢',
                'degraded': '🟡',
                'down': '🔴'
            }.get(system_status['api_status'], '⚪')
            
            notification_status_emoji = {
                'active': '🟢',
                'inactive': '🔴'
            }.get(system_status['notification_status'], '⚪')
            
            status_text = (
                "🔧 <b>Tizim holati - To'liq ma'lumot</b>\n\n"
                f"{status_emoji} <b>Asosiy tizim:</b> {system_status['system_status'].title()}\n"
                f"{db_status_emoji} <b>Ma'lumotlar bazasi:</b> {system_status['database_status'].title()}\n"
                f"{api_status_emoji} <b>API holati:</b> {system_status['api_status'].title()}\n"
                f"{notification_status_emoji} <b>Bildirishnomalar:</b> {system_status['notification_status'].title()}\n\n"
                f"💾 <b>Oxirgi zaxira:</b> {system_status['last_backup']}\n"
                f"⏰ <b>Ish vaqti:</b> {system_status['uptime']}\n\n"
                "📊 <b>Tizim holati:</b> Yaxshi"
            )
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_monitoring")]
            ])
            
            await callback.message.edit_text(status_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "back_to_monitoring")
    async def back_to_monitoring(callback: CallbackQuery, state: FSMContext):
        """Back to monitoring menu"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            # Get monitoring data
            monitoring_data = await get_monitoring_data()
            
            monitoring_text = (
                "📊 <b>Monitoring - To'liq ma'lumot</b>\n\n"
                "📈 <b>Umumiy statistika:</b>\n"
                f"• Jami arizalar: {monitoring_data['total_applications']}\n"
                f"• Kutilmoqda: {monitoring_data['pending']}\n"
                f"• Jarayonda: {monitoring_data['in_progress']}\n"
                f"• Bajarilgan: {monitoring_data['completed']}\n"
                f"• Bekor qilingan: {monitoring_data['cancelled']}\n\n"
                f"👨‍🔧 <b>Texniklar:</b> {monitoring_data['active_technicians']}/{monitoring_data['total_technicians']}\n"
                f"⏰ <b>O'rtacha javob vaqti:</b> {monitoring_data['avg_response_time']}\n"
                f"📈 <b>Muvaffaqiyat darajasi:</b> {monitoring_data['success_rate']}\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
                if lang == 'uz' else
                "📊 <b>Мониторинг - Полная информация</b>\n\n"
                "📈 <b>Общая статистика:</b>\n"
                f"• Всего заявок: {monitoring_data['total_applications']}\n"
                f"• Ожидающие: {monitoring_data['pending']}\n"
                f"• В процессе: {monitoring_data['in_progress']}\n"
                f"• Завершенные: {monitoring_data['completed']}\n"
                f"• Отмененные: {monitoring_data['cancelled']}\n\n"
                f"👨‍🔧 <b>Техники:</b> {monitoring_data['active_technicians']}/{monitoring_data['total_technicians']}\n"
                f"⏰ <b>Среднее время ответа:</b> {monitoring_data['avg_response_time']}\n"
                f"📈 <b>Уровень успеха:</b> {monitoring_data['success_rate']}\n\n"
                "Выберите один из разделов ниже:"
            )
            
            await callback.message.edit_text(
                text=monitoring_text,
                reply_markup=get_monitoring_keyboard(lang),
                parse_mode='HTML'
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    return router

def get_controller_monitoring_router():
    """Get controller monitoring router - alias for get_monitoring_router"""
    return get_monitoring_router()