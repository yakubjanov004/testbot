"""
Controller Technicians Activity - DB-less Implementation

Shows technicians' activity for controller role with filters and per-technician detailed view.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Mock auth
async def get_user_by_telegram_id(telegram_id: int):
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'controller',
        'language': 'uz',
        'full_name': 'Test Controller'
    }

# Mock technicians dataset
async def get_technicians_activity() -> List[Dict[str, Any]]:
    base_time = datetime.now()
    return [
        {
            'id': 101,
            'full_name': 'Texnik 1',
            'phone': '+998901111111',
            'online_minutes_ago': 3,
            'assigned_tasks': 4,
            'in_progress': 2,
            'completed_today': 5,
            'success_rate': 92,
            'avg_response_time_min': 28,
            'last_seen': (base_time - timedelta(minutes=3)).strftime('%H:%M'),
            'attendance_today': '✅',
            'status': 'online'
        },
        {
            'id': 102,
            'full_name': 'Texnik 2',
            'phone': '+998902222222',
            'online_minutes_ago': 40,
            'assigned_tasks': 8,
            'in_progress': 3,
            'completed_today': 7,
            'success_rate': 85,
            'avg_response_time_min': 35,
            'last_seen': (base_time - timedelta(minutes=40)).strftime('%H:%M'),
            'attendance_today': '✅',
            'status': 'busy'
        },
        {
            'id': 103,
            'full_name': 'Texnik 3',
            'phone': '+998903333333',
            'online_minutes_ago': 5,
            'assigned_tasks': 2,
            'in_progress': 1,
            'completed_today': 2,
            'success_rate': 78,
            'avg_response_time_min': 42,
            'last_seen': (base_time - timedelta(minutes=5)).strftime('%H:%M'),
            'attendance_today': '❌',
            'status': 'online'
        },
    ]


def get_controller_technicians_router():
    router = Router()

    role_filter = RoleFilter('controller')
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    # Helpers
    def _filter_techs(techs: List[Dict[str, Any]], flt: str) -> List[Dict[str, Any]]:
        if flt == 'all':
            return techs
        if flt == 'online':
            return [t for t in techs if t.get('status') == 'online']
        if flt == 'busy':
            return [t for t in techs if t.get('assigned_tasks', 0) > 0]
        return techs

    def _tech_detail_keyboard(flt: str, index: int, total: int) -> InlineKeyboardMarkup:
        rows = []
        nav = []
        if index > 0:
            nav.append(InlineKeyboardButton(text='⬅️ Oldingi', callback_data=f'ctrl_tech_nav_prev_{flt}_{index-1}'))
        nav.append(InlineKeyboardButton(text=f"{index+1}/{total}", callback_data='noop'))
        if index < total - 1:
            nav.append(InlineKeyboardButton(text='Keyingi ➡️', callback_data=f'ctrl_tech_nav_next_{flt}_{index+1}'))
        if nav:
            rows.append(nav)
        rows.append([
            InlineKeyboardButton(text='📋 Hammasi', callback_data='ctrl_tech_filter_all'),
            InlineKeyboardButton(text='🟢 Onlayn', callback_data='ctrl_tech_filter_online'),
            InlineKeyboardButton(text='📋 Band', callback_data='ctrl_tech_filter_busy'),
        ])
        rows.append([
            InlineKeyboardButton(text='🔄 Yangilash', callback_data=f'ctrl_tech_refresh_detail_{flt}_{index}'),
            InlineKeyboardButton(text='⬅️ Orqaga', callback_data='controllers_back'),
        ])
        return InlineKeyboardMarkup(inline_keyboard=rows)

    async def _render_tech_detail(message_or_callback, flt: str = 'all', index: int = 0):
        techs = await get_technicians_activity()
        filtered = _filter_techs(techs, flt)
        total = len(filtered)
        if total == 0:
            text = "👥 <b>Texniklar faoliyati</b>\nHozircha ma'lumot yo'q"
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='📋 Hammasi', callback_data='ctrl_tech_filter_all'),
                 InlineKeyboardButton(text='🟢 Onlayn', callback_data='ctrl_tech_filter_online'),
                 InlineKeyboardButton(text='📋 Band', callback_data='ctrl_tech_filter_busy')],
                [InlineKeyboardButton(text='⬅️ Orqaga', callback_data='controllers_back')]
            ])
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer(text, reply_markup=kb, parse_mode='HTML')
            else:
                await message_or_callback.message.edit_text(text, reply_markup=kb, parse_mode='HTML')
            return
        index = max(0, min(index, total - 1))
        t = filtered[index]
        emoji_status = '🟢 Onlayn' if t.get('status') == 'online' else '🟠 Band'
        text = (
            "👥 <b>Texniklar faoliyati</b>\n\n"
            f"👨‍🔧 <b>F.I.O.:</b> {t.get('full_name','-')}\n"
            f"📞 <b>Telefon:</b> {t.get('phone','-')}\n"
            f"📌 <b>Status:</b> {emoji_status} (oxirgi ko'rildi: {t.get('last_seen','-')})\n"
            f"🧾 <b>Bugun bajarilgan:</b> {t.get('completed_today',0)} ta\n"
            f"📦 <b>Biriktirilgan:</b> {t.get('assigned_tasks',0)} ta\n"
            f"🔧 <b>Jarayonda:</b> {t.get('in_progress',0)} ta\n"
            f"📈 <b>Muvaffaqiyat:</b> {t.get('success_rate',0)}%\n"
            f"⏱ <b>O'rtacha javob vaqti:</b> {t.get('avg_response_time_min',0)} daqiqa\n"
            f"🗓 <b>Davomat (bugun):</b> {t.get('attendance_today','-')}\n"
            f"\n📊 <b>#{index+1}/{total}</b>"
        )
        kb = _tech_detail_keyboard(flt, index, total)
        if isinstance(message_or_callback, Message):
            await message_or_callback.answer(text, reply_markup=kb, parse_mode='HTML')
        else:
            await message_or_callback.message.edit_text(text, reply_markup=kb, parse_mode='HTML')

    # Entry: reply button
    @router.message(F.text.in_(["👥 Xodimlar faoliyati"]))
    async def technicians_activity(message: Message, state: FSMContext):
        user = await get_user_by_telegram_id(message.from_user.id)
        if not user or user.get('role') != 'controller':
            await message.answer("Sizda controller huquqi yo'q.")
            return
        await _render_tech_detail(message, flt='all', index=0)

    # Filters
    @router.callback_query(F.data == 'ctrl_tech_filter_all')
    async def tech_filter_all(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await _render_tech_detail(callback, flt='all', index=0)

    @router.callback_query(F.data == 'ctrl_tech_filter_online')
    async def tech_filter_online(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await _render_tech_detail(callback, flt='online', index=0)

    @router.callback_query(F.data == 'ctrl_tech_filter_busy')
    async def tech_filter_busy(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await _render_tech_detail(callback, flt='busy', index=0)

    # Navigation
    @router.callback_query(lambda c: c.data.startswith('ctrl_tech_nav_prev_'))
    async def tech_nav_prev(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        _, _, _, flt, index = callback.data.split('_')
        await _render_tech_detail(callback, flt=flt, index=int(index))

    @router.callback_query(lambda c: c.data.startswith('ctrl_tech_nav_next_'))
    async def tech_nav_next(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        _, _, _, flt, index = callback.data.split('_')
        await _render_tech_detail(callback, flt=flt, index=int(index))

    @router.callback_query(lambda c: c.data.startswith('ctrl_tech_refresh_detail_'))
    async def tech_refresh_detail(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        _, _, _, flt, index = callback.data.split('_')
        await _render_tech_detail(callback, flt=flt, index=int(index))

    return router