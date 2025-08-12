from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime

from filters.role_filter import RoleFilter
from states.call_center_states import (
    CallCenterClientSearchStates,
    CallCenterServiceOrderStates,
)
from keyboards.call_center_buttons import get_call_center_client_search_keyboard
from keyboards.controllers_buttons import (
    get_controller_regions_keyboard,
    controller_zayavka_type_keyboard,
    controller_media_attachment_keyboard,
    controller_geolocation_keyboard,
)

# Mock search helpers (no DB)
async def search_clients_by_phone(phone: str):
    return [
        {'id': 1, 'full_name': 'Ali Valiyev', 'phone': phone},
        {'id': 2, 'full_name': 'Vali Aliev', 'phone': phone},
    ]

async def search_clients_by_name(name: str):
    return [
        {'id': 3, 'full_name': name, 'phone': '+998901112233'}
    ]


def get_call_center_technical_service_router():
    router = Router()

    # Role guard
    role_filter = RoleFilter("call_center")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    # 1) Entry: show search method selector
    @router.message(F.text.in_(["🔧 Texnik xizmat yaratish", "🔧 Создать техническую заявку"]))
    async def new_service_request(message: Message, state: FSMContext):
        await state.update_data(current_flow='technical')
        await message.answer(
            "Mijozni qanday qidiramiz?",
            reply_markup=get_call_center_client_search_keyboard('uz')
        )
        await state.set_state(CallCenterClientSearchStates.selecting_client_search_method)

    # 2) Search flow (same as connection)
    @router.callback_query(F.data == "cc_client_search_phone", StateFilter(CallCenterClientSearchStates.selecting_client_search_method))
    async def search_by_phone(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(CallCenterClientSearchStates.entering_phone)
        await callback.message.edit_text("📱 Telefon raqamini kiriting:\nMasalan: +998901234567")

    @router.callback_query(F.data == "cc_client_search_name", StateFilter(CallCenterClientSearchStates.selecting_client_search_method))
    async def search_by_name(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(CallCenterClientSearchStates.entering_name)
        await callback.message.edit_text("👤 Mijoz ismini kiriting:\nMasalan: Alisher Karimov")

    @router.callback_query(F.data == "cc_client_search_id", StateFilter(CallCenterClientSearchStates.selecting_client_search_method))
    async def search_by_id(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(CallCenterClientSearchStates.entering_client_id)
        await callback.message.edit_text("🆔 Mijoz ID sini kiriting:\nMasalan: 12345")

    @router.callback_query(F.data == "cc_client_search_new", StateFilter(CallCenterClientSearchStates.selecting_client_search_method))
    async def create_new_client(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(CallCenterClientSearchStates.entering_new_client_name)
        await callback.message.edit_text("➕ Yangi mijoz nomini kiriting:")

    @router.callback_query(F.data == "cc_cancel_application_creation")
    async def cancel_creation(callback: CallbackQuery, state: FSMContext):
        await state.clear()
        await callback.message.edit_text("❌ Zayavka yaratish bekor qilindi")
        await callback.answer()

    @router.message(StateFilter(CallCenterClientSearchStates.entering_phone))
    async def process_phone_search(message: Message, state: FSMContext):
        phone = message.text.strip()
        clients = await search_clients_by_phone(phone)
        await _show_clients_list(message, state, clients)

    @router.message(StateFilter(CallCenterClientSearchStates.entering_name))
    async def process_name_search(message: Message, state: FSMContext):
        name = message.text.strip()
        clients = await search_clients_by_name(name)
        await _show_clients_list(message, state, clients)

    @router.message(StateFilter(CallCenterClientSearchStates.entering_client_id))
    async def process_id_search(message: Message, state: FSMContext):
        client_id = message.text.strip()
        clients = [{'id': int(client_id) if client_id.isdigit() else 9999, 'full_name': f'Mijoz #{client_id}', 'phone': '+998900000000'}]
        await _show_clients_list(message, state, clients)

    @router.message(StateFilter(CallCenterClientSearchStates.entering_new_client_name))
    async def process_new_client(message: Message, state: FSMContext):
        full_name = message.text.strip()
        clients = [{'id': -1, 'full_name': full_name, 'phone': 'N/A'}]
        await _show_clients_list(message, state, clients)

    async def _show_clients_list(message: Message, state: FSMContext, clients):
        if not clients:
            await message.answer("Mijoz topilmadi. Qayta urinib ko'ring.")
            await state.set_state(CallCenterClientSearchStates.selecting_client_search_method)
            await message.answer("Qidirish usulini tanlang:", reply_markup=get_call_center_client_search_keyboard('uz'))
            return
        await state.update_data(found_clients=clients)
        await state.set_state(CallCenterClientSearchStates.selecting_client)

        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        rows = []
        for i, c in enumerate(clients[:5]):
            rows.append([InlineKeyboardButton(text=f"{c['full_name']} - {c.get('phone','N/A')}", callback_data=f"cc_select_client_{i}")])
        rows.append([InlineKeyboardButton(text="🔍 Boshqa qidirish", callback_data="cc_search_again")])
        rows.append([InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cc_cancel_application_creation")])
        kb = InlineKeyboardMarkup(inline_keyboard=rows)
        await message.answer("Mijozni tanlang:", reply_markup=kb)

    @router.callback_query(lambda c: c.data.startswith("cc_select_client_"), StateFilter(CallCenterClientSearchStates.selecting_client))
    async def select_client(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        data = await state.get_data()
        clients = data.get('found_clients', [])
        idx = int(callback.data.split('_')[-1])
        if idx >= len(clients):
            await callback.answer("Xato", show_alert=True)
            return
        await state.update_data(selected_client=clients[idx])
        await callback.message.edit_text("Hududni tanlang:")
        await callback.message.answer("Hududni tanlang:", reply_markup=get_controller_regions_keyboard('uz'))
        await state.set_state(CallCenterServiceOrderStates.selecting_region)

    @router.callback_query(F.data == "cc_search_again")
    async def search_again(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(CallCenterClientSearchStates.selecting_client_search_method)
        await callback.message.edit_text("Qidirish usulini tanlang:")
        await callback.message.answer("Qidirish usulini tanlang:", reply_markup=get_call_center_client_search_keyboard('uz'))

    # 3) Technical service flow (after client selected)
    @router.callback_query(F.data.startswith("ctrl_region_"), StateFilter(CallCenterServiceOrderStates.selecting_region))
    async def select_region(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        region = callback.data.replace("ctrl_region_", "")
        await state.update_data(region=region)

        await callback.message.answer(
            "Abonent turini tanlang:",
            reply_markup=controller_zayavka_type_keyboard('uz')
        )
        await state.set_state(CallCenterServiceOrderStates.selecting_order_type)

    @router.callback_query(F.data.startswith("ctrl_zayavka_type_"), StateFilter(CallCenterServiceOrderStates.selecting_order_type))
    async def select_abonent_type(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        abonent_type = callback.data.replace("ctrl_zayavka_type_", "")
        await state.update_data(abonent_type=abonent_type)

        await callback.message.answer("Abonent ID raqamini kiriting:")
        await state.set_state(CallCenterServiceOrderStates.waiting_for_abonent_id)

    @router.message(StateFilter(CallCenterServiceOrderStates.waiting_for_abonent_id))
    async def get_abonent_id(message: Message, state: FSMContext):
        await state.update_data(abonent_id=message.text)
        await message.answer("Muammo tavsifini kiriting:")
        await state.set_state(CallCenterServiceOrderStates.entering_description)

    @router.message(StateFilter(CallCenterServiceOrderStates.entering_description))
    async def get_service_description(message: Message, state: FSMContext):
        await state.update_data(description=message.text)

        await message.answer(
            "Foto yoki video yuborasizmi?",
            reply_markup=controller_media_attachment_keyboard('uz')
        )
        await state.set_state(CallCenterServiceOrderStates.asking_for_media)

    @router.callback_query(F.data.in_(["ctrl_attach_media_yes", "ctrl_attach_media_no"]), StateFilter(CallCenterServiceOrderStates.asking_for_media))
    async def ask_for_media(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        if callback.data == "ctrl_attach_media_yes":
            await callback.message.answer("Foto yoki videoni yuboring:")
            await state.set_state(CallCenterServiceOrderStates.waiting_for_media)
        else:
            await ask_for_address(callback, state)

    @router.message(StateFilter(CallCenterServiceOrderStates.waiting_for_media), F.photo | F.video)
    async def process_media(message: Message, state: FSMContext):
        media_file_id = message.photo[-1].file_id if message.photo else message.video.file_id
        await state.update_data(media=media_file_id)
        await ask_for_address(message, state)

    async def ask_for_address(message_or_callback, state: FSMContext):
        if hasattr(message_or_callback, "message"):
            await message_or_callback.message.answer("Xizmat ko'rsatiladigan manzilni kiriting:")
        else:
            await message_or_callback.answer("Xizmat ko'rsatiladigan manzilni kiriting:")
        await state.set_state(CallCenterServiceOrderStates.entering_address)

    @router.message(StateFilter(CallCenterServiceOrderStates.entering_address))
    async def get_service_address(message: Message, state: FSMContext):
        await state.update_data(address=message.text)
        await message.answer(
            "Geolokatsiya yuborasizmi?",
            reply_markup=controller_geolocation_keyboard('uz')
        )
        await state.set_state(CallCenterServiceOrderStates.asking_for_location)

    @router.callback_query(F.data.in_(["ctrl_send_location_yes", "ctrl_send_location_no"]), StateFilter(CallCenterServiceOrderStates.asking_for_location))
    async def ask_for_geo(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        if callback.data == "ctrl_send_location_yes":
            await callback.message.answer("Geolokatsiyani yuboring:")
            await state.set_state(CallCenterServiceOrderStates.waiting_for_location)
        else:
            await show_service_confirmation(callback, state)

    @router.message(StateFilter(CallCenterServiceOrderStates.waiting_for_location), F.location)
    async def get_geo(message: Message, state: FSMContext):
        await state.update_data(geo=message.location)
        await show_service_confirmation(message, state)

    async def show_service_confirmation(message_or_callback, state: FSMContext):
        data = await state.get_data()
        selected_client = data.get('selected_client', {})
        region = data.get('region', '-')
        abonent_type = data.get('abonent_type', '-')
        abonent_id = data.get('abonent_id', '-')
        description = data.get('description', '-')
        address = data.get('address', '-')
        geo = data.get('geo')
        media = data.get('media')

        text = (
            f"👤 <b>Mijoz:</b> {selected_client.get('full_name','N/A')}\n"
            f"🏛️ <b>Hudud:</b> {region}\n"
            f"👤 <b>Abonent turi:</b> {abonent_type}\n"
            f"🆔 <b>Abonent ID:</b> {abonent_id}\n"
            f"📝 <b>Muammo tavsifi:</b> {description}\n"
            f"🏠 <b>Manzil:</b> {address}\n"
            f"📍 <b>Geolokatsiya:</b> {'✅ Yuborilgan' if geo else '❌ Yuborilmagan'}\n"
            f"🖼 <b>Media:</b> {'✅ Yuborilgan' if media else '❌ Yuborilmagan'}"
        )

        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="cc_confirm_service"),
             InlineKeyboardButton(text="🔄 Qayta yuborish", callback_data="cc_resend_service")]
        ])

        if hasattr(message_or_callback, 'message'):
            await message_or_callback.message.answer(text, parse_mode='HTML', reply_markup=kb)
        else:
            await message_or_callback.answer(text, parse_mode='HTML', reply_markup=kb)
        await state.set_state(CallCenterServiceOrderStates.confirming_order)

    @router.callback_query(F.data == "cc_confirm_service", StateFilter(CallCenterServiceOrderStates.confirming_order))
    async def confirm_service_order(callback: CallbackQuery, state: FSMContext):
        try:
            try:
                await callback.message.edit_reply_markup(reply_markup=None)
            except Exception:
                pass
            await callback.answer()

            request_id = f"TX_CC_{callback.from_user.id}_{int(datetime.now().timestamp())}"
            success_msg = (
                "✅ Texnik xizmat arizasi call center tomonidan yaratildi!\n"
                f"Ariza ID: {request_id[:10]}\n"
                "Operatorlar tez orada mijoz bilan bog'lanadi."
            )
            await callback.message.answer(success_msg)
            await state.clear()
        except Exception:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "cc_resend_service", StateFilter(CallCenterServiceOrderStates.confirming_order))
    async def resend_service_summary(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await show_service_confirmation(callback, state)

    return router