from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.controller_new_buttons import get_back_keyboard, get_pagination_keyboard, get_application_actions_keyboard
from utils.language import get_text
from utils.database import get_user_language, get_manager_inbox_applications
from utils.pagination import paginate_applications

router = Router()

@router.message(F.text == "📥 Inbox")
async def handle_inbox(message: Message, state: FSMContext):
    """Inbox handler for controller"""
    lang = await get_user_language(message.from_user.id)
    
    # Get inbox applications
    applications = await get_manager_inbox_applications()
    
    if not applications:
        text = get_text("no_applications", lang)
        await message.answer(text, reply_markup=get_back_keyboard(lang))
        return
    
    # Paginate applications
    page = 1
    paginated_data = paginate_applications(applications, page, 5)
    
    text = get_text("inbox_applications", lang).format(
        total=len(applications),
        showing=f"{paginated_data['start'] + 1}-{paginated_data['end']}"
    )
    
    # Create keyboard with pagination
    keyboard = get_pagination_keyboard(page, paginated_data['total_pages'], lang)
    
    await message.answer(text, reply_markup=keyboard)
    await state.set_state("inbox")

@router.callback_query(F.data.startswith("page_"))
async def handle_pagination(callback: CallbackQuery, state: FSMContext):
    """Handle pagination for inbox applications"""
    lang = await get_user_language(callback.from_user.id)
    page = int(callback.data.split("_")[1])
    
    applications = await get_manager_inbox_applications()
    paginated_data = paginate_applications(applications, page, 5)
    
    text = get_text("inbox_applications", lang).format(
        total=len(applications),
        showing=f"{paginated_data['start'] + 1}-{paginated_data['end']}"
    )
    
    keyboard = get_pagination_keyboard(page, paginated_data['total_pages'], lang)
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith("view_app_"))
async def handle_view_application(callback: CallbackQuery, state: FSMContext):
    """View application details"""
    lang = await get_user_language(callback.from_user.id)
    application_id = int(callback.data.split("_")[2])
    
    # Get application details from database
    # This would need to be implemented in utils.database
    application = {"id": application_id, "title": "Sample Application"}  # Placeholder
    
    text = get_text("application_details", lang).format(
        id=application["id"],
        title=application["title"]
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