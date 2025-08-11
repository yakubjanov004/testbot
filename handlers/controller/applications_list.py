"""
Controller Applications List Handler - Simplified Implementation

Bu modul controller uchun arizalar ro'yxati va navigatsiyasini ta'minlaydi.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter
from datetime import datetime, timedelta


def get_controller_applications_list_router():
    router = Router()

    role_filter = RoleFilter("controller")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["📋 Arizalarni ko'rish"]))
    async def view_all_applications(message: Message, state: FSMContext):
        try:
            applications = await _mock_get_controller_applications()
            if not applications:
                await message.answer("Hozircha arizalar yo'q.")
                return
            await _show_application_details(message, applications[0], applications, 0)
        except Exception:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.startswith("ctrl_app_nav:"))
    async def navigate_applications(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            _, index_str = callback.data.split(":", 1)
            index = int(index_str)
            applications = await _mock_get_controller_applications()
            total = len(applications)
            if index < 0:
                index = 0
            if index >= total:
                index = total - 1
            await _show_application_details(callback, applications[index], applications, index)
        except Exception:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "ctrl_app_back")
    async def back_to_main(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            from keyboards.controllers_buttons import controllers_main_menu
            await callback.message.edit_text(
                "🎛️ Controller bosh menyu",
                reply_markup=controllers_main_menu('uz')
            )
        except Exception:
            await callback.answer("Xatolik yuz berdi")

    return router


async def _show_application_details(message_or_callback, application: dict, applications: list, index: int):
    workflow_type_emoji = {
        'connection_request': '🔌',
        'technical_service': '🔧',
        'call_center_direct': '📞'
    }.get(application.get('workflow_type'), '📄')

    workflow_type_text = {
        'connection_request': "Ulanish arizasi",
        'technical_service': "Texnik xizmat",
        'call_center_direct': "Call Center"
    }.get(application.get('workflow_type'), 'Boshqa')

    status_emoji = {
        'in_progress': '🟡',
        'created': '🟠',
        'completed': '🟢',
        'cancelled': '🔴'
    }.get(application.get('current_status'), '⚪')

    status_text = {
        'in_progress': "Jarayonda",
        'created': "Yaratilgan",
        'completed': "Bajarilgan",
        'cancelled': "Bekor qilingan"
    }.get(application.get('current_status'), "Noma'lum")

    created_date = application.get('created_at')
    if isinstance(created_date, datetime):
        created_date = created_date.strftime('%d.%m.%Y %H:%M')

    updated_date = application.get('updated_at') or application.get('created_at')
    if isinstance(updated_date, datetime):
        updated_date = updated_date.strftime('%d.%m.%Y %H:%M')

    text = (
        f"{workflow_type_emoji} <b>{workflow_type_text} - To'liq ma'lumot</b>\n\n"
        f"🆔 <b>Ariza ID:</b> {application.get('id')}\n"
        f"📅 <b>Yaratilgan:</b> {created_date}\n"
        f"🔄 <b>Yangilangan:</b> {updated_date}\n"
        f"👤 <b>Mijoz:</b> {application.get('contact_info', {}).get('full_name', '-')}\n"
        f"📞 <b>Telefon:</b> {application.get('contact_info', {}).get('phone', '-')}\n"
        f"🏛️ <b>Hudud:</b> {application.get('region', "Noma'lum")}\n"
        f"🏠 <b>Manzil:</b> {application.get('address', "Noma'lum")}\n"
        f"📝 <b>Tavsif:</b> {application.get('description', '-')}\n"
        f"{status_emoji} <b>Holat:</b> {status_text}\n"
        f"👨‍🔧 <b>Texnik:</b> {application.get('technician', 'Tayinlanmagan')}\n"
        f"⏰ <b>Taxminiy vaqt:</b> {application.get('estimated_time', "Noma'lum")}\n\n"
        f"📊 <b>Ariza #{index + 1} / {len(applications)}</b>"
    )

    keyboard = _applications_navigation_keyboard(index, len(applications))

    if hasattr(message_or_callback, 'message_id'):
        await message_or_callback.answer(text, reply_markup=keyboard, parse_mode='HTML')
    else:
        await message_or_callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')


def _applications_navigation_keyboard(index: int, total: int) -> InlineKeyboardMarkup:
    prev_index = max(index - 1, 0)
    next_index = min(index + 1, total - 1)
    buttons = []
    nav_row = []
    if index > 0:
        nav_row.append(InlineKeyboardButton(text="◀️ Oldingi", callback_data=f"ctrl_app_nav:{prev_index}"))
    if index < total - 1:
        nav_row.append(InlineKeyboardButton(text="Keyingi ▶️", callback_data=f"ctrl_app_nav:{next_index}"))
    if nav_row:
        buttons.append(nav_row)
    buttons.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="ctrl_app_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def _mock_get_controller_applications() -> list:
    now = datetime.now()
    return [
        {
            'id': 'req_101_2024_01_20',
            'workflow_type': 'connection_request',
            'current_status': 'in_progress',
            'contact_info': {'full_name': 'Sirojiddin Qo\'chqorov', 'phone': '+998901112233'},
            'created_at': now - timedelta(hours=4),
            'updated_at': now - timedelta(hours=1, minutes=10),
            'description': 'Yangi uyga internet ulash',
            'location': 'Toshkent, Chilonzor',
            'priority': 'high',
            'estimated_time': '2-3 kun',
            'technician': 'Umar Xolmatov',
            'region': 'Toshkent shahri',
            'address': 'Chilonzor 5, 10-uy'
        },
        {
            'id': 'req_102_2024_01_21',
            'workflow_type': 'technical_service',
            'current_status': 'created',
            'contact_info': {'full_name': 'Malika Nasirova', 'phone': '+998909998877'},
            'created_at': now - timedelta(hours=2, minutes=20),
            'updated_at': now - timedelta(hours=2),
            'description': 'WiFi ishlamayapti',
            'location': 'Toshkent, Sergeli',
            'priority': 'normal',
            'estimated_time': '1-2 kun',
            'technician': 'Tayinlanmagan',
            'region': 'Toshkent shahri',
            'address': 'Sergeli 2, 23-uy'
        }
    ]