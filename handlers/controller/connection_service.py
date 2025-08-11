"""
Controller Connection Service - Client-like Flow

Allows controller to create a connection request on behalf of a client.
DB-less implementation, mirrors client flow and uses separate controller callbacks.
"""

import logging
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime

from filters.role_filter import RoleFilter
from states.controller_states import ControllerConnectionOrderStates
from keyboards.controllers_buttons import (
    get_controller_regions_keyboard,
    controller_zayavka_type_keyboard,
    controller_geolocation_keyboard,
    controller_confirmation_keyboard,
    get_controller_tariff_selection_keyboard,
)

logger = logging.getLogger(__name__)

# Mock functions (no DB)
async def get_user_by_telegram_id(telegram_id: int):
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'controller',
        'language': 'uz',
        'full_name': 'Test Controller',
        'phone_number': '+998901234567'
    }


def get_controller_connection_service_router():
    router = Router()

    # Role guard
    role_filter = RoleFilter("controller")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🔌 Ulanish arizasi yaratish"]))
    async def start_connection_order(message: Message, state: FSMContext):
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user.get('role') != 'controller':
                await message.answer("Sizda ruxsat yo'q.")
                return

            await message.answer(
                "Hududni tanlang:",
                reply_markup=get_controller_regions_keyboard('uz')
            )
            await state.set_state(ControllerConnectionOrderStates.selecting_region)
        except Exception:
            await message.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")

    @router.callback_query(F.data.startswith("ctrl_region_"), StateFilter(ControllerConnectionOrderStates.selecting_region))
    async def select_region(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            region = callback.data.replace("ctrl_region_", "")
            await state.update_data(region=region)

            await callback.message.answer(
                "Ulanish turini tanlang:",
                reply_markup=controller_zayavka_type_keyboard('uz')
            )
            await state.set_state(ControllerConnectionOrderStates.selecting_connection_type)
        except Exception:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("ctrl_zayavka_type_"), StateFilter(ControllerConnectionOrderStates.selecting_connection_type))
    async def select_connection_type(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            connection_type = callback.data.replace("ctrl_zayavka_type_", "")
            await state.update_data(connection_type=connection_type)

            await callback.message.answer(
                "Tariflardan birini tanlang:",
                reply_markup=get_controller_tariff_selection_keyboard('uz')
            )
            await state.set_state(ControllerConnectionOrderStates.selecting_tariff)
        except Exception:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.in_(["ctrl_tariff_standard", "ctrl_tariff_new"]), StateFilter(ControllerConnectionOrderStates.selecting_tariff))
    async def select_tariff(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            tariff = "Standard" if callback.data == "ctrl_tariff_standard" else "Yangi"
            await state.update_data(selected_tariff=tariff)

            await callback.message.answer("Manzilingizni kiriting:")
            await state.set_state(ControllerConnectionOrderStates.entering_address)
        except Exception:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.message(StateFilter(ControllerConnectionOrderStates.entering_address))
    async def get_connection_address(message: Message, state: FSMContext):
        try:
            await state.update_data(address=message.text)

            await message.answer(
                "Geolokatsiya yuborasizmi?",
                reply_markup=controller_geolocation_keyboard('uz')
            )
            await state.set_state(ControllerConnectionOrderStates.asking_for_geo)
        except Exception:
            await message.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")

    @router.callback_query(F.data.in_(["ctrl_send_location_yes", "ctrl_send_location_no"]), StateFilter(ControllerConnectionOrderStates.asking_for_geo))
    async def ask_for_geo(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            if callback.data == "ctrl_send_location_yes":
                await callback.message.answer("Geolokatsiyani yuboring:")
                await state.set_state(ControllerConnectionOrderStates.waiting_for_geo)
            else:
                await show_connection_confirmation(callback, state, geo=None)
        except Exception:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.message(StateFilter(ControllerConnectionOrderStates.waiting_for_geo), F.location)
    async def get_geo(message: Message, state: FSMContext):
        try:
            await state.update_data(geo=message.location)
            await show_connection_confirmation(message, state, geo=message.location)
        except Exception:
            await message.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")

    async def show_connection_confirmation(message_or_callback, state: FSMContext, geo=None):
        data = await state.get_data()
        region = data.get('region', '-')
        connection_type = data.get('connection_type', '-')
        tariff = data.get('selected_tariff', '-')
        address = data.get('address', '-')

        text = (
            f"🏛️ <b>Hudud:</b> {region}\n"
            f"🔌 <b>Ulanish turi:</b> {connection_type}\n"
            f"💳 <b>Tarif:</b> {tariff}\n"
            f"🏠 <b>Manzil:</b> {address}\n"
            f"📍 <b>Geolokatsiya:</b> {'✅ Yuborilgan' if geo else '❌ Yuborilmagan'}"
        )

        if hasattr(message_or_callback, 'message'):
            await message_or_callback.message.answer(text, parse_mode='HTML', reply_markup=controller_confirmation_keyboard('uz'))
        else:
            await message_or_callback.answer(text, parse_mode='HTML', reply_markup=controller_confirmation_keyboard('uz'))
        await state.set_state(ControllerConnectionOrderStates.confirming_connection)

    @router.callback_query(F.data == "ctrl_confirm_zayavka", StateFilter(ControllerConnectionOrderStates.confirming_connection))
    async def confirm_connection_order(callback: CallbackQuery, state: FSMContext):
        try:
            try:
                await callback.message.edit_reply_markup(reply_markup=None)
            except Exception:
                pass
            await callback.answer()

            request_id = f"UL_CTRL_{callback.from_user.id}_{int(datetime.now().timestamp())}"
            success_msg = (
                "✅ Ulanish arizasi controller tomonidan yaratildi!\n"
                f"Ariza ID: {request_id[:10]}\n"
                "Menejerlar tez orada mijoz bilan bog'lanadi."
            )
            await callback.message.answer(success_msg)
            await state.clear()
        except Exception:
            await callback.answer("Xatolik yuz berdi")

    return router