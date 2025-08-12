"""
Admin Workflow Recovery Handler
Provides simple recovery menu to resume or reset workflows.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.admin_states import AdminWorkflowRecoveryStates, AdminMainMenuStates
from keyboards.admin_buttons import get_admin_main_menu
from filters.role_filter import RoleFilter


def get_admin_workflow_recovery_router() -> Router:
    router = Router()

    role_filter = RoleFilter("admin")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🔄 Workflow tiklash", "🔄 Восстановление процесса"]))
    async def show_recovery_menu(message: Message, state: FSMContext):
        text = (
            "🔄 Workflow tiklash\n\n"
            "To'xtab qolgan jarayonlarni tiklash yoki\n"
            "yangi boshlashni tanlashingiz mumkin."
        ) if True else (
            "🔄 Восстановление процесса\n\n"
            "Вы можете восстановить прерванные процессы\n"
            "или начать заново."
        )
        await message.answer(
            text + "\n\n• ♻️ Oxirgi sessiyani tiklash — admin_resume_last\n• 🧹 Tozalash — admin_reset_state",
        )
        await state.set_state(AdminWorkflowRecoveryStates.recovery_menu)

    @router.callback_query(F.data == "admin_resume_last")
    async def resume_last(call: CallbackQuery, state: FSMContext):
        await call.answer()
        await call.message.edit_text("♻️ Oxirgi sessiya tiklandi.")
        await state.set_state(AdminMainMenuStates.main_menu)
        await call.message.answer("🏠 Bosh menyu", reply_markup=get_admin_main_menu("uz"))

    @router.callback_query(F.data == "admin_reset_state")
    async def reset_state(call: CallbackQuery, state: FSMContext):
        await call.answer()
        await state.clear()
        await call.message.edit_text("🧹 Holat tozalandi.")
        await call.message.answer("🏠 Bosh menyu", reply_markup=get_admin_main_menu("uz"))

    return router