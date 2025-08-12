"""
Admin Main Menu Handler
Manages admin main menu and dashboard
"""

from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from typing import Optional, Dict, Any

# Keyboard imports
from keyboards.admin_buttons import get_admin_main_menu

# States imports
from states.admin_states import AdminMainMenuStates
from filters.role_filter import RoleFilter

def get_admin_main_menu_router():
    """Get admin main menu router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("admin")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["/start", "/admin"]))
    async def admin_start(message: Message, state: FSMContext):
        """Admin start"""
        data = await state.get_data()
        lang = data.get('lang', 'uz')

        # Store default lang if not set
        if 'lang' not in data:
            await state.update_data(lang=lang)

        if lang == 'ru':
            welcome_text = (
                f"🛠 <b>Панель администратора</b>\n\n"
                f"📊 <b>Состояние системы:</b>\n"
                f"👥 Всего пользователей: <b>1250</b>\n"
                f"📋 Заявок сегодня: <b>45</b>\n"
                f"✅ Выполнено сегодня: <b>32</b>\n"
                f"⏳ В ожидании: <b>13</b>\n"
                f"👨‍🔧 Активных техников: <b>8</b>\n\n"
                f"Выберите нужный раздел:"
            )
        else:
            welcome_text = (
                f"🛠 <b>Admin Panel</b>\n\n"
                f"📊 <b>Tizim holati:</b>\n"
                f"👥 Jami foydalanuvchilar: <b>1250</b>\n"
                f"📋 Bugungi zayavkalar: <b>45</b>\n"
                f"✅ Bugun bajarilgan: <b>32</b>\n"
                f"⏳ Kutilayotgan: <b>13</b>\n"
                f"👨‍🔧 Faol texniklar: <b>8</b>\n\n"
                f"Kerakli bo'limni tanlang:"
            )

        await message.answer(welcome_text, reply_markup=get_admin_main_menu(lang))
        await state.set_state(AdminMainMenuStates.main_menu)

    @router.message(F.text.in_(['🏠 Bosh sahifa', '🏠 Главная']))
    async def admin_home(message: Message, state: FSMContext):
        """Return to admin home"""
        await admin_start(message, state)
        
        await state.set_state(AdminMainMenuStates.main_menu)

    @router.message(F.text.in_(['◀️ Orqaga', '⬅️ Orqaga', '◀️ Назад', '⬅️ Назад']))
    async def admin_back_to_home(message: Message, state: FSMContext):
        """Back button -> main menu"""
        await admin_start(message, state)

    # Test handler without decorator
    @router.message(F.text == '/test_admin')
    async def test_admin(message: Message):
        """Test admin access without decorator"""
        await message.answer("✅ Admin access confirmed!")

    return router

async def show_admin_main_menu(message: Message):
    """Show admin main menu"""
    welcome_text = (f"🛠 <b>Admin Panel</b>\n\n" f"Kerakli bo'limni tanlang:")
    await message.answer(welcome_text, reply_markup=get_admin_main_menu('uz'))
