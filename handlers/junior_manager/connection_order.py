"""
Junior Manager Application Creation Handler - Soddalashtirilgan versiya

Bu modul junior manager uchun ariza yaratish funksionalligini o'z ichiga oladi.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from datetime import datetime
from filters.role_filter import RoleFilter
from keyboards.client_buttons import (
    get_client_regions_keyboard,
    zayavka_type_keyboard,
    get_client_tariff_selection_keyboard,
    geolocation_keyboard,
    confirmation_keyboard,
)


# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'junior_manager',
        'language': 'uz',
        'full_name': 'Test Junior Manager',
        'phone_number': '+998901234567'
    }

async def create_connection_request_for_client(creator_id: int, data: dict):
    """Mock: create connection request on behalf of a client"""
    return {
        'id': f"UL_{creator_id}_{int(datetime.now().timestamp())}",
        'region': data.get('region'),
        'connection_type': data.get('connection_type'),
        'tariff': data.get('selected_tariff'),
        'address': data.get('address'),
        'geo': bool(data.get('geo')),
        'created_at': datetime.now(),
    }


class JuniorManagerConnectionStates(StatesGroup):
    selecting_region = State()
    selecting_connection_type = State()
    selecting_tariff = State()
    entering_address = State()
    asking_for_geo = State()
    waiting_for_geo = State()
    confirming_connection = State()


def get_junior_manager_application_creation_router():
    """Junior manager creates a client connection order with the same flow as the client."""
    router = Router()

    # Apply role filter
    role_filter = RoleFilter("junior_manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🔌 Ulanish arizasi yaratish"]))
    async def start_connection_order(message: Message, state: FSMContext):
        """Start connection order creation on behalf of a client."""
        user = await get_user_by_telegram_id(message.from_user.id)
        if not user:
            await message.answer("Xatolik: Foydalanuvchi ma'lumotlari topilmadi. Iltimos, qaytadan urinib ko'ring.")
            return

        await message.answer("Hududni tanlang:", reply_markup=get_client_regions_keyboard())
        await state.set_state(JuniorManagerConnectionStates.selecting_region)

    @router.callback_query(
        F.data.startswith("region_"),
        StateFilter(JuniorManagerConnectionStates.selecting_region),
    )
    async def select_region(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        region = callback.data.split("_")[-1]
        await state.update_data(region=region)

        await callback.message.answer(
            "Ulanish turini tanlang:",
            reply_markup=zayavka_type_keyboard('uz')
        )
        await state.set_state(JuniorManagerConnectionStates.selecting_connection_type)

    @router.callback_query(
        F.data.startswith("zayavka_type_"),
        StateFilter(JuniorManagerConnectionStates.selecting_connection_type),
    )
    async def select_connection_type(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        connection_type = callback.data.split("_")[-1]
        await state.update_data(connection_type=connection_type)

        await callback.message.answer(
            "Tariflardan birini tanlang:",
            reply_markup=get_client_tariff_selection_keyboard()
        )
        await state.set_state(JuniorManagerConnectionStates.selecting_tariff)

    @router.callback_query(
        F.data.in_(["tariff_standard", "tariff_new"]),
        StateFilter(JuniorManagerConnectionStates.selecting_tariff),
    )
    async def select_tariff(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        tariff = "Standard" if callback.data == "tariff_standard" else "Yangi"
        await state.update_data(selected_tariff=tariff)

        await callback.message.answer("Mijoz manzilini kiriting:")
        await state.set_state(JuniorManagerConnectionStates.entering_address)

    @router.message(StateFilter(JuniorManagerConnectionStates.entering_address))
    async def get_connection_address(message: Message, state: FSMContext):
        await state.update_data(address=message.text.strip())

        await message.answer(
            "Geolokatsiya yuborasizmi?",
            reply_markup=geolocation_keyboard('uz')
        )
        await state.set_state(JuniorManagerConnectionStates.asking_for_geo)

    @router.callback_query(
        F.data.in_(["send_location_yes", "send_location_no"]),
        StateFilter(JuniorManagerConnectionStates.asking_for_geo),
    )
    async def ask_for_geo(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        if callback.data == "send_location_yes":
            await callback.message.answer("Geolokatsiyani yuboring:")
            await state.set_state(JuniorManagerConnectionStates.waiting_for_geo)
        else:
            await finish_connection_order(callback, state, geo=None)

    @router.message(StateFilter(JuniorManagerConnectionStates.waiting_for_geo), F.location)
    async def get_geo(message: Message, state: FSMContext):
        await state.update_data(geo=message.location)
        await finish_connection_order(message, state, geo=message.location)

    async def finish_connection_order(message_or_callback, state: FSMContext, geo=None):
        """Show final confirmation before creating the request."""
        data = await state.get_data()
        region = data.get('region', '-')
        connection_type = data.get('connection_type', 'standard')
        tariff = data.get('selected_tariff', 'Standard')
        address = data.get('address', '-')

        text = (
            f"🏛️ <b>Hudud:</b> {region}\n"
            f"🔌 <b>Ulanish turi:</b> {connection_type}\n"
            f"💳 <b>Tarif:</b> {tariff}\n"
            f"🏠 <b>Manzil:</b> {address}\n"
            f"📍 <b>Geolokatsiya:</b> {'✅ Yuborilgan' if geo else '❌ Yuborilmagan'}"
        )

        if hasattr(message_or_callback, "message"):
            await message_or_callback.message.answer(text, parse_mode='HTML', reply_markup=confirmation_keyboard('uz'))
        else:
            await message_or_callback.answer(text, parse_mode='HTML', reply_markup=confirmation_keyboard('uz'))

        await state.set_state(JuniorManagerConnectionStates.confirming_connection)

    @router.callback_query(
        F.data == "confirm_zayavka",
        StateFilter(JuniorManagerConnectionStates.confirming_connection),
    )
    async def confirm_connection_order(callback: CallbackQuery, state: FSMContext):
        try:
            try:
                await callback.message.edit_reply_markup(reply_markup=None)
            except Exception:
                pass
            await callback.answer()

            data = await state.get_data()
            user = await get_user_by_telegram_id(callback.from_user.id)

            # Create request on behalf of client
            created = await create_connection_request_for_client(callback.from_user.id, data)

            success_msg = (
                "✅ Ulanish arizasi yaratildi!\n"
                f"Ariza ID: {created['id'][:8]}\n"
                "Controller/menejer tez orada bog'lanadi."
            )
            await callback.message.answer(success_msg)
            await state.clear()
        except Exception:
            await callback.answer("Xatolik yuz berdi")

    return router 