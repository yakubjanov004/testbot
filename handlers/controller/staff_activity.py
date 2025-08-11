"""
Controller Staff Activity - Technicians Only
"""

from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter


def get_controller_staff_activity_router():
    router = Router()

    role_filter = RoleFilter("controller")
    router.message.filter(role_filter)

    @router.message(F.text == "👥 Xodimlar faoliyati")
    async def show_technicians_work(message: Message, state: FSMContext):
        try:
            # Mock technicians' current work summary
            technicians = [
                {"full_name": "Aziz Karimov", "active_orders": 3, "last_task": "Router sozlash", "minutes_on_task": 25},
                {"full_name": "Malika Yusupova", "active_orders": 1, "last_task": "Kabelni almashtirish", "minutes_on_task": 52},
                {"full_name": "Bekzod Toirov", "active_orders": 0, "last_task": "—", "minutes_on_task": 0},
            ]

            text = "👥 <b>Texniklar faoliyati</b>\n\n"
            for tech in technicians:
                text += (
                    f"👨‍🔧 {tech['full_name']} — Faol buyurtmalar: {tech['active_orders']}\n"
                    f"   So'nggi vazifa: {tech['last_task']} ({tech['minutes_on_task']} daqiqa)\n\n"
                )

            await message.answer(text, parse_mode='HTML')
        except Exception:
            await message.answer("Xatolik yuz berdi")

    return router