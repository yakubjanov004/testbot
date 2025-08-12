from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from filters.role_filter import RoleFilter
from states.call_center_states import CallCenterStandaloneSearchStates

# Mock search helpers (no DB)
async def search_clients_by_phone(phone: str):
    return [
        {'id': 101, 'full_name': 'Aziz Karimov', 'phone': phone, 'address': 'Toshkent sh.'},
        {'id': 102, 'full_name': 'Malika Yusupova', 'phone': phone, 'address': 'Yunusobod'},
    ]

async def search_clients_by_name(name: str):
    return [
        {'id': 103, 'full_name': name, 'phone': '+998901112233', 'address': 'Chilonzor'}
    ]

async def search_clients_by_id(client_id: str):
    return [
        {'id': int(client_id) if client_id.isdigit() else 9999, 'full_name': f'Mijoz #{client_id}', 'phone': '+998900000000', 'address': 'N/A'}
    ]


def get_call_center_client_search_router():
    router = Router()

    role_filter = RoleFilter("call_center")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🔍 Mijoz qidirish", "🔍 Поиск клиента"]))
    async def start_search(message: Message, state: FSMContext):
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📱 Telefon", callback_data="cc_find_phone"),
             InlineKeyboardButton(text="👤 Ism", callback_data="cc_find_name")],
            [InlineKeyboardButton(text="🆔 ID", callback_data="cc_find_id")],
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cc_find_cancel")],
        ])
        await message.answer("Qidirish usulini tanlang:", reply_markup=kb)
        await state.set_state(CallCenterStandaloneSearchStates.selecting_method)

    @router.callback_query(F.data == "cc_find_cancel")
    async def cancel(callback: CallbackQuery, state: FSMContext):
        await state.clear()
        await callback.message.edit_text("❌ Qidiruv bekor qilindi")
        await callback.answer()

    @router.callback_query(F.data == "cc_find_phone", StateFilter(CallCenterStandaloneSearchStates.selecting_method))
    async def method_phone(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(CallCenterStandaloneSearchStates.entering_phone)
        await callback.message.edit_text("📱 Telefon raqamini kiriting:\nMasalan: +998901234567")

    @router.callback_query(F.data == "cc_find_name", StateFilter(CallCenterStandaloneSearchStates.selecting_method))
    async def method_name(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(CallCenterStandaloneSearchStates.entering_name)
        await callback.message.edit_text("👤 Mijoz ismini kiriting:")

    @router.callback_query(F.data == "cc_find_id", StateFilter(CallCenterStandaloneSearchStates.selecting_method))
    async def method_id(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(CallCenterStandaloneSearchStates.entering_id)
        await callback.message.edit_text("🆔 Mijoz ID sini kiriting:")

    @router.message(StateFilter(CallCenterStandaloneSearchStates.entering_phone))
    async def process_phone(message: Message, state: FSMContext):
        clients = await search_clients_by_phone(message.text.strip())
        await _show_list(message, state, clients)

    @router.message(StateFilter(CallCenterStandaloneSearchStates.entering_name))
    async def process_name(message: Message, state: FSMContext):
        clients = await search_clients_by_name(message.text.strip())
        await _show_list(message, state, clients)

    @router.message(StateFilter(CallCenterStandaloneSearchStates.entering_id))
    async def process_id(message: Message, state: FSMContext):
        clients = await search_clients_by_id(message.text.strip())
        await _show_list(message, state, clients)

    async def _show_list(message: Message, state: FSMContext, clients):
        if not clients:
            await message.answer("Mijoz topilmadi.")
            await state.clear()
            return
        await state.update_data(found_clients=clients)
        await state.set_state(CallCenterStandaloneSearchStates.selecting_client)

        rows = []
        for idx, c in enumerate(clients[:10]):
            rows.append([InlineKeyboardButton(text=f"{c['full_name']} - {c.get('phone','N/A')}", callback_data=f"cc_find_select_{idx}")])
        rows.append([InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cc_find_cancel")])
        kb = InlineKeyboardMarkup(inline_keyboard=rows)
        await message.answer("Mijozni tanlang:", reply_markup=kb)

    @router.callback_query(lambda c: c.data.startswith("cc_find_select_"), StateFilter(CallCenterStandaloneSearchStates.selecting_client))
    async def select_client(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        data = await state.get_data()
        clients = data.get('found_clients', [])
        idx = int(callback.data.split('_')[-1])
        if idx >= len(clients):
            await callback.answer("Xato", show_alert=True)
            return
        client = clients[idx]
        text = (
            f"👤 <b>Mijoz:</b> {client.get('full_name')}\n"
            f"📱 <b>Telefon:</b> {client.get('phone')}\n"
            f"📍 <b>Manzil:</b> {client.get('address','N/A')}\n"
            f"🆔 <b>ID:</b> {client.get('id')}"
        )
        await callback.message.edit_text(text, parse_mode='HTML')
        await state.clear()

    return router