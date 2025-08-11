from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.controller_new_buttons import get_controller_main_keyboard, get_back_keyboard
from utils.language import get_text
from utils.database import get_user_language

router = Router()

@router.message(F.text == "📥 Inbox")
async def handle_inbox(message: Message, state: FSMContext):
    """Inbox handler"""
    lang = await get_user_language(message.from_user.id)
    text = get_text("inbox_welcome", lang)
    
    await message.answer(
        text=text,
        reply_markup=get_back_keyboard(lang)
    )
    await state.set_state("inbox")

@router.message(F.text == "📋 Arizalarni ko'rish")
async def handle_view_applications(message: Message, state: FSMContext):
    """Arizalarni ko'rish handler"""
    lang = await get_user_language(message.from_user.id)
    text = get_text("view_applications_welcome", lang)
    
    await message.answer(
        text=text,
        reply_markup=get_back_keyboard(lang)
    )
    await state.set_state("view_applications")

@router.message(F.text == "🔌 Ulanish arizasi yaratish")
async def handle_create_connection(message: Message, state: FSMContext):
    """Ulanish arizasi yaratish handler"""
    lang = await get_user_language(message.from_user.id)
    text = get_text("create_connection_welcome", lang)
    
    await message.answer(
        text=text,
        reply_markup=get_back_keyboard(lang)
    )
    await state.set_state("create_connection")

@router.message(F.text == "🔧 Texnik xizmat yaratish")
async def handle_create_technical(message: Message, state: FSMContext):
    """Texnik xizmat yaratish handler"""
    lang = await get_user_language(message.from_user.id)
    text = get_text("create_technical_welcome", lang)
    
    await message.answer(
        text=text,
        reply_markup=get_back_keyboard(lang)
    )
    await state.set_state("create_technical")

@router.message(F.text == "🕐 Real vaqtda kuzatish")
async def handle_realtime_monitoring(message: Message, state: FSMContext):
    """Real vaqtda kuzatish handler"""
    lang = await get_user_language(message.from_user.id)
    text = get_text("realtime_monitoring_welcome", lang)
    
    await message.answer(
        text=text,
        reply_markup=get_back_keyboard(lang)
    )
    await state.set_state("realtime_monitoring")

@router.message(F.text == "📊 Monitoring")
async def handle_monitoring(message: Message, state: FSMContext):
    """Monitoring handler"""
    lang = await get_user_language(message.from_user.id)
    text = get_text("monitoring_welcome", lang)
    
    await message.answer(
        text=text,
        reply_markup=get_back_keyboard(lang)
    )
    await state.set_state("monitoring")

@router.message(F.text == "👥 Xodimlar faoliyati")
async def handle_staff_activity(message: Message, state: FSMContext):
    """Xodimlar faoliyati handler (faqat texniklar uchun)"""
    lang = await get_user_language(message.from_user.id)
    text = get_text("staff_activity_welcome", lang)
    
    await message.answer(
        text=text,
        reply_markup=get_back_keyboard(lang)
    )
    await state.set_state("staff_activity")

@router.message(F.text == "📤 Export")
async def handle_export(message: Message, state: FSMContext):
    """Export handler"""
    lang = await get_user_language(message.from_user.id)
    text = get_text("export_welcome", lang)
    
    await message.answer(
        text=text,
        reply_markup=get_back_keyboard(lang)
    )
    await state.set_state("export")

@router.message(F.text == "🌐 Tilni o'zgartirish")
async def handle_language_change(message: Message, state: FSMContext):
    """Tilni o'zgartirish handler"""
    lang = await get_user_language(message.from_user.id)
    text = get_text("language_change_welcome", lang)
    
    await message.answer(
        text=text,
        reply_markup=get_back_keyboard(lang)
    )
    await state.set_state("language_change")

@router.message(F.text == "◀️ Orqaga")
async def handle_back(message: Message, state: FSMContext):
    """Orqaga qaytish handler"""
    lang = await get_user_language(message.from_user.id)
    text = get_text("back_to_main_menu", lang)
    
    await message.answer(
        text=text,
        reply_markup=get_controller_main_keyboard(lang)
    )
    await state.clear()