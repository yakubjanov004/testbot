from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.manager_new_buttons import get_back_keyboard, get_pagination_keyboard, get_application_actions_keyboard
from utils.language import get_text
from utils.database import get_user_language, get_manager_inbox_applications
from utils.pagination import paginate_applications

router = Router()

@router.message(F.text == "📥 Inbox")
async def handle_inbox(message: Message, state: FSMContext):
    """Inbox handler"""
    lang = await get_user_language(message.from_user.id)
    user_id = message.from_user.id
    
    # Menejer uchun inbox arizalarini olish
    applications = await get_manager_inbox_applications(user_id)
    
    if not applications:
        text = get_text("inbox_empty", lang)
        await message.answer(text, reply_markup=get_back_keyboard(lang))
        return
    
    # Pagination bilan arizalarni ko'rsatish
    page = 1
    per_page = 5
    paginated_apps = paginate_applications(applications, page, per_page)
    
    text = get_text("inbox_welcome", lang)
    text += f"\n\n{get_text('total_applications', lang)}: {len(applications)}"
    text += f"\n{get_text('page', lang)}: {page}/{len(applications) // per_page + 1}"
    
    # Har bir ariza uchun ma'lumot
    for app in paginated_apps:
        status_emoji = {
            'new': '🆕',
            'in_progress': '⏳',
            'completed': '✅',
            'cancelled': '❌',
            'pending': '⏸️',
            'rejected': '🚫'
        }.get(app['status'], '❓')
        
        text += f"\n\n{status_emoji} {get_text('application', lang)} #{app['id']}"
        text += f"\n{get_text('client', lang)}: {app['client_name']}"
        text += f"\n{get_text('type', lang)}: {app['type']}"
        text += f"\n{get_text('status', lang)}: {get_text(f'status_{app['status']}', lang)}"
        text += f"\n{get_text('created_at', lang)}: {app['created_at']}"
    
    # Pagination keyboard
    total_pages = len(applications) // per_page + 1
    pagination_kb = get_pagination_keyboard(page, total_pages, lang)
    
    await message.answer(
        text=text,
        reply_markup=pagination_kb
    )
    
    # State'ga ma'lumotlarni saqlash
    await state.update_data({
        'applications': applications,
        'current_page': page,
        'per_page': per_page,
        'total_pages': total_pages
    })

@router.callback_query(F.data.startswith("page_"))
async def handle_pagination(callback: CallbackQuery, state: FSMContext):
    """Pagination handler"""
    page = int(callback.data.split("_")[1])
    lang = await get_user_language(callback.from_user.id)
    
    data = await state.get_data()
    applications = data.get('applications', [])
    per_page = data.get('per_page', 5)
    
    if not applications:
        await callback.answer(get_text("no_applications", lang))
        return
    
    # Yangi sahifani ko'rsatish
    paginated_apps = paginate_applications(applications, page, per_page)
    
    text = get_text("inbox_welcome", lang)
    text += f"\n\n{get_text('total_applications', lang)}: {len(applications)}"
    text += f"\n{get_text('page', lang)}: {page}/{len(applications) // per_page + 1}"
    
    # Har bir ariza uchun ma'lumot
    for app in paginated_apps:
        status_emoji = {
            'new': '🆕',
            'in_progress': '⏳',
            'completed': '✅',
            'cancelled': '❌',
            'pending': '⏸️',
            'rejected': '🚫'
        }.get(app['status'], '❓')
        
        text += f"\n\n{status_emoji} {get_text('application', lang)} #{app['id']}"
        text += f"\n{get_text('client', lang)}: {app['client_name']}"
        text += f"\n{get_text('type', lang)}: {app['type']}"
        text += f"\n{get_text('status', lang)}: {get_text(f'status_{app['status']}', lang)}"
        text += f"\n{get_text('created_at', lang)}: {app['created_at']}"
    
    # Yangi pagination keyboard
    total_pages = len(applications) // per_page + 1
    pagination_kb = get_pagination_keyboard(page, total_pages, lang)
    
    await callback.message.edit_text(
        text=text,
        reply_markup=pagination_kb
    )
    
    # State'ni yangilash
    await state.update_data({'current_page': page})
    await callback.answer()

@router.callback_query(F.data.startswith("view_app_"))
async def handle_view_application(callback: CallbackQuery, state: FSMContext):
    """Ariza ko'rish handler"""
    app_id = int(callback.data.split("_")[2])
    lang = await get_user_language(callback.from_user.id)
    
    # Ariza ma'lumotlarini olish
    data = await state.get_data()
    applications = data.get('applications', [])
    
    app = next((app for app in applications if app['id'] == app_id), None)
    if not app:
        await callback.answer(get_text("application_not_found", lang))
        return
    
    # Ariza batafsil ma'lumotlari
    text = f"📋 {get_text('application_details', lang)} #{app['id']}\n\n"
    text += f"{get_text('client', lang)}: {app['client_name']}\n"
    text += f"{get_text('type', lang)}: {app['type']}\n"
    text += f"{get_text('status', lang)}: {get_text(f'status_{app['status']}', lang)}\n"
    text += f"{get_text('created_at', lang)}: {app['created_at']}\n"
    text += f"{get_text('description', lang)}: {app.get('description', 'N/A')}\n"
    
    if app.get('assigned_technician'):
        text += f"{get_text('assigned_technician', lang)}: {app['assigned_technician']}\n"
    
    if app.get('priority'):
        text += f"{get_text('priority', lang)}: {get_text(f'priority_{app['priority']}', lang)}\n"
    
    # Action keyboard
    actions_kb = get_application_actions_keyboard(app_id, lang)
    
    await callback.message.edit_text(
        text=text,
        reply_markup=actions_kb
    )
    await callback.answer()

@router.callback_query(F.data.startswith("edit_app_"))
async def handle_edit_application(callback: CallbackQuery, state: FSMContext):
    """Ariza tahrirlash handler"""
    app_id = int(callback.data.split("_")[2])
    lang = await get_user_language(callback.from_user.id)
    
    text = get_text("edit_application_welcome", lang).format(app_id=app_id)
    
    await callback.message.edit_text(
        text=text,
        reply_markup=get_back_keyboard(lang)
    )
    
    await state.set_state("edit_application")
    await state.update_data({'editing_app_id': app_id})
    await callback.answer()

@router.callback_query(F.data.startswith("delete_app_"))
async def handle_delete_application(callback: CallbackQuery, state: FSMContext):
    """Ariza o'chirish handler"""
    app_id = int(callback.data.split("_")[2])
    lang = await get_user_language(callback.from_user.id)
    
    text = get_text("delete_application_confirm", lang).format(app_id=app_id)
    
    from keyboards.manager_new_buttons import get_confirmation_keyboard
    confirm_kb = get_confirmation_keyboard("delete_app", lang)
    
    await callback.message.edit_text(
        text=text,
        reply_markup=confirm_kb
    )
    await callback.answer()