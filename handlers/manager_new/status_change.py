from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.manager_new_buttons import get_back_keyboard, get_status_keyboard, get_confirmation_keyboard
from utils.language import get_text
from utils.database import get_user_language, get_manager_applications, update_application_status
from aiogram.fsm.state import State, StatesGroup

router = Router()

class StatusChangeStates(StatesGroup):
    waiting_for_app_id = State()
    waiting_for_status = State()
    waiting_for_confirmation = State()

@router.message(F.text == "🔄 Status o'zgartirish")
async def handle_status_change(message: Message, state: FSMContext):
    """Status o'zgartirish handler"""
    lang = await get_user_language(message.from_user.id)
    user_id = message.from_user.id
    
    # Menejer uchun arizalarni olish
    applications = await get_manager_applications(user_id)
    
    if not applications:
        text = get_text("status_change_no_applications", lang)
        await message.answer(text, reply_markup=get_back_keyboard(lang))
        return
    
    # Arizalarni ko'rsatish
    text = get_text("status_change_welcome", lang)
    text += f"\n\n{get_text('select_application', lang)}:"
    
    for app in applications[:10]:  # Faqat 10 ta ariza
        status_emoji = {
            'new': '🆕',
            'in_progress': '⏳',
            'completed': '✅',
            'cancelled': '❌',
            'pending': '⏸️',
            'rejected': '🚫'
        }.get(app['status'], '❓')
        
        text += f"\n{status_emoji} #{app['id']} - {app['client_name']} ({get_text(f'status_{app['status']}', lang)})"
    
    if len(applications) > 10:
        text += f"\n\n... va {len(applications) - 10} ta boshqa ariza"
    
    text += f"\n\n{get_text('enter_application_id', lang)}"
    
    await message.answer(
        text=text,
        reply_markup=get_back_keyboard(lang)
    )
    
    await state.set_state(StatusChangeStates.waiting_for_app_id)
    await state.update_data({'applications': applications})

@router.message(StatusChangeStates.waiting_for_app_id)
async def handle_app_id_input(message: Message, state: FSMContext):
    """Ariza ID kiritish handler"""
    lang = await get_user_language(message.from_user.id)
    
    try:
        app_id = int(message.text)
    except ValueError:
        text = get_text("invalid_application_id", lang)
        await message.answer(text)
        return
    
    # Ariza mavjudligini tekshirish
    data = await state.get_data()
    applications = data.get('applications', [])
    
    app = next((app for app in applications if app['id'] == app_id), None)
    if not app:
        text = get_text("application_not_found", lang)
        await message.answer(text)
        return
    
    # Ariza ma'lumotlarini ko'rsatish
    text = f"📋 {get_text('application_details', lang)} #{app_id}\n\n"
    text += f"{get_text('client', lang)}: {app['client_name']}\n"
    text += f"{get_text('type', lang)}: {app['type']}\n"
    text += f"{get_text('current_status', lang)}: {get_text(f'status_{app['status']}', lang)}\n"
    text += f"{get_text('created_at', lang)}: {app['created_at']}\n"
    
    if app.get('description'):
        text += f"{get_text('description', lang)}: {app['description']}\n"
    
    # Status tanlash keyboard
    available_statuses = ['new', 'in_progress', 'completed', 'cancelled', 'pending', 'rejected']
    status_kb = get_status_keyboard(available_statuses, app_id, lang)
    
    await message.answer(
        text=text,
        reply_markup=status_kb
    )
    
    await state.set_state(StatusChangeStates.waiting_for_status)
    await state.update_data({'selected_app_id': app_id, 'selected_app': app})

@router.callback_query(F.data.startswith("status_"))
async def handle_status_selection(callback: CallbackQuery, state: FSMContext):
    """Status tanlash handler"""
    parts = callback.data.split("_")
    if len(parts) < 3:
        await callback.answer("Invalid callback data")
        return
    
    new_status = parts[1]
    app_id = int(parts[2])
    lang = await get_user_language(callback.from_user.id)
    
    # State'dan ma'lumotlarni olish
    data = await state.get_data()
    selected_app = data.get('selected_app')
    
    if not selected_app or selected_app['id'] != app_id:
        await callback.answer(get_text("application_not_found", lang))
        return
    
    current_status = selected_app['status']
    
    if new_status == current_status:
        await callback.answer(get_text("status_already_set", lang))
        return
    
    # Status o'zgarishini tasdiqlash
    text = get_text("status_change_confirm", lang).format(
        app_id=app_id,
        old_status=get_text(f'status_{current_status}', lang),
        new_status=get_text(f'status_{new_status}', lang)
    )
    
    confirm_kb = get_confirmation_keyboard("status_change", lang)
    
    await callback.message.edit_text(
        text=text,
        reply_markup=confirm_kb
    )
    
    await state.set_state(StatusChangeStates.waiting_for_confirmation)
    await state.update_data({'new_status': new_status})
    await callback.answer()

@router.callback_query(F.data == "status_change_yes")
async def handle_status_confirmation(callback: CallbackQuery, state: FSMContext):
    """Status o'zgarishini tasdiqlash handler"""
    lang = await get_user_language(callback.from_user.id)
    data = await state.get_data()
    
    app_id = data.get('selected_app_id')
    new_status = data.get('new_status')
    
    if not app_id or not new_status:
        await callback.answer(get_text("invalid_data", lang))
        return
    
    try:
        # Status o'zgartirish
        await update_application_status(app_id, new_status)
        
        success_text = get_text("status_change_success", lang).format(
            app_id=app_id,
            new_status=get_text(f'status_{new_status}', lang)
        )
        
        await callback.message.edit_text(
            text=success_text,
            reply_markup=get_back_keyboard(lang)
        )
        
        # State'ni tozalash
        await state.clear()
        
    except Exception as e:
        error_text = get_text("status_change_error", lang).format(error=str(e))
        await callback.message.edit_text(
            text=error_text,
            reply_markup=get_back_keyboard(lang)
        )
    
    await callback.answer()

@router.callback_query(F.data == "status_change_no")
async def handle_status_cancel(callback: CallbackQuery, state: FSMContext):
    """Status o'zgarishini bekor qilish handler"""
    lang = await get_user_language(callback.from_user.id)
    
    text = get_text("status_change_cancelled", lang)
    
    await callback.message.edit_text(
        text=text,
        reply_markup=get_back_keyboard(lang)
    )
    
    await state.clear()
    await callback.answer()

@router.message(F.text == "◀️ Orqaga")
async def handle_back(message: Message, state: FSMContext):
    """Orqaga qaytish handler"""
    from keyboards.manager_new_buttons import get_manager_main_keyboard
    from handlers.manager_new.main_menu import handle_back as main_back
    
    await main_back(message, state)