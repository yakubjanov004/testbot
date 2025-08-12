"""
Admin Generic Callbacks Handler
Handles small navigation callbacks shared across admin flows.
"""

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from states.admin_states import AdminMainMenuStates
from keyboards.admin_buttons import get_admin_main_menu, get_zayavka_main_keyboard
from filters.role_filter import RoleFilter


def get_admin_callbacks_router() -> Router:
    router = Router()

    role_filter = RoleFilter("admin")
    router.callback_query.filter(role_filter)

    @router.callback_query(F.data == "back_to_orders")
    async def back_to_orders(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        text = (
            "📊 Zayavkalar statistikasi\n\n"
            "Yangi: 15\nJarayonda: 8\nBajarilgan: 32\nBekor qilingan: 3\n\n"
            "Zayavkalar bo'yicha qidirish va filtrlash uchun quyidagi tugmalardan foydalaning:"
        )
        await callback.message.edit_text(text)
        await callback.message.answer(text, reply_markup=get_zayavka_main_keyboard('uz'))

    @router.callback_query(F.data == "admin_back_main")
    async def back_main(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(AdminMainMenuStates.main_menu)
        await callback.message.delete()
        await callback.message.answer("🏠 Bosh menyu", reply_markup=get_admin_main_menu('uz'))

    @router.callback_query(F.data == "users_list")
    async def users_list(callback: CallbackQuery):
        await callback.answer()
        await callback.message.edit_text("👥 Foydalanuvchilar ro'yxati hozircha to'liq ko'rsatilmaydi.")

    return router