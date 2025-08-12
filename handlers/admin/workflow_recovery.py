"""
Admin Workflow Recovery - minimal placeholder
"""

from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter
from states.admin_states import AdminWorkflowRecoveryStates


def get_admin_workflow_recovery_router() -> Router:
    router = Router()

    role_filter = RoleFilter("admin")
    router.message.filter(role_filter)

    @router.message(F.text.in_(["🧯 Ish jarayonini tiklash", "🧯 Восстановление процесса"]))
    async def show_recovery_menu(message: Message, state: FSMContext):
        await message.answer("Ish jarayonini tiklash bo'limi (yaqin kunlarda).")
        await state.set_state(AdminWorkflowRecoveryStates.workflow_recovery)

    return router