"""
Call Center Supervisor Main Menu Handler

This module implements the main menu handler for Call Center Supervisor role,
including staff management, order oversight, and application creation functionality.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, Optional

# Keyboard imports
from keyboards.call_center_supervisor_buttons import (
    get_call_center_supervisor_main_menu, get_staff_actions_menu,
    get_order_management_menu, get_client_search_menu, get_order_action_menu,
    get_staff_assignment_menu, get_status_change_menu, get_quick_actions_menu,
    get_supervisor_dashboard_menu, get_advanced_staff_management_menu,
    get_advanced_order_management_menu, get_analytics_dashboard_keyboard,
    get_notification_management_keyboard, get_supervisor_settings_keyboard
)

# States imports
from states.call_center_supervisor_states import (
    CallCenterSupervisorStates, CallCenterSupervisorInboxStates, 
    CallCenterSupervisorOrdersStates, CallCenterSupervisorStatisticsStates
)

def get_call_center_supervisor_main_menu_router():
    """Get router for call center supervisor main menu handlers"""
    router = Router()

    @router.message(F.text.in_(["📞 Call Center Supervisor", "📞 Супервайзер колл-центра", "📞 Call Center Nazoratchi"]))
    async def call_center_supervisor_start(message: Message, state: FSMContext):
        """Call center supervisor main menu"""
        lang = 'uz'  # Default language
        
        await state.clear()
        
        welcome_text = "📞 Call Center Supervisor paneliga xush kelibsiz!"
        
        await message.answer(
            welcome_text,
            reply_markup=get_call_center_supervisor_main_menu(lang)
        )
        await state.set_state(CallCenterSupervisorStates.main_menu)

    @router.message(F.text.in_(["🏠 Bosh menyu", "🏠 Главное меню"]))
    async def call_center_supervisor_main_menu_handler(message: Message, state: FSMContext):
        """Handle call center supervisor main menu button"""
        lang = 'uz'  # Default language
        
        main_menu_text = "Bosh menyu"
        
        await message.answer(
            main_menu_text,
            reply_markup=get_call_center_supervisor_main_menu(lang)
        )
        if state is not None:
            await state.set_state(CallCenterSupervisorStates.main_menu)

    # Staff application creation handlers
    @router.message(F.text.in_(["🔌 Ulanish arizasi yaratish", "🔌 Создать заявку на подключение"]))
    async def call_center_supervisor_create_connection_application(message: Message, state: FSMContext):
        """Handle call center supervisor creating connection application"""
        lang = 'uz'  # Default language
        
        # Mock application creation start
        await state.update_data(
            creator_context={'role': 'call_center_supervisor', 'id': 123},
            application_type='connection_request'
        )
        
        prompt_text = (
            "🔌 Call Center Supervisor: Ulanish arizasi yaratish\n\n"
            "Mijoz bilan telefon orqali gaplashayotgan vaqtda ariza yaratish.\n\n"
            "Mijozni qanday qidirishni xohlaysiz?\n\n"
            "📱 Telefon raqami bo'yicha\n"
            "👤 Ism bo'yicha\n"
            "🆔 Mijoz ID bo'yicha\n"
            "➕ Yangi mijoz qo'shish"
        )
        
        await message.answer(prompt_text)

    @router.message(F.text.in_(["🔧 Texnik xizmat yaratish", "🔧 Создать техническую заявку"]))
    async def call_center_supervisor_create_technical_application(message: Message, state: FSMContext):
        """Handle call center supervisor creating technical application"""
        lang = 'uz'  # Default language
        
        # Mock application creation start
        await state.update_data(
            creator_context={'role': 'call_center_supervisor', 'id': 123},
            application_type='technical_service'
        )
        
        prompt_text = (
            "🔧 Call Center Supervisor: Texnik xizmat arizasi yaratish\n\n"
            "Mijoz bilan telefon orqali gaplashayotgan vaqtda texnik xizmat arizasi yaratish.\n\n"
            "Mijozni qanday qidirishni xohlaysiz?\n\n"
            "📱 Telefon raqami bo'yicha\n"
            "👤 Ism bo'yicha\n"
            "🆔 Mijoz ID bo'yicha\n"
            "➕ Yangi mijoz qo'shish"
        )
        
        await message.answer(prompt_text)

    # Staff management handlers
    @router.message(F.text.in_(["👥 Xodimlar boshqaruvi", "👥 Управление персоналом"]))
    async def call_center_supervisor_staff_management(message: Message, state: FSMContext):
        """Handle call center supervisor staff management"""
        lang = 'uz'  # Default language
        
        # Mock staff management menu
        staff_text = (
            "👥 <b>Xodimlar boshqaruvi</b>\n\n"
            "Xodimlar bilan ishlash uchun bo'limni tanlang:\n\n"
            "📋 Xodimlar ro'yxati\n"
            "📊 Samaradorlik baholash\n"
            "💬 Xabar yuborish\n"
            "📅 Uchrashuv belgilash\n"
            "🎓 O'qitish"
        )
        
        await message.answer(staff_text)

    @router.message(F.text.in_(["👥 Xodimlarni ko'rish", "👥 Просмотр персонала"]))
    async def handle_staff_list(message: Message, state: FSMContext):
        """Handle staff list view"""
        # Mock staff list
        staff_list = [
            {'id': 1, 'name': 'Aziz Karimov', 'role': 'Operator', 'status': 'Faol'},
            {'id': 2, 'name': 'Malika Yusupova', 'role': 'Operator', 'status': 'Faol'},
            {'id': 3, 'name': 'Bekzod Toirov', 'role': 'Operator', 'status': 'Dam olish'}
        ]
        
        text = "👥 <b>Xodimlar ro'yxati</b>\n\n"
        for staff in staff_list:
            text += f"👤 {staff['name']} - {staff['role']} ({staff['status']})\n"
        
        await message.answer(text)

    @router.message(F.text.in_(["📋 Vazifa berish", "📋 Назначить задачу"]))
    async def handle_assign_tasks(message: Message, state: FSMContext):
        """Handle task assignment"""
        text = "📋 <b>Vazifa berish</b>\n\nVazifa berish funksiyasi ishlayapti."
        await message.answer(text)

    @router.message(F.text.in_(["📊 Samaradorlik baholash", "📊 Оценка производительности"]))
    async def handle_performance_review(message: Message, state: FSMContext):
        """Handle performance review"""
        text = "📊 <b>Samaradorlik baholash</b>\n\nSamaradorlik baholash funksiyasi ishlayapti."
        await message.answer(text)

    @router.message(F.text.in_(["💬 Xabar yuborish", "💬 Отправить сообщение"]))
    async def handle_send_message(message: Message, state: FSMContext):
        """Handle sending messages"""
        text = "💬 <b>Xabar yuborish</b>\n\nXabar yuborish funksiyasi ishlayapti."
        await message.answer(text)

    @router.message(F.text.in_(["📅 Uchrashuv belgilash", "📅 Назначить встречу"]))
    async def handle_schedule_meeting(message: Message, state: FSMContext):
        """Handle scheduling meetings"""
        text = "📅 <b>Uchrashuv belgilash</b>\n\nUchrashuv belgilash funksiyasi ishlayapti."
        await message.answer(text)

    @router.message(F.text.in_(["🎓 O'qitish", "🎓 Обучение"]))
    async def handle_training(message: Message, state: FSMContext):
        """Handle training"""
        text = "🎓 <b>O'qitish</b>\n\nO'qitish funksiyasi ishlayapti."
        await message.answer(text)

    @router.message(F.text.in_(["⬅️ Orqaga", "⬅️ Назад"]))
    async def handle_back_staff_menu(message: Message, state: FSMContext):
        """Handle back to staff menu"""
        text = "🏠 Bosh sahifaga qaytdingiz"
        await message.answer(text)

    # Quick actions handlers
    @router.message(F.text.in_(["🆕 Yangi buyurtmalar", "🆕 Новые заказы"]))
    async def handle_new_orders_quick(message: Message, state: FSMContext):
        """Handle new orders quick view"""
        # Mock new orders
        new_orders = [
            {'id': 'ORD001', 'client': 'Ahmad Karimov', 'service': 'Internet', 'priority': 'Yuqori'},
            {'id': 'ORD002', 'client': 'Malika Yusupova', 'service': 'TV', 'priority': 'O\'rta'}
        ]
        
        text = "🆕 <b>Yangi buyurtmalar</b>\n\n"
        for order in new_orders:
            text += f"📋 {order['id']} - {order['client']} ({order['service']}) - {order['priority']}\n"
        
        await message.answer(text)

    @router.message(F.text.in_(["🚨 Shoshilinch vazifalar", "🚨 Срочные задачи"]))
    async def handle_urgent_tasks(message: Message, state: FSMContext):
        """Handle urgent tasks"""
        # Mock urgent tasks
        urgent_tasks = [
            {'id': 'TASK001', 'description': 'Internet uzulish', 'assigned_to': 'Aziz Karimov'},
            {'id': 'TASK002', 'description': 'TV signal yo\'q', 'assigned_to': 'Malika Yusupova'}
        ]
        
        text = "🚨 <b>Shoshilinch vazifalar</b>\n\n"
        for task in urgent_tasks:
            text += f"⚠️ {task['id']} - {task['description']} (Bajaruvchi: {task['assigned_to']})\n"
        
        await message.answer(text)

    @router.message(F.text.in_(["👥 Xodimlar holati", "👥 Статус персонала"]))
    async def handle_staff_status(message: Message, state: FSMContext):
        """Handle staff status"""
        # Mock staff status
        staff_status = [
            {'name': 'Aziz Karimov', 'status': 'Ishlayapti', 'orders': 5},
            {'name': 'Malika Yusupova', 'status': 'Dam olish', 'orders': 0},
            {'name': 'Bekzod Toirov', 'status': 'Ishlayapti', 'orders': 3}
        ]
        
        text = "👥 <b>Xodimlar holati</b>\n\n"
        for staff in staff_status:
            text += f"👤 {staff['name']} - {staff['status']} (Buyurtmalar: {staff['orders']})\n"
        
        await message.answer(text)

    @router.message(F.text.in_(["📊 Kunlik hisobot", "📊 Дневной отчет"]))
    async def handle_daily_report(message: Message, state: FSMContext):
        """Handle daily report"""
        # Mock daily report
        daily_stats = {
            'total_orders': 45,
            'completed_orders': 38,
            'pending_orders': 7,
            'staff_online': 8,
            'avg_response_time': '2.3 daqiqa'
        }
        
        text = (
            f"📊 <b>Kunlik hisobot</b>\n\n"
            f"📋 Jami buyurtmalar: {daily_stats['total_orders']}\n"
            f"✅ Bajarilgan: {daily_stats['completed_orders']}\n"
            f"⏳ Kutilayotgan: {daily_stats['pending_orders']}\n"
            f"👥 Faol xodimlar: {daily_stats['staff_online']}\n"
            f"⚡ O'rtacha javob vaqti: {daily_stats['avg_response_time']}"
        )
        
        await message.answer(text)

    @router.message(F.text.in_(["🔔 Bildirishnomalar", "🔔 Уведомления"]))
    async def handle_notifications(message: Message, state: FSMContext):
        """Handle notifications"""
        # Mock notifications
        notifications = [
            'Yangi buyurtma qabul qilindi',
            'Xodim ishga keldi',
            'Buyurtma bajarildi'
        ]
        
        text = "🔔 <b>Bildirishnomalar</b>\n\n"
        for notification in notifications:
            text += f"📢 {notification}\n"
        
        await message.answer(text)

    # Callback handlers for inline buttons
    @router.callback_query(F.data.startswith("supervisor_action_"))
    async def handle_supervisor_action(call: CallbackQuery, state: FSMContext):
        """Handle supervisor action callbacks"""
        await call.answer()
        
        action = call.data.split("_")[-1]
        
        if action == "staff_management":
            text = "👥 <b>Xodimlar boshqaruvi</b>\n\nXodimlar bilan ishlash bo'limi."
        elif action == "order_oversight":
            text = "📋 <b>Buyurtmalar nazorati</b>\n\nBuyurtmalar nazorati bo'limi."
        elif action == "analytics":
            text = "📊 <b>Analitika</b>\n\nAnalitika va hisobotlar bo'limi."
        else:
            text = "❌ Noto'g'ri amal."
        
        await call.message.edit_text(text)

    @router.callback_query(F.data.startswith("staff_action_"))
    async def handle_staff_action(call: CallbackQuery, state: FSMContext):
        """Handle staff action callbacks"""
        await call.answer()
        
        action = call.data.split("_")[-1]
        
        if action == "assign":
            text = "📋 <b>Vazifa berish</b>\n\nVazifa berish funksiyasi ishlayapti."
        elif action == "evaluate":
            text = "📊 <b>Baholash</b>\n\nXodim baholash funksiyasi ishlayapti."
        elif action == "message":
            text = "💬 <b>Xabar yuborish</b>\n\nXabar yuborish funksiyasi ishlayapti."
        else:
            text = "❌ Noto'g'ri amal."
        
        await call.message.edit_text(text)

    @router.callback_query(F.data.in_(["back", "orqaga", "назад"]))
    async def supervisor_back(call: CallbackQuery, state: FSMContext):
        """Go back to supervisor main menu"""
        await call.answer()
        
        text = "Call Center Supervisor paneliga xush kelibsiz!"
        await call.message.edit_text(text)
        await state.clear()

    return router