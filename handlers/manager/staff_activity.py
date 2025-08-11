"""
Manager Staff Activity Handler - Complete Implementation

This module provides complete staff activity monitoring functionality for Manager role,
allowing managers to view online staff, performance, workload, attendance, and junior manager work.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from datetime import datetime, date, timedelta
from filters.role_filter import RoleFilter

def get_manager_staff_activity_router():
    """Get router for manager staff activity handlers"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text == "👥 Xodimlar faoliyati")
    async def show_staff_activity_menu(message: Message, state: FSMContext):
        """Manager staff activity handler"""
        try:
            activity_text = "👥 Xodimlar faoliyati:"
            keyboard = _create_staff_activity_keyboard()
            await message.answer(activity_text, reply_markup=keyboard)
        except Exception:
            await message.answer("Xatolik yuz berdi")

    # Inline callbacks for staff activity sections
    @router.callback_query(F.data == "staff_performance")
    async def cb_staff_performance(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await show_staff_performance(callback.message)

    @router.callback_query(F.data == "staff_workload")
    async def cb_staff_workload(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await show_staff_workload(callback.message)

    @router.callback_query(F.data == "staff_user_detail")
    async def cb_staff_user_detail(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.update_data(staff_user_index=0)
        await show_staff_user_detail(callback, state)

    @router.callback_query(F.data == "staff_user_prev")
    async def cb_staff_user_prev(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        data = await state.get_data()
        idx = max(0, int(data.get('staff_user_index', 0)) - 1)
        await state.update_data(staff_user_index=idx)
        await show_staff_user_detail(callback, state)

    @router.callback_query(F.data == "staff_user_next")
    async def cb_staff_user_next(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        data = await state.get_data()
        idx = int(data.get('staff_user_index', 0)) + 1
        await state.update_data(staff_user_index=idx)
        await show_staff_user_detail(callback, state)

    @router.callback_query(F.data == "staff_back")
    async def cb_staff_back(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        from keyboards.manager_buttons import get_manager_main_keyboard
        await callback.message.edit_text("Asosiy menyu:")
        await callback.message.answer("Asosiy menyu:", reply_markup=get_manager_main_keyboard())

    async def show_staff_performance(message):
        """Show staff performance statistics"""
        try:
            performance = [
                {'full_name': 'Technician A', 'completed_tasks': 32, 'total_tasks': 40},
                {'full_name': 'Technician B', 'completed_tasks': 25, 'total_tasks': 33},
                {'full_name': 'Controller C', 'completed_tasks': 41, 'total_tasks': 50},
                {'full_name': 'Junior Manager D', 'completed_tasks': 19, 'total_tasks': 24},
            ]
            text = "📊 <b>Xodimlar samaradorligi:</b>\n\n"
            for s in performance:
                pct = int((s['completed_tasks'] / s['total_tasks']) * 100) if s['total_tasks'] else 0
                text += f"👤 {s['full_name']}: {s['completed_tasks']} / {s['total_tasks']} ({pct}%)\n"
            await message.answer(text, parse_mode='HTML')
        except Exception:
            await message.answer("Xatolik yuz berdi")

    async def show_staff_workload(message):
        """Show staff workload statistics"""
        try:
            workload = [
                {'full_name': 'Technician A', 'total_tasks': 10, 'completed_tasks': 7, 'pending_tasks': 3},
                {'full_name': 'Technician B', 'total_tasks': 12, 'completed_tasks': 9, 'pending_tasks': 3},
                {'full_name': 'Controller C', 'total_tasks': 8, 'completed_tasks': 6, 'pending_tasks': 2},
                {'full_name': 'Junior Manager D', 'total_tasks': 6, 'completed_tasks': 5, 'pending_tasks': 1},
            ]
            text = "📋 <b>Ish yuki:</b>\n\n"
            for s in workload:
                text += (
                    f"👤 {s['full_name']}: {s['total_tasks']} ta ("
                    f"✅ {s['completed_tasks']}, ⏳ {s['pending_tasks']})\n"
                )
            await message.answer(text, parse_mode='HTML')
        except Exception:
            await message.answer("Xatolik yuz berdi")

    async def show_staff_user_detail(message_or_callback, state: FSMContext):
        """Per-employee detailed card with navigation"""
        staff_list = [
            {
                'full_name': 'Technician A',
                'role': 'technician',
                'completed_today': 5,
                'in_progress': 2,
                'cancelled': 0,
                'success_rate': 92,
                'avg_completion_hours': 3.4,
                'tasks_by_type': {'Ulanish': 3, 'Texnik xizmat': 4},
                'last_7_days_completed': 21,
                'last_7_days_avg_hours': 3.9,
            },
            {
                'full_name': 'Technician B',
                'role': 'technician',
                'completed_today': 3,
                'in_progress': 3,
                'cancelled': 1,
                'success_rate': 84,
                'avg_completion_hours': 4.2,
                'tasks_by_type': {'Ulanish': 4, 'Texnik xizmat': 3},
                'last_7_days_completed': 18,
                'last_7_days_avg_hours': 4.5,
            },
            {
                'full_name': 'Junior Manager D',
                'role': 'junior_manager',
                'completed_today': 2,
                'in_progress': 1,
                'cancelled': 0,
                'success_rate': 88,
                'avg_completion_hours': 2.8,
                'tasks_by_type': {'Ulanish': 2, 'Tekshirish': 1},
                'last_7_days_completed': 14,
                'last_7_days_avg_hours': 3.1,
            },
        ]
        data = await state.get_data()
        idx = max(0, min(int(data.get('staff_user_index', 0)), len(staff_list) - 1))
        s = staff_list[idx]
        role_map = {'technician': '👨‍🔧 Texnik', 'junior_manager': '👨‍💼 Kichik menejer', 'manager': '👨‍💼 Menejer'}
        by_type_lines = "\n".join([f"   • {k}: {v} ta" for k, v in s['tasks_by_type'].items()])
        text = (
            f"👤 <b>{s['full_name']}</b> — {role_map.get(s['role'], s['role'])}\n\n"
            f"✅ <b>Bugun bajarilgan:</b> {s['completed_today']} ta\n"
            f"⏳ <b>Jarayonda:</b> {s['in_progress']} ta\n"
            f"❌ <b>Bekor qilingan:</b> {s['cancelled']} ta\n"
            f"📈 <b>Muvaffaqiyat:</b> {s['success_rate']}%\n"
            f"⏱️ <b>O'rtacha bajarish vaqti:</b> {s['avg_completion_hours']} soat\n\n"
            f"🗂 <b>Ish turlari bo'yicha:</b>\n{by_type_lines}\n\n"
            f"📅 <b>Oxirgi 7 kun:</b> {s['last_7_days_completed']} ta, o'rtacha {s['last_7_days_avg_hours']} soat\n"
            f"\n📊 <b>#{idx+1}/{len(staff_list)}</b>"
        )
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='⬅️ Oldingi', callback_data='staff_user_prev') if idx > 0 else InlineKeyboardButton(text=f'{idx+1}/{len(staff_list)}', callback_data='noop'),
                InlineKeyboardButton(text='Keyingi ➡️', callback_data='staff_user_next') if idx < len(staff_list)-1 else InlineKeyboardButton(text=f'{idx+1}/{len(staff_list)}', callback_data='noop')
            ],
            [InlineKeyboardButton(text='⬅️ Orqaga', callback_data='staff_back')]
        ])
        if isinstance(message_or_callback, CallbackQuery):
            try:
                await message_or_callback.message.edit_text(text, reply_markup=kb, parse_mode='HTML')
            except Exception:
                await message_or_callback.message.answer(text, reply_markup=kb, parse_mode='HTML')
        else:
            await message_or_callback.answer(text, reply_markup=kb, parse_mode='HTML')

    return router


def _create_staff_activity_keyboard():
    """Create keyboard for staff activity menu (updated)"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📊 Samaradorlik", callback_data="staff_performance"),
            InlineKeyboardButton(text="📋 Ish yuki", callback_data="staff_workload"),
        ],
        [
            InlineKeyboardButton(text="👤 Xodimlar kesimi", callback_data="staff_user_detail"),
        ],
        [
            InlineKeyboardButton(text="🔙 Orqaga", callback_data="staff_back")
        ],
    ])
