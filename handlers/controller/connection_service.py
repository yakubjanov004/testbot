"""
Controller Connection Service - Client-like Flow with Client Search

Allows controller to create a connection request on behalf of a client.
DB-less implementation. First selects client via search, then mirrors client flow.
"""

import logging
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime

from filters.role_filter import RoleFilter
from states.controller_states import (
    ControllerConnectionOrderStates,
    ControllerApplicationStates,
    ControllerServiceOrderStates,
)
from keyboards.controllers_buttons import (
    get_controller_regions_keyboard,
    controller_zayavka_type_keyboard,
    controller_geolocation_keyboard,
    controller_confirmation_keyboard,
    get_controller_tariff_selection_keyboard,
    get_application_creator_keyboard,
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

# Mock search helpers
async def search_clients_by_phone(phone: str):
    return [
        {'id': 1, 'full_name': 'Ali Valiyev', 'phone': phone},
        {'id': 2, 'full_name': 'Vali Aliev', 'phone': phone},
    ]

async def search_clients_by_name(name: str):
    return [
        {'id': 3, 'full_name': name, 'phone': '+998901112233'}
    ]


def get_controller_connection_service_router():
    router = Router()

    # Role guard
    role_filter = RoleFilter("controller")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    # 1) Entry point: start with selecting search method
    @router.message(F.text.in_(["🔌 Ulanish arizasi yaratish"]))
    async def start_connection_order(message: Message, state: FSMContext):
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user.get('role') != 'controller':
                await message.answer("Sizda ruxsat yo'q.")
                return

            await state.update_data(current_flow='connection')
            await message.answer(
                "Mijozni qanday qidiramiz?",
                reply_markup=get_application_creator_keyboard('uz')
            )
            await state.set_state(ControllerApplicationStates.selecting_client_search_method)
        except Exception:
            await message.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")

    # 2) Search flow (shared)
    @router.callback_query(F.data == "ctrl_search_phone", StateFilter(ControllerApplicationStates.selecting_client_search_method))
    async def search_by_phone(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(ControllerApplicationStates.entering_phone)
        await callback.message.edit_text("📱 Telefon raqamini kiriting:\nMasalan: +998901234567")

    @router.callback_query(F.data == "ctrl_search_name", StateFilter(ControllerApplicationStates.selecting_client_search_method))
    async def search_by_name(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(ControllerApplicationStates.entering_name)
        await callback.message.edit_text("👤 Mijoz ismini kiriting:\nMasalan: Alisher Karimov")

    @router.callback_query(F.data == "ctrl_search_id", StateFilter(ControllerApplicationStates.selecting_client_search_method))
    async def search_by_id(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(ControllerApplicationStates.entering_client_id)
        await callback.message.edit_text("🆔 Mijoz ID sini kiriting:\nMasalan: 12345")

    @router.callback_query(F.data == "ctrl_search_new", StateFilter(ControllerApplicationStates.selecting_client_search_method))
    async def create_new_client(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(ControllerApplicationStates.entering_new_client_name)
        await callback.message.edit_text("➕ Yangi mijoz nomini kiriting:")

    @router.callback_query(F.data == "ctrl_cancel_creation")
    async def cancel_creation(callback: CallbackQuery, state: FSMContext):
        await state.clear()
        await callback.message.edit_text("❌ Zayavka yaratish bekor qilindi")
        await callback.answer()

    @router.message(StateFilter(ControllerApplicationStates.entering_phone))
    async def process_phone_search(message: Message, state: FSMContext):
        phone = message.text.strip()
        clients = await search_clients_by_phone(phone)
        await _show_clients_list(message, state, clients)

    @router.message(StateFilter(ControllerApplicationStates.entering_name))
    async def process_name_search(message: Message, state: FSMContext):
        name = message.text.strip()
        clients = await search_clients_by_name(name)
        await _show_clients_list(message, state, clients)

    @router.message(StateFilter(ControllerApplicationStates.entering_client_id))
    async def process_id_search(message: Message, state: FSMContext):
        client_id = message.text.strip()
        clients = [{'id': int(client_id) if client_id.isdigit() else 9999, 'full_name': f'Mijoz #{client_id}', 'phone': '+998900000000'}]
        await _show_clients_list(message, state, clients)

    @router.message(StateFilter(ControllerApplicationStates.entering_new_client_name))
    async def process_new_client(message: Message, state: FSMContext):
        full_name = message.text.strip()
        clients = [{'id': -1, 'full_name': full_name, 'phone': 'N/A'}]
        await _show_clients_list(message, state, clients)

    async def _show_clients_list(message: Message, state: FSMContext, clients):
        if not clients:
            await message.answer("Mijoz topilmadi. Qayta urinib ko'ring.")
            await state.set_state(ControllerApplicationStates.selecting_client_search_method)
            await message.answer("Qidirish usulini tanlang:", reply_markup=get_application_creator_keyboard('uz'))
            return
        await state.update_data(found_clients=clients)
        await state.set_state(ControllerApplicationStates.selecting_client)

        buttons = []
        for i, c in enumerate(clients[:5]):
            buttons.append([{"text": f"{c['full_name']} - {c.get('phone','N/A')}", "cb": f"ctrl_select_client_{i}"}])
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        ikb = InlineKeyboardMarkup(inline_keyboard=[
            *[ [InlineKeyboardButton(text=b[0]['text'], callback_data=b[0]['cb'])] for b in buttons ],
            [InlineKeyboardButton(text="🔍 Boshqa qidirish", callback_data="ctrl_search_again")],
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="ctrl_cancel_creation")],
        ])
        await message.answer("Mijozni tanlang:", reply_markup=ikb)

    @router.callback_query(lambda c: c.data.startswith("ctrl_select_client_"), StateFilter(ControllerApplicationStates.selecting_client))
    async def select_client(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        data = await state.get_data()
        clients = data.get('found_clients', [])
        idx = int(callback.data.split('_')[-1])
        if idx >= len(clients):
            await callback.answer("Xato", show_alert=True)
            return
        await state.update_data(selected_client=clients[idx])

        # Branch to next flow based on current_flow
        flow = (await state.get_data()).get('current_flow', 'connection')
        if flow == 'connection':
            await callback.message.edit_text("Hududni tanlang:")
            await callback.message.answer("Hududni tanlang:", reply_markup=get_controller_regions_keyboard('uz'))
            await state.set_state(ControllerConnectionOrderStates.selecting_region)
        else:
            await callback.message.edit_text("Hududni tanlang:")
            await callback.message.answer("Hududni tanlang:", reply_markup=get_controller_regions_keyboard('uz'))
            await state.set_state(ControllerServiceOrderStates.selecting_region)

    @router.callback_query(F.data == "ctrl_search_again")
    async def search_again(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(ControllerApplicationStates.selecting_client_search_method)
        await callback.message.edit_text("Qidirish usulini tanlang:")
        await callback.message.answer("Qidirish usulini tanlang:", reply_markup=get_application_creator_keyboard('uz'))

    # 3) Connection order flow (after client selected)
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
        selected_client = data.get('selected_client', {})
        region = data.get('region', '-')
        connection_type = data.get('connection_type', '-')
        tariff = data.get('selected_tariff', '-')
        address = data.get('address', '-')

        text = (
            f"👤 <b>Mijoz:</b> {selected_client.get('full_name','N/A')}\n"
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

    @router.callback_query(F.data == "ctrl_resend_zayavka", StateFilter(ControllerConnectionOrderStates.confirming_connection))
    async def resend_connection_summary(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            data = await state.get_data()
            await show_connection_confirmation(callback, state, geo=data.get('geo'))
        except Exception:
            await callback.answer("Xatolik yuz berdi")

    return router