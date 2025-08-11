from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime

from filters.role_filter import RoleFilter
from keyboards.manager_buttons import (
    get_manager_client_search_keyboard,
    get_manager_confirmation_keyboard,
)
from keyboards.controllers_buttons import (
    get_controller_regions_keyboard,
    controller_zayavka_type_keyboard,
    controller_media_attachment_keyboard,
    controller_geolocation_keyboard,
)
from states.manager_states import ManagerClientSearchStates, ManagerServiceOrderStates




def get_manager_technical_service_router():
    router = Router()

    role_filter = RoleFilter("manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    # Entry point
    @router.message(F.text == "🔧 Texnik xizmat yaratish")
    async def start_manager_service(message: Message, state: FSMContext):
        await state.update_data(current_flow='technical')
        await message.answer("Mijozni qanday qidiramiz?", reply_markup=get_manager_client_search_keyboard('uz'))
        await state.set_state(ManagerClientSearchStates.selecting_client_search_method)

    # Search method callbacks
    @router.callback_query(F.data == "mgr_search_phone", StateFilter(ManagerClientSearchStates.selecting_client_search_method))
    async def mgr_search_by_phone(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.update_data(search_method='phone')
        await callback.message.edit_text("📱 Telefon raqamini kiriting:\nMasalan: +998901234567")
        await state.set_state(ManagerClientSearchStates.entering_phone)

    @router.callback_query(F.data == "mgr_search_name", StateFilter(ManagerClientSearchStates.selecting_client_search_method))
    async def mgr_search_by_name(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.update_data(search_method='name')
        await callback.message.edit_text("👤 Mijoz ismini kiriting:\nMasalan: Alisher Karimov")
        await state.set_state(ManagerClientSearchStates.entering_name)

    @router.callback_query(F.data == "mgr_search_id", StateFilter(ManagerClientSearchStates.selecting_client_search_method))
    async def mgr_search_by_id(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.update_data(search_method='id')
        await callback.message.edit_text("🆔 Mijoz ID sini kiriting:\nMasalan: 12345")
        await state.set_state(ManagerClientSearchStates.entering_client_id)

    @router.callback_query(F.data == "mgr_search_new", StateFilter(ManagerClientSearchStates.selecting_client_search_method))
    async def mgr_create_new_client(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.update_data(search_method='new')
        await callback.message.edit_text("➕ Yangi mijoz nomini kiriting:")
        await state.set_state(ManagerClientSearchStates.entering_new_client_name)

    @router.callback_query(F.data == "mgr_cancel_creation")
    async def mgr_cancel_creation(callback: CallbackQuery, state: FSMContext):
        await state.clear()
        await callback.message.edit_text("❌ Ariza yaratish bekor qilindi")
        await callback.answer()

    # Collect user input for search entries (reuse flexible states from ManagerApplicationStates)
    @router.message(StateFilter(ManagerClientSearchStates.entering_phone, ManagerClientSearchStates.entering_name, ManagerClientSearchStates.entering_client_id, ManagerClientSearchStates.entering_new_client_name))
    async def handle_search_inputs(message: Message, state: FSMContext):
        data = await state.get_data()
        method = data.get('search_method')
        query = message.text.strip()
        # Mock clients
        if method == 'phone':
            clients = [
                {'id': 1, 'full_name': 'Ali Valiyev', 'phone': query},
                {'id': 2, 'full_name': 'Vali Aliev', 'phone': query},
            ]
        elif method == 'name':
            clients = [{'id': 3, 'full_name': query, 'phone': '+998901112233'}]
        elif method == 'id':
            clients = [{'id': int(query) if query.isdigit() else 9999, 'full_name': f'Mijoz #{query}', 'phone': '+998900000000'}]
        else:  # new
            clients = [{'id': -1, 'full_name': query, 'phone': 'N/A'}]

        await state.update_data(found_clients=clients)
        await state.set_state(ManagerClientSearchStates.selecting_client)
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        ikb = InlineKeyboardMarkup(inline_keyboard=[
            *[[InlineKeyboardButton(text=f"{c['full_name']} - {c.get('phone','N/A')}", callback_data=f"mgr_select_client_{i}")] for i, c in enumerate(clients[:5])],
            [InlineKeyboardButton(text="🔍 Boshqa qidirish", callback_data="mgr_search_again")],
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="mgr_cancel_creation")],
        ])
        await message.answer("Mijozni tanlang:", reply_markup=ikb)

    @router.callback_query(lambda c: c.data.startswith("mgr_select_client_"), StateFilter(ManagerClientSearchStates.selecting_client))
    async def mgr_select_client(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        data = await state.get_data()
        clients = data.get('found_clients', [])
        idx = int(callback.data.split('_')[-1])
        if idx >= len(clients):
            await callback.answer("Xato", show_alert=True)
            return
        await state.update_data(selected_client=clients[idx])
        # Proceed to service flow
        await callback.message.edit_text("Hududni tanlang:")
        await callback.message.answer("Hududni tanlang:", reply_markup=get_controller_regions_keyboard('uz'))
        await state.set_state(ManagerServiceOrderStates.selecting_region)

    @router.callback_query(F.data == "mgr_search_again", StateFilter(ManagerClientSearchStates.selecting_client))
    async def mgr_search_again(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await callback.message.edit_text("Qidirish usulini tanlang:")
        await callback.message.answer("Qidirish usulini tanlang:", reply_markup=get_manager_client_search_keyboard('uz'))

    # Service order flow (mirrors controller)
    @router.callback_query(F.data.startswith("ctrl_region_"), StateFilter(ManagerServiceOrderStates.selecting_region))
    async def mgr_select_region(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        region = callback.data.replace("ctrl_region_", "")
        await state.update_data(region=region)
        await callback.message.answer("Abonent turini tanlang:", reply_markup=controller_zayavka_type_keyboard('uz'))
        await state.set_state(ManagerServiceOrderStates.selecting_order_type)

    @router.callback_query(F.data.startswith("ctrl_zayavka_type_"), StateFilter(ManagerServiceOrderStates.selecting_order_type))
    async def mgr_select_abonent_type(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        abonent_type = callback.data.replace("ctrl_zayavka_type_", "")
        await state.update_data(abonent_type=abonent_type)
        await callback.message.answer("Abonent ID raqamini kiriting:")
        await state.set_state(ManagerServiceOrderStates.waiting_for_abonent_id)

    @router.message(StateFilter(ManagerServiceOrderStates.waiting_for_abonent_id))
    async def mgr_get_abonent_id(message: Message, state: FSMContext):
        await state.update_data(abonent_id=message.text)
        await message.answer("Muammo tavsifini kiriting:")
        await state.set_state(ManagerServiceOrderStates.entering_description)

    @router.message(StateFilter(ManagerServiceOrderStates.entering_description))
    async def mgr_get_service_description(message: Message, state: FSMContext):
        await state.update_data(description=message.text)
        await message.answer("Foto yoki video yuborasizmi?", reply_markup=controller_media_attachment_keyboard('uz'))
        await state.set_state(ManagerServiceOrderStates.asking_for_media)

    @router.callback_query(F.data.in_(["ctrl_attach_media_yes", "ctrl_attach_media_no"]), StateFilter(ManagerServiceOrderStates.asking_for_media))
    async def mgr_ask_for_media(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        if callback.data == "ctrl_attach_media_yes":
            await callback.message.answer("Foto yoki videoni yuboring:")
            await state.set_state(ManagerServiceOrderStates.waiting_for_media)
        else:
            await mgr_ask_for_address(callback, state)

    @router.message(StateFilter(ManagerServiceOrderStates.waiting_for_media), F.photo | F.video)
    async def mgr_process_media(message: Message, state: FSMContext):
        media_file_id = message.photo[-1].file_id if message.photo else message.video.file_id
        await state.update_data(media=media_file_id)
        await mgr_ask_for_address(message, state)

    async def mgr_ask_for_address(message_or_callback, state: FSMContext):
        if hasattr(message_or_callback, "message"):
            await message_or_callback.message.answer("Xizmat ko'rsatiladigan manzilni kiriting:")
        else:
            await message_or_callback.answer("Xizmat ko'rsatiladigan manzilni kiriting:")
        await state.set_state(ManagerServiceOrderStates.entering_address)

    @router.message(StateFilter(ManagerServiceOrderStates.entering_address))
    async def mgr_get_service_address(message: Message, state: FSMContext):
        await state.update_data(address=message.text)
        await message.answer("Geolokatsiya yuborasizmi?", reply_markup=controller_geolocation_keyboard('uz'))
        await state.set_state(ManagerServiceOrderStates.asking_for_location)

    @router.callback_query(F.data.in_(["ctrl_send_location_yes", "ctrl_send_location_no"]), StateFilter(ManagerServiceOrderStates.asking_for_location))
    async def mgr_ask_for_geo(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        if callback.data == "ctrl_send_location_yes":
            await callback.message.answer("Geolokatsiyani yuboring:")
            await state.set_state(ManagerServiceOrderStates.waiting_for_location)
        else:
            await mgr_show_service_confirmation(callback, state)

    @router.message(StateFilter(ManagerServiceOrderStates.waiting_for_location), F.location)
    async def mgr_get_geo(message: Message, state: FSMContext):
        await state.update_data(geo=message.location)
        await mgr_show_service_confirmation(message, state)

    async def mgr_show_service_confirmation(message_or_callback, state: FSMContext):
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

        if hasattr(message_or_callback, 'message'):
            await message_or_callback.message.answer(text, parse_mode='HTML', reply_markup=get_manager_confirmation_keyboard('uz'))
        else:
            await message_or_callback.answer(text, parse_mode='HTML', reply_markup=get_manager_confirmation_keyboard('uz'))
        await state.set_state(ManagerServiceOrderStates.confirming_order)

    @router.callback_query(F.data == "mgr_confirm_zayavka", StateFilter(ManagerServiceOrderStates.confirming_order))
    async def mgr_confirm_service_order(callback: CallbackQuery, state: FSMContext):
        try:
            try:
                await callback.message.edit_reply_markup(reply_markup=None)
            except Exception:
                pass
            await callback.answer()
            request_id = f"TX_MGR_{callback.from_user.id}_{int(datetime.now().timestamp())}"
            success_msg = (
                "✅ Texnik xizmat arizasi menejer tomonidan yaratildi!\n"
                f"Ariza ID: {request_id[:10]}\n"
                "Texniklar tez orada mijoz bilan bog'lanadi."
            )
            await callback.message.answer(success_msg)
            await state.clear()
        except Exception:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "mgr_resend_zayavka", StateFilter(ManagerServiceOrderStates.confirming_order))
    async def mgr_resend_service_summary(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await mgr_show_service_confirmation(callback, state)

    return router