"""
Call Center Main Menu Handler - Simplified Implementation
Manages call center main menu and dashboard
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from states.call_center import CallCenterMainMenuStates

def get_call_center_main_menu_router():
    """Get call center main menu router - Simplified Implementation"""
    router = Router()

    @router.message(F.text.in_(["/start", "/callcenter", "📞 Call Center", " Колл-центр"]))
    async def call_center_start(message: Message, state: FSMContext):
        """Call center start"""
        try:
            await state.set_state(CallCenterMainMenuStates.main_menu)
            
            # Mock dashboard stats
            stats = {
                'calls_today': 45,
                'orders_today': 23,
                'pending_callbacks': 8,
                'active_chats': 12,
                'conversion_rate': 78
            }
            
            welcome_text = f"""
📞 <b>Call Center Panel</b>

📊 <b>Bugungi holat:</b>
📞 Bugungi qo'ng'iroqlar: <b>{stats.get('calls_today', 0)}</b>
📋 Bugungi buyurtmalar: <b>{stats.get('orders_today', 0)}</b>
⏳ Kutilayotgan: <b>{stats.get('pending_callbacks', 0)}</b>
💬 Faol chatlar: <b>{stats.get('active_chats', 0)}</b>
🎯 Konversiya: <b>{stats.get('conversion_rate', 0)}%</b>
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📞 Qo'ng'iroqlar", callback_data="call_center_calls")],
                [InlineKeyboardButton(text="📋 Buyurtmalar", callback_data="call_center_orders")],
                [InlineKeyboardButton(text="🔍 Mijoz qidirish", callback_data="call_center_search")],
                [InlineKeyboardButton(text="💬 Chat sessiyalari", callback_data="call_center_chats")],
                [InlineKeyboardButton(text="📊 Statistika", callback_data="call_center_stats")],
                [InlineKeyboardButton(text="🌐 Tilni o'zgartirish", callback_data="call_center_language")]
            ])
            
            await message.answer(welcome_text.strip(), parse_mode='HTML', reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text.in_(['🏠 Bosh sahifa', '🏠 Главная']))
    async def call_center_home(message: Message, state: FSMContext):
        """Call center home"""
        try:
            await state.set_state(CallCenterMainMenuStates.main_menu)
            
            # Mock dashboard stats
            stats = {
                'calls_today': 45,
                'orders_today': 23,
                'pending_callbacks': 8,
                'active_chats': 12,
                'conversion_rate': 78
            }
            
            welcome_text = f"""
📞 <b>Call Center Panel</b>

📊 <b>Bugungi holat:</b>
📞 Bugungi qo'ng'iroqlar: <b>{stats.get('calls_today', 0)}</b>
📋 Bugungi buyurtmalar: <b>{stats.get('orders_today', 0)}</b>
⏳ Kutilayotgan: <b>{stats.get('pending_callbacks', 0)}</b>
💬 Faol chatlar: <b>{stats.get('active_chats', 0)}</b>
🎯 Konversiya: <b>{stats.get('conversion_rate', 0)}%</b>
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📞 Qo'ng'iroqlar", callback_data="call_center_calls")],
                [InlineKeyboardButton(text="📋 Buyurtmalar", callback_data="call_center_orders")],
                [InlineKeyboardButton(text="🔍 Mijoz qidirish", callback_data="call_center_search")],
                [InlineKeyboardButton(text="💬 Chat sessiyalari", callback_data="call_center_chats")],
                [InlineKeyboardButton(text="📊 Statistika", callback_data="call_center_stats")],
                [InlineKeyboardButton(text="🌐 Tilni o'zgartirish", callback_data="call_center_language")]
            ])
            
            await message.answer(welcome_text.strip(), parse_mode='HTML', reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text.in_(['ℹ️ Yordam', 'ℹ️ Помощь']))
    async def call_center_help(message: Message, state: FSMContext):
        """Call center help"""
        try:
            help_text = """
📞 <b>Call Center yordam</b>

🔧 <b>Asosiy funksiyalar:</b>
📞 Qo'ng'iroqlar boshqaruvi
📋 Buyurtmalar yaratish
🔍 Mijoz qidirish
💬 Chat sessiyalari
⭐️ Fikr-mulohaza
📊 Statistika

💡 Qo'shimcha ma'lumot uchun admin bilan bog'laning.
            """
            
            await message.answer(help_text.strip(), parse_mode='HTML')
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "call_center_main_menu")
    async def call_center_main_menu_callback(callback: CallbackQuery, state: FSMContext):
        """Return to call center main menu"""
        try:
            await state.set_state(CallCenterMainMenuStates.main_menu)
            
            # Mock dashboard stats
            stats = {
                'calls_today': 45,
                'orders_today': 23,
                'pending_callbacks': 8,
                'active_chats': 12,
                'conversion_rate': 78
            }
            
            welcome_text = f"""
📞 <b>Call Center Panel</b>

📊 <b>Bugungi holat:</b>
📞 Bugungi qo'ng'iroqlar: <b>{stats.get('calls_today', 0)}</b>
📋 Bugungi buyurtmalar: <b>{stats.get('orders_today', 0)}</b>
⏳ Kutilayotgan: <b>{stats.get('pending_callbacks', 0)}</b>
💬 Faol chatlar: <b>{stats.get('active_chats', 0)}</b>
🎯 Konversiya: <b>{stats.get('conversion_rate', 0)}%</b>
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📞 Qo'ng'iroqlar", callback_data="call_center_calls")],
                [InlineKeyboardButton(text="📋 Buyurtmalar", callback_data="call_center_orders")],
                [InlineKeyboardButton(text="🔍 Mijoz qidirish", callback_data="call_center_search")],
                [InlineKeyboardButton(text="💬 Chat sessiyalari", callback_data="call_center_chats")],
                [InlineKeyboardButton(text="📊 Statistika", callback_data="call_center_stats")],
                [InlineKeyboardButton(text="🌐 Tilni o'zgartirish", callback_data="call_center_language")]
            ])
            
            await callback.message.edit_text(welcome_text.strip(), parse_mode='HTML', reply_markup=keyboard)
            await callback.answer()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router