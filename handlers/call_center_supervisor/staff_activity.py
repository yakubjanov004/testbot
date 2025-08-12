from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter
from typing import List, Dict
from keyboards.call_center_supervisor_buttons import get_call_center_supervisor_main_menu


def get_call_center_supervisor_staff_activity_router():
    router = Router()

    role_filter = RoleFilter("call_center_supervisor")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["👥 Xodimlar boshqaruvi", "👥 Управление сотрудниками"]))
    async def show_staff_activity_menu(message: Message, state: FSMContext):
        lang = 'uz'
        text = "👥 Call Center xodimlari boshqaruvi"
        await message.answer(text, reply_markup=_get_staff_activity_menu_keyboard(lang))

    @router.callback_query(F.data == "ccs_staff_perf")
    async def cb_staff_performance(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await _show_staff_performance(callback)

    @router.callback_query(F.data == "ccs_staff_load")
    async def cb_staff_workload(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await _show_staff_workload(callback)

    @router.callback_query(F.data == "ccs_staff_list")
    async def cb_staff_list(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.update_data(ccs_staff_index=0)
        await _show_staff_detail(callback, state)

    @router.callback_query(F.data == "ccs_staff_prev")
    async def cb_staff_prev(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        data = await state.get_data()
        idx = max(0, int(data.get('ccs_staff_index', 0)) - 1)
        await state.update_data(ccs_staff_index=idx)
        await _show_staff_detail(callback, state)

    @router.callback_query(F.data == "ccs_staff_next")
    async def cb_staff_next(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        data = await state.get_data()
        idx = int(data.get('ccs_staff_index', 0)) + 1
        await state.update_data(ccs_staff_index=idx)
        await _show_staff_detail(callback, state)

    @router.callback_query(F.data == "ccs_staff_back")
    async def cb_staff_back(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        lang = 'uz'
        await callback.message.edit_text("🏠 Bosh menyu")
        await callback.message.answer("🏠 Bosh menyu", reply_markup=get_call_center_supervisor_main_menu(lang))

    return router


def _get_mock_call_center_staff() -> List[Dict]:
    return [
        {
            'full_name': 'Aziza Abdullayeva',
            'role': 'call_center',
            'status': 'available',
            'active_calls': 2,
            'completed_today': 9,
            'callbacks_scheduled': 1,
            'avg_handle_time_min': 4.8,
            'week_completed': 42,
            'week_avg_handle_time_min': 5.2,
        },
        {
            'full_name': 'Bobur Karimov',
            'role': 'call_center',
            'status': 'available',
            'active_calls': 1,
            'completed_today': 7,
            'callbacks_scheduled': 2,
            'avg_handle_time_min': 5.5,
            'week_completed': 36,
            'week_avg_handle_time_min': 6.1,
        },
        {
            'full_name': 'Malika Toshmatova',
            'role': 'call_center',
            'status': 'busy',
            'active_calls': 3,
            'completed_today': 11,
            'callbacks_scheduled': 0,
            'avg_handle_time_min': 4.1,
            'week_completed': 48,
            'week_avg_handle_time_min': 5.0,
        },
    ]


def _get_staff_activity_menu_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(text=("📊 Samaradorlik" if lang == 'uz' else "📊 Эффективность"), callback_data="ccs_staff_perf"),
            InlineKeyboardButton(text=("📋 Ish yuki" if lang == 'uz' else "📋 Нагрузка"), callback_data="ccs_staff_load"),
        ],
        [InlineKeyboardButton(text=("👤 Operatorlar kesimi" if lang == 'uz' else "👤 По операторам"), callback_data="ccs_staff_list")],
        [InlineKeyboardButton(text=("🔙 Orqaga" if lang == 'uz' else "🔙 Назад"), callback_data="ccs_staff_back")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


async def _show_staff_performance(callback: CallbackQuery):
    staff = _get_mock_call_center_staff()
    text_lines = ["📊 <b>Call Center xodimlar samaradorligi:</b>", ""]
    for s in sorted(staff, key=lambda x: x['completed_today'], reverse=True):
        status_emoji = "🟢" if s['status'] == 'available' else "🔴"
        text_lines.append(
            f"{status_emoji} {s['full_name']}: bugun {s['completed_today']} ta, o'rtacha {s['avg_handle_time_min']} daqiqa"
        )
    await _edit_or_answer(callback, "\n".join(text_lines))


async def _show_staff_workload(callback: CallbackQuery):
    staff = _get_mock_call_center_staff()
    text_lines = ["📋 <b>Ish yuki holati:</b>", ""]
    for s in staff:
        status_emoji = "🟢" if s['status'] == 'available' else "🔴"
        text_lines.append(
            f"{status_emoji} {s['full_name']}: faol qo'ng'iroqlar {s['active_calls']} ta, qayta qo'ng'iroqlar {s['callbacks_scheduled']} ta"
        )
    await _edit_or_answer(callback, "\n".join(text_lines))


async def _show_staff_detail(callback: CallbackQuery, state: FSMContext):
    staff = _get_mock_call_center_staff()
    data = await state.get_data()
    idx = max(0, min(int(data.get('ccs_staff_index', 0)), len(staff) - 1))
    s = staff[idx]

    status_map = {'available': '🟢 Mavjud', 'busy': '🔴 Band'}
    text = (
        f"👤 <b>{s['full_name']}</b> — 📞 Call Center\n\n"
        f"{status_map.get(s['status'], s['status'])}\n"
        f"📞 Faol qo'ng'iroqlar: {s['active_calls']}\n"
        f"✅ Bugun yakunlangan: {s['completed_today']}\n"
        f"⏰ O'rtacha ishlov vaqti: {s['avg_handle_time_min']} daqiqa\n"
        f"⏳ Qayta qo'ng'iroqlar: {s['callbacks_scheduled']}\n\n"
        f"📅 Oxirgi 7 kun: {s['week_completed']} ta, o'rtacha {s['week_avg_handle_time_min']} daqiqa\n"
        f"\n📊 <b>#{idx+1}/{len(staff)}</b>"
    )

    kb = _get_staff_detail_keyboard(idx, len(staff))
    try:
        await callback.message.edit_text(text, reply_markup=kb, parse_mode='HTML')
    except Exception:
        await callback.message.answer(text, reply_markup=kb, parse_mode='HTML')


def _get_staff_detail_keyboard(index: int, total: int) -> InlineKeyboardMarkup:
    nav_row = []
    if index > 0:
        nav_row.append(InlineKeyboardButton(text='⬅️ Oldingi', callback_data='ccs_staff_prev'))
    nav_row.append(InlineKeyboardButton(text=f'{index+1}/{total}', callback_data='noop'))
    if index < total - 1:
        nav_row.append(InlineKeyboardButton(text='Keyingi ➡️', callback_data='ccs_staff_next'))

    rows = [nav_row, [InlineKeyboardButton(text='🔙 Orqaga', callback_data='ccs_staff_back')]]
    return InlineKeyboardMarkup(inline_keyboard=rows)


async def _edit_or_answer(callback: CallbackQuery, text: str):
    try:
        await callback.message.edit_text(text, parse_mode='HTML', reply_markup=_get_staff_activity_menu_keyboard('uz'))
    except Exception:
        await callback.message.answer(text, parse_mode='HTML', reply_markup=_get_staff_activity_menu_keyboard('uz'))


