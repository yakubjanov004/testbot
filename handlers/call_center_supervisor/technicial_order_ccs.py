"""
Call Center Supervisor Technical Service Creation Handler

Creates a technical service order on behalf of a client, mirroring the
client flow: region → abonent type → abonent id → description → media →
address → geolocation → confirmation.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from filters.role_filter import RoleFilter

from keyboards.client_buttons import (
    zayavka_type_keyboard,
    geolocation_keyboard,
    confirmation_keyboard,
    media_attachment_keyboard,
    get_client_regions_keyboard,
)
from states.client_states import OrderStates


async def _get_user_by_telegram_id(telegram_id: int):
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'call_center_supervisor',
        'language': 'uz',
        'full_name': 'Supervisor',
        'phone_number': '+998900000000'
    }


def get_call_center_supervisor_technical_order_router():
    router = Router()

    role_filter = RoleFilter("call_center_supervisor")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🔧 Texnik xizmat yaratish", "🔧 Создать техническую заявку"]))
    async def start_technical_order(message: Message, state: FSMContext):
        user = await _get_user_by_telegram_id(message.from_user.id)
        if not user:
            await message.answer("Xatolik: foydalanuvchi topilmadi.")
            return
        await message.answer("Hududni tanlang:", reply_markup=get_client_regions_keyboard('uz'))
        await state.set_state(OrderStates.selecting_region)

    @router.callback_query(F.data.startswith("region_"), StateFilter(OrderStates.selecting_region))
    async def select_region(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        region = callback.data.split("_")[-1]
        await state.update_data(region=region)
        await callback.message.answer("Abonent turini tanlang:", reply_markup=zayavka_type_keyboard('uz'))
        await state.set_state(OrderStates.selecting_order_type)

    @router.callback_query(F.data.startswith("zayavka_type_"), StateFilter(OrderStates.selecting_order_type))
    async def select_abonent_type(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        abonent_type = callback.data.split("_")[-1]
        await state.update_data(abonent_type=abonent_type)
        await callback.message.answer("Abonent ID raqamini kiriting:")
        await state.set_state(OrderStates.waiting_for_contact)

    @router.message(StateFilter(OrderStates.waiting_for_contact))
    async def enter_abonent_id(message: Message, state: FSMContext):
        await state.update_data(abonent_id=message.text.strip())
        await message.answer("Muammo tavsifini kiriting:")
        await state.set_state(OrderStates.entering_description)

    @router.message(StateFilter(OrderStates.entering_description))
    async def enter_description(message: Message, state: FSMContext):
        await state.update_data(description=message.text.strip())
        await message.answer("Foto yoki video yuborasizmi?", reply_markup=media_attachment_keyboard('uz'))
        await state.set_state(OrderStates.asking_for_media)

    @router.callback_query(F.data.in_(["attach_media_yes", "attach_media_no"]), StateFilter(OrderStates.asking_for_media))
    async def ask_media(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        if callback.data == "attach_media_yes":
            await callback.message.answer("Foto yoki videoni yuboring:")
            await state.set_state(OrderStates.waiting_for_media)
        else:
            await _ask_for_address(callback, state)

    @router.message(StateFilter(OrderStates.waiting_for_media), F.photo | F.video)
    async def receive_media(message: Message, state: FSMContext):
        media_file_id = message.photo[-1].file_id if message.photo else message.video.file_id
        await state.update_data(media=media_file_id)
        await _ask_for_address(message, state)

    async def _ask_for_address(message_or_callback, state: FSMContext):
        if hasattr(message_or_callback, "message"):
            await message_or_callback.message.answer("Xizmat ko'rsatiladigan manzilni kiriting:")
        else:
            await message_or_callback.answer("Xizmat ko'rsatiladigan manzilni kiriting:")
        await state.set_state(OrderStates.entering_address)

    @router.message(StateFilter(OrderStates.entering_address))
    async def enter_address(message: Message, state: FSMContext):
        await state.update_data(address=message.text.strip())
        await message.answer("Geolokatsiya yuborasizmi?", reply_markup=geolocation_keyboard('uz'))
        await state.set_state(OrderStates.asking_for_location)

    @router.callback_query(F.data.in_(["send_location_yes", "send_location_no"]), StateFilter(OrderStates.asking_for_location))
    async def ask_geo(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        if callback.data == "send_location_yes":
            await callback.message.answer("Geolokatsiyani yuboring:")
            await state.set_state(OrderStates.waiting_for_location)
        else:
            await _show_confirmation(callback, state)

    @router.message(StateFilter(OrderStates.waiting_for_location), F.location)
    async def receive_geo(message: Message, state: FSMContext):
        await state.update_data(geo=message.location)
        await _show_confirmation(message, state)

    async def _show_confirmation(message_or_callback, state: FSMContext):
        data = await state.get_data()
        region = data.get('region', '-')
        abonent_type = data.get('abonent_type', '-')
        abonent_id = data.get('abonent_id', '-')
        description = data.get('description', '-')
        address = data.get('address', '-')
        geo = data.get('geo', None)
        media = data.get('media', None)
        text = (
            f"🏛️ <b>Hudud:</b> {region}\n"
            f"👤 <b>Abonent turi:</b> {abonent_type}\n"
            f"🆔 <b>Abonent ID:</b> {abonent_id}\n"
            f"📝 <b>Muammo tavsifi:</b> {description}\n"
            f"🏠 <b>Manzil:</b> {address}\n"
            f"📍 <b>Geolokatsiya:</b> {'✅ Yuborilgan' if geo else '❌ Yuborilmagan'}\n"
            f"🖼 <b>Media:</b> {'✅ Yuborilgan' if media else '❌ Yuborilmagan'}"
        )
        if hasattr(message_or_callback, "message"):
            await message_or_callback.message.answer(text, parse_mode='HTML', reply_markup=confirmation_keyboard('uz'))
        else:
            await message_or_callback.answer(text, parse_mode='HTML', reply_markup=confirmation_keyboard('uz'))
        await state.set_state(OrderStates.confirming_order)

    @router.callback_query(F.data == "confirm_zayavka", StateFilter(OrderStates.confirming_order))
    async def confirm_order(callback: CallbackQuery, state: FSMContext):
        try:
            try:
                await callback.message.edit_reply_markup(reply_markup=None)
            except Exception:
                pass
            await callback.answer()
            await callback.message.answer("✅ Texnik xizmat arizasi yaratildi! Operatorlar tez orada mijoz bilan bog'lanadi.")
            await state.clear()
        except Exception:
            await callback.answer("Xatolik yuz berdi")

    return router


