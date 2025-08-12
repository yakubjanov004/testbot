from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta
from filters.role_filter import RoleFilter
from keyboards.technician_buttons import (
    get_technician_back_keyboard,
    get_technician_main_menu_keyboard,
)


async def get_mock_completed_tasks(user_id: int):
    """Return mock list of completed tasks for technician."""
    now = datetime.now()
    return [
        {
            'id': 'done_001_2024_01_10',
            'workflow_type': 'technical_service',
            'created_at': now - timedelta(days=7, hours=2),
            'completed_at': now - timedelta(days=7),
            'contact_info': {
                'full_name': 'Otabek Islomov',
                'phone': '+998901111111'
            },
            'location': 'Toshkent, Mirobod tumani, 12-uy',
            'priority': 'high',
            'tariff': '',
            'connection_type': '',
            'equipment_needed': 'Switch 8-port',
            'estimated_cost': "350,000 so'm",
            'expected_completion': '1 kun',
            'diagnostic_result': 'Switch nosozligi aniqlanib, almashtirildi',
            'work_notes': 'Nosoz switch almashtirildi, xizmatlar qayta ishga tushdi',
            'warehouse_needed': True,
            'warehouse_item': 'Switch 8-port - 1 dona',
        },
        {
            'id': 'done_002_2024_01_12',
            'workflow_type': 'connection_request',
            'created_at': now - timedelta(days=5, hours=5),
            'completed_at': now - timedelta(days=5, hours=1),
            'contact_info': {
                'full_name': 'Dilshod Karimov',
                'phone': '+998902222222'
            },
            'location': 'Toshkent, Chilonzor tumani, 9-mavze',
            'priority': 'normal',
            'tariff': '100 Mbps',
            'connection_type': 'B2C',
            'equipment_needed': 'Router TP-Link Archer C6',
            'estimated_cost': "300,000 so'm",
            'expected_completion': '3 kun',
            'diagnostic_result': 'Ulanish ishga tushirildi',
            'work_notes': 'Router o‘rnatildi, sozlamalar bajarildi, ulanish muvaffaqiyatli',
            'warehouse_needed': True,
            'warehouse_item': 'Router TP-Link Archer C6 - 1 dona',
        },
    ]


def build_tasks_nav_keyboard(index: int, total: int, lang: str = 'uz') -> InlineKeyboardMarkup:
    keyboard = []
    if total > 1 and index > 0:
        prev_text = "⬅️ Oldingi" if lang == 'uz' else "⬅️ Предыдущий"
        keyboard.append([InlineKeyboardButton(text=prev_text, callback_data="tech_tasks_prev_task")])
    if total > 1 and index < total - 1:
        next_text = "Keyingi ➡️" if lang == 'uz' else "Следующий ➡️"
        keyboard.append([InlineKeyboardButton(text=next_text, callback_data="tech_tasks_next_task")])
    home_text = "🏠 Asosiy menyu" if lang == 'uz' else "🏠 Главное меню"
    keyboard.append([InlineKeyboardButton(text=home_text, callback_data="tech_tasks_back_to_main")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def show_task_details(message_or_callback, task: dict, index: int, total: int, lang: str = 'uz'):
    try:
        workflow_emoji = {
            'connection_request': '🔌',
            'technical_service': '🔧',
            'call_center_direct': '📞',
        }.get(task.get('workflow_type', ''), '📄')

        priority_text = {
            'urgent': 'Shoshilinch',
            'high': 'Yuqori',
            'medium': "O'rtacha",
            'normal': 'Oddiy',
        }.get(task.get('priority', 'normal'), 'Oddiy')

        created_date = task.get('created_at')
        created_str = created_date.strftime('%d.%m.%Y %H:%M') if isinstance(created_date, datetime) else '-'
        completed_date = task.get('completed_at')
        completed_str = completed_date.strftime('%d.%m.%Y %H:%M') if isinstance(completed_date, datetime) else datetime.now().strftime('%d.%m.%Y %H:%M')

        text = (
            f"{workflow_emoji} <b>Bajarilgan vazifa</b>\n\n"
            f"🆔 <b>ID:</b> {task.get('id', '-') }\n"
            f"📅 <b>Yaratilgan:</b> {created_str}\n"
            f"✅ <b>Yakunlangan:</b> {completed_str}\n"
            f"👤 <b>Mijoz:</b> {task.get('contact_info', {}).get('full_name', '-') }\n"
            f"📞 <b>Telefon:</b> {task.get('contact_info', {}).get('phone', '-') }\n"
            f"📍 <b>Manzil:</b> {task.get('location', '-') }\n"
            f"⭐ <b>Ustuvorlik:</b> {priority_text}\n"
        )

        if task.get('tariff'):
            text += f"📊 <b>Tarif:</b> {task['tariff']}\n"
        if task.get('connection_type'):
            text += f"🔗 <b>Ulanish turi:</b> {task['connection_type']}\n"
        if task.get('equipment_needed'):
            text += f"🔧 <b>Kerakli jihozlar:</b> {task['equipment_needed']}\n"
        if task.get('estimated_cost'):
            text += f"💰 <b>Narx:</b> {task['estimated_cost']}\n"
        if task.get('expected_completion'):
            text += f"⏱ <b>Muddat:</b> {task['expected_completion']}\n"
        if task.get('diagnostic_result'):
            text += f"\n🔍 <b>Diagnostika:</b> {task['diagnostic_result']}\n"
        if task.get('work_notes'):
            text += f"📝 <b>Ish izohi:</b> {task['work_notes']}\n"
        if task.get('warehouse_needed'):
            text += f"📦 <b>Ombor ishlatildi:</b> Ha\n"
            if task.get('warehouse_item'):
                text += f"📦 <b>Olingan mahsulot:</b> {task['warehouse_item']}\n"

        text += f"\n📊 <b>Vazifa #{index + 1} / {total}</b>"

        keyboard = build_tasks_nav_keyboard(index, total, lang)
        if isinstance(message_or_callback, Message):
            await message_or_callback.answer(text, reply_markup=keyboard, parse_mode='HTML')
        else:
            await message_or_callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
    except Exception:
        if isinstance(message_or_callback, Message):
            await message_or_callback.answer("❌ Xatolik yuz berdi")
        else:
            await message_or_callback.answer("❌ Xatolik yuz berdi")


def get_technician_tasks_router() -> Router:
    """Router for technician 'My Tasks' showing completed tasks with details and navigation."""
    router = Router()

    role_filter = RoleFilter("technician")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["📋 Vazifalarim", "📋 Мои задачи"]))
    async def my_tasks_entry(message: Message, state: FSMContext):
        """Entry point to show completed tasks list (detailed)."""
        try:
            # Prefer tasks from state (captured during Inbox use)
            data = await state.get_data()
            applications = data.get('applications', [])
            lang = data.get('lang', 'uz')
            completed_from_state = [a for a in applications if a.get('work_completed')]

            if completed_from_state:
                tasks = []
                for t in completed_from_state:
                    # Build a compact task dict for display
                    tasks.append({
                        'id': t.get('id'),
                        'workflow_type': t.get('workflow_type'),
                        'created_at': t.get('created_at'),
                        'completed_at': datetime.now(),
                        'contact_info': t.get('contact_info', {}),
                        'location': t.get('location'),
                        'priority': t.get('priority', 'normal'),
                        'tariff': t.get('tariff', ''),
                        'connection_type': t.get('connection_type', ''),
                        'equipment_needed': t.get('equipment_needed', ''),
                        'estimated_cost': t.get('estimated_cost', ''),
                        'expected_completion': t.get('expected_completion', ''),
                        'diagnostic_result': t.get('diagnostic_result', ''),
                        'work_notes': t.get('work_notes', ''),
                        'warehouse_needed': t.get('warehouse_needed', False),
                        'warehouse_item': t.get('warehouse_item', ''),
                    })
            else:
                # Fallback mock data
                tasks = await get_mock_completed_tasks(message.from_user.id)
                lang = 'uz'

            if not tasks:
                none_text = "📭 Hozircha bajarilgan vazifalar yo'q." if lang == 'uz' else "📭 Пока нет выполненных задач."
                await message.answer(none_text, reply_markup=get_technician_back_keyboard(lang))
                return

            await state.update_data(completed_tasks=tasks, current_completed_index=0, lang=lang)
            await show_task_details(message, tasks[0], 0, len(tasks), lang)
        except Exception:
            await message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "tech_tasks_prev_task")
    async def tasks_prev(callback: CallbackQuery, state: FSMContext):
        try:
            data = await state.get_data()
            tasks = data.get('completed_tasks', [])
            index = data.get('current_completed_index', 0)
            lang = data.get('lang', 'uz')
            if not tasks:
                await callback.answer("Topilmadi")
                return
            if index > 0:
                index -= 1
                await state.update_data(current_completed_index=index)
                await show_task_details(callback, tasks[index], index, len(tasks), lang)
            else:
                await callback.answer("Bu birinchi vazifa")
        except Exception:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "tech_tasks_next_task")
    async def tasks_next(callback: CallbackQuery, state: FSMContext):
        try:
            data = await state.get_data()
            tasks = data.get('completed_tasks', [])
            index = data.get('current_completed_index', 0)
            lang = data.get('lang', 'uz')
            if not tasks:
                await callback.answer("Topilmadi")
                return
            if index < len(tasks) - 1:
                index += 1
                await state.update_data(current_completed_index=index)
                await show_task_details(callback, tasks[index], index, len(tasks), lang)
            else:
                await callback.answer("Bu oxirgi vazifa")
        except Exception:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "tech_tasks_back_to_main")
    async def tasks_back_to_main(callback: CallbackQuery, state: FSMContext):
        try:
            lang = (await state.get_data()).get('lang', 'uz')
            text = (
                "🔧 <b>Technician Panel</b>\n\n"
                "📊 Asosiy menyu\n\n"
                "Kerakli bo'limni tanlang:"
            )
            await callback.message.edit_text(text, parse_mode='HTML', reply_markup=get_technician_main_menu_keyboard(lang))
            await callback.answer()
        except Exception:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router


