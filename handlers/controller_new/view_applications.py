from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.controller_new_buttons import get_back_keyboard, get_pagination_keyboard, get_application_actions_keyboard
from utils.language import get_text
from utils.database import get_user_language, get_all_applications
from utils.pagination import paginate_applications

router = Router()

@router.message(F.text == "📋 Arizalarni ko'rish")
async def handle_view_applications(message: Message, state: FSMContext):
    """Arizalarni ko'rish handler for controller (hamma arizalarni ko'rsatadi)"""
    lang = await get_user_language(message.from_user.id)
    
    # Get all applications
    applications = await get_all_applications()
    
    if not applications:
        text = get_text("no_applications", lang)
        await message.answer(text, reply_markup=get_back_keyboard(lang))
        return
    
    # Paginate applications
    page = 1
    paginated_data = paginate_applications(applications, page, 5)
    
    text = get_text("all_applications_header", lang).format(
        total=len(applications),
        showing=f"{paginated_data['start'] + 1}-{paginated_data['end']}"
    ) + "\n\n"
    
    # Display applications in current page
    for app in paginated_data['items']:
        text += get_text("application_summary_format", lang).format(
            id=app.get('id', 'N/A'),
            title=app.get('title', 'N/A'),
            status=app.get('status', 'N/A'),
            priority=app.get('priority', 'N/A'),
            created_date=app.get('created_date', 'N/A'),
            assigned_to=app.get('assigned_to', get_text("unassigned", lang))
        ) + "\n\n"
    
    # Create keyboard with pagination
    keyboard = get_pagination_keyboard(page, paginated_data['total_pages'], lang)
    
    await message.answer(text, reply_markup=keyboard)
    await state.set_state("view_applications")

@router.callback_query(F.data.startswith("page_"))
async def handle_pagination(callback: CallbackQuery, state: FSMContext):
    """Handle pagination for applications"""
    lang = await get_user_language(callback.from_user.id)
    page = int(callback.data.split("_")[1])
    
    applications = await get_all_applications()
    paginated_data = paginate_applications(applications, page, 5)
    
    text = get_text("all_applications_header", lang).format(
        total=len(applications),
        showing=f"{paginated_data['start'] + 1}-{paginated_data['end']}"
    ) + "\n\n"
    
    for app in paginated_data['items']:
        text += get_text("application_summary_format", lang).format(
            id=app.get('id', 'N/A'),
            title=app.get('title', 'N/A'),
            status=app.get('status', 'N/A'),
            priority=app.get('priority', 'N/A'),
            created_date=app.get('created_date', 'N/A'),
            assigned_to=app.get('assigned_to', get_text("unassigned", lang))
        ) + "\n\n"
    
    keyboard = get_pagination_keyboard(page, paginated_data['total_pages'], lang)
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith("view_app_"))
async def handle_view_application(callback: CallbackQuery, state: FSMContext):
    """View detailed application information"""
    lang = await get_user_language(callback.from_user.id)
    application_id = int(callback.data.split("_")[2])
    
    # Get detailed application information
    # This would need to be implemented in utils.database
    application = {"id": application_id, "title": "Sample Application"}  # Placeholder
    
    text = get_text("application_details_full", lang).format(
        id=application["id"],
        title=application["title"],
        description=application.get("description", "N/A"),
        status=application.get("status", "N/A"),
        priority=application.get("priority", "N/A"),
        created_date=application.get("created_date", "N/A"),
        assigned_to=application.get("assigned_to", get_text("unassigned", lang)),
        estimated_time=application.get("estimated_time", "N/A"),
        actual_time=application.get("actual_time", "N/A")
    )
    
    keyboard = get_application_actions_keyboard(application_id, lang)
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith("edit_app_"))
async def handle_edit_application(callback: CallbackQuery, state: FSMContext):
    """Edit application handler"""
    lang = await get_user_language(callback.from_user.id)
    application_id = int(callback.data.split("_")[2])
    
    text = get_text("edit_application", lang).format(id=application_id)
    
    await callback.message.edit_text(text, reply_markup=get_back_keyboard(lang))
    await callback.answer()
    await state.set_state("edit_application")

@router.callback_query(F.data.startswith("delete_app_"))
async def handle_delete_application(callback: CallbackQuery, state: FSMContext):
    """Delete application handler"""
    lang = await get_user_language(callback.from_user.id)
    application_id = int(callback.data.split("_")[2])
    
    text = get_text("delete_application_confirm", lang).format(id=application_id)
    
    await callback.message.edit_text(text, reply_markup=get_back_keyboard(lang))
    await callback.answer()
    await state.set_state("delete_application")

@router.message(F.text == "◀️ Orqaga")
async def handle_back(message: Message, state: FSMContext):
    """Back to main menu"""
    from .main_menu import handle_back as main_back
    await main_back(message, state)