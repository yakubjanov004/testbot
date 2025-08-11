from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.manager_new_buttons import get_back_keyboard, get_export_format_keyboard
from utils.language import get_text
from utils.database import get_user_language, get_manager_export_data
from utils.export import export_to_excel, export_to_pdf, export_to_word

router = Router()

@router.message(F.text == "📤 Export")
async def handle_export(message: Message, state: FSMContext):
    """Export handler"""
    lang = await get_user_language(message.from_user.id)
    text = get_text("export_welcome", lang)
    
    # Export format tanlash keyboard
    format_kb = get_export_format_keyboard(lang)
    
    await message.answer(
        text=text,
        reply_markup=format_kb
    )
    await state.set_state("export")

@router.callback_query(F.data.startswith("export_"))
async def handle_export_format(callback: CallbackQuery, state: FSMContext):
    """Export format tanlash handler"""
    export_format = callback.data.split("_")[1]  # excel, pdf, word
    lang = await get_user_language(callback.from_user.id)
    user_id = callback.from_user.id
    
    await callback.answer(get_text("export_processing", lang))
    
    try:
        # Menejer uchun export ma'lumotlarini olish
        export_data = await get_manager_export_data(user_id)
        
        if not export_data:
            text = get_text("export_no_data", lang)
            await callback.message.edit_text(
                text=text,
                reply_markup=get_back_keyboard(lang)
            )
            return
        
        # Export faylini yaratish
        if export_format == "excel":
            file_path = await export_to_excel(export_data, f"manager_export_{user_id}")
            file_type = "Excel"
        elif export_format == "pdf":
            file_path = await export_to_pdf(export_data, f"manager_export_{user_id}")
            file_type = "PDF"
        elif export_format == "word":
            file_path = await export_to_word(export_data, f"manager_export_{user_id}")
            file_type = "Word"
        else:
            await callback.answer(get_text("export_invalid_format", lang))
            return
        
        # Faylni yuborish
        from aiogram.types import FSInputFile
        
        file = FSInputFile(file_path)
        caption = get_text("export_success", lang).format(
            format=file_type,
            records=len(export_data)
        )
        
        await callback.message.answer_document(
            document=file,
            caption=caption,
            reply_markup=get_back_keyboard(lang)
        )
        
        # Export format keyboard'ni o'chirish
        await callback.message.delete()
        
        # State'ni tozalash
        await state.clear()
        
    except Exception as e:
        error_text = get_text("export_error", lang).format(error=str(e))
        await callback.message.edit_text(
            text=error_text,
            reply_markup=get_back_keyboard(lang)
        )

@router.message(F.text == "◀️ Orqaga")
async def handle_back(message: Message, state: FSMContext):
    """Orqaga qaytish handler"""
    from keyboards.manager_new_buttons import get_manager_main_keyboard
    from handlers.manager_new.main_menu import handle_back as main_back
    
    await main_back(message, state)