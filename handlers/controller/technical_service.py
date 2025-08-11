"""
Controller Technical Service - Client-like Flow

Allows controller to create a technical service request on behalf of a client.
DB-less implementation, mirrors client flow and uses separate controller callbacks.
"""

import logging
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime

from filters.role_filter import RoleFilter
from states.controller_states import ControllerServiceOrderStates
from keyboards.controllers_buttons import (
    get_controller_regions_keyboard,
    controller_zayavka_type_keyboard,
    controller_media_attachment_keyboard,
    controller_geolocation_keyboard,
    controller_confirmation_keyboard,
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


def get_controller_technical_service_router():
    router = Router()

    # Role guard
    role_filter = RoleFilter("controller")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🔧 Texnik xizmat yaratish"]))
    async def new_service_request(message: Message, state: FSMContext):
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user.get('role') != 'controller':
                await message.answer("Sizda ruxsat yo'q.")
                return

            await message.answer(
                "Hududni tanlang:",
                reply_markup=get_controller_regions_keyboard('uz')
            )
            await state.set_state(ControllerServiceOrderStates.selecting_region)
        except Exception:
            await message.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")

    @router.callback_query(F.data.startswith("ctrl_region_"), StateFilter(ControllerServiceOrderStates.selecting_region))
    async def select_region(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            region = callback.data.replace("ctrl_region_", "")
            await state.update_data(region=region)

            await callback.message.answer(
                "Abonent turini tanlang:",
                reply_markup=controller_zayavka_type_keyboard('uz')
            )
            await state.set_state(ControllerServiceOrderStates.selecting_order_type)
        except Exception:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("ctrl_zayavka_type_"), StateFilter(ControllerServiceOrderStates.selecting_order_type))
    async def select_abonent_type(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            abonent_type = callback.data.replace("ctrl_zayavka_type_", "")
            await state.update_data(abonent_type=abonent_type)

            await callback.message.answer("Abonent ID raqamini kiriting:")
            await state.set_state(ControllerServiceOrderStates.waiting_for_abonent_id)
        except Exception:
            await callback.answer("Xatolik yuz berdi")

    @router.message(StateFilter(ControllerServiceOrderStates.waiting_for_abonent_id))
    async def get_abonent_id(message: Message, state: FSMContext):
        try:
            await state.update_data(abonent_id=message.text)
            await message.answer("Muammo tavsifini kiriting:")
            await state.set_state(ControllerServiceOrderStates.entering_description)
        except Exception:
            await message.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")

    @router.message(StateFilter(ControllerServiceOrderStates.entering_description))
    async def get_service_description(message: Message, state: FSMContext):
        try:
            await state.update_data(description=message.text)

            await message.answer(
                "Foto yoki video yuborasizmi?",
                reply_markup=controller_media_attachment_keyboard('uz')
            )
            await state.set_state(ControllerServiceOrderStates.asking_for_media)
        except Exception:
            await message.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")

    @router.callback_query(F.data.in_(["ctrl_attach_media_yes", "ctrl_attach_media_no"]), StateFilter(ControllerServiceOrderStates.asking_for_media))
    async def ask_for_media(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            if callback.data == "ctrl_attach_media_yes":
                await callback.message.answer("Foto yoki videoni yuboring:")
                await state.set_state(ControllerServiceOrderStates.waiting_for_media)
            else:
                await ask_for_address(callback, state)
        except Exception:
            await callback.answer("Xatolik yuz berdi")

    @router.message(StateFilter(ControllerServiceOrderStates.waiting_for_media), F.photo | F.video)
    async def process_media(message: Message, state: FSMContext):
        try:
            media_file_id = message.photo[-1].file_id if message.photo else message.video.file_id
            await state.update_data(media=media_file_id)
            await ask_for_address(message, state)
        except Exception:
            await message.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")

    async def ask_for_address(message_or_callback, state: FSMContext):
        try:
            if hasattr(message_or_callback, "message"):
                await message_or_callback.message.answer("Xizmat ko'rsatiladigan manzilni kiriting:")
            else:
                await message_or_callback.answer("Xizmat ko'rsatiladigan manzilni kiriting:")
            await state.set_state(ControllerServiceOrderStates.entering_address)
        except Exception:
            if hasattr(message_or_callback, "message"):
                await message_or_callback.message.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")
            else:
                await message_or_callback.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")

    @router.message(StateFilter(ControllerServiceOrderStates.entering_address))
    async def get_service_address(message: Message, state: FSMContext):
        try:
            await state.update_data(address=message.text)
            await message.answer(
                "Geolokatsiya yuborasizmi?",
                reply_markup=controller_geolocation_keyboard('uz')
            )
            await state.set_state(ControllerServiceOrderStates.asking_for_location)
        except Exception:
            await message.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")

    @router.callback_query(F.data.in_(["ctrl_send_location_yes", "ctrl_send_location_no"]), StateFilter(ControllerServiceOrderStates.asking_for_location))
    async def ask_for_geo(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            if callback.data == "ctrl_send_location_yes":
                await callback.message.answer("Geolokatsiyani yuboring:")
                await state.set_state(ControllerServiceOrderStates.waiting_for_location)
            else:
                await show_service_confirmation(callback, state)
        except Exception:
            await callback.answer("Xatolik yuz berdi")

    @router.message(StateFilter(ControllerServiceOrderStates.waiting_for_location), F.location)
    async def get_geo(message: Message, state: FSMContext):
        try:
            await state.update_data(geo=message.location)
            await show_service_confirmation(message, state)
        except Exception:
            await message.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")

    async def show_service_confirmation(message_or_callback, state: FSMContext):
        try:
            data = await state.get_data()
            region = data.get('region', '-')
            abonent_type = data.get('abonent_type', '-')
            abonent_id = data.get('abonent_id', '-')
            description = data.get('description', '-')
            address = data.get('address', '-')
            geo = data.get('geo')
            media = data.get('media')

            text = (
                f"🏛️ <b>Hudud:</b> {region}\n"
                f"👤 <b>Abonent turi:</b> {abonent_type}\n"
                f"🆔 <b>Abonent ID:</b> {abonent_id}\n"
                f"📝 <b>Muammo tavsifi:</b> {description}\n"
                f"🏠 <b>Manzil:</b> {address}\n"
                f"📍 <b>Geolokatsiya:</b> {'✅ Yuborilgan' if geo else '❌ Yuborilmagan'}\n"
                f"🖼 <b>Media:</b> {'✅ Yuborilgan' if media else '❌ Yuborilmagan'}"
            )

            if hasattr(message_or_callback, 'message'):
                await message_or_callback.message.answer(text, parse_mode='HTML', reply_markup=controller_confirmation_keyboard('uz'))
            else:
                await message_or_callback.answer(text, parse_mode='HTML', reply_markup=controller_confirmation_keyboard('uz'))
            await state.set_state(ControllerServiceOrderStates.confirming_order)
        except Exception:
            if hasattr(message_or_callback, 'message'):
                await message_or_callback.message.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")
            else:
                await message_or_callback.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")

    @router.callback_query(F.data == "ctrl_confirm_zayavka", StateFilter(ControllerServiceOrderStates.confirming_order))
    async def confirm_service_order(callback: CallbackQuery, state: FSMContext):
        try:
            try:
                await callback.message.edit_reply_markup(reply_markup=None)
            except Exception:
                pass
            await callback.answer()

            request_id = f"TX_CTRL_{callback.from_user.id}_{int(datetime.now().timestamp())}"
            success_msg = (
                "✅ Texnik xizmat arizasi controller tomonidan yaratildi!\n"
                f"Ariza ID: {request_id[:10]}\n"
                "Operatorlar tez orada mijoz bilan bog'lanadi."
            )
            await callback.message.answer(success_msg)
            await state.clear()
        except Exception:
            await callback.answer("Xatolik yuz berdi")

    return router
