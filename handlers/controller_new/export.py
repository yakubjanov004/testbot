from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from keyboards.controller_new_buttons import get_back_keyboard, get_export_format_keyboard
from utils.language import get_text
from utils.database import get_user_language, get_manager_export_data
from utils.export import export_to_excel, export_to_pdf, export_to_word

router = Router()

@router.message(F.text == "📤 Export")
async def handle_export(message: Message, state: FSMContext):
    """Export handler for controller"""
    lang = await get_user_language(message.from_user.id)
    text = get_text("export_format_selection", lang)
    
    await message.answer(
        text=text,
        reply_markup=get_export_format_keyboard(lang)
    )
    await state.set_state("export")

@router.callback_query(F.data.startswith("export_"))
async def handle_export_format(callback: CallbackQuery, state: FSMContext):
    """Handle export format selection"""
    lang = await get_user_language(callback.from_user.id)
    export_format = callback.data.split("_")[1]
    
    try:
        # Get export data
        data = await get_manager_export_data()
        
        if not data:
            text = get_text("no_data_to_export", lang)
            await callback.message.edit_text(text, reply_markup=get_back_keyboard(lang))
            await callback.answer()
            return
        
        # Generate export file based on format
        if export_format == "excel":
            file_path = await export_to_excel(data, "controller_export")
            file = FSInputFile(file_path, filename="controller_export.xlsx")
            caption = get_text("excel_export_success", lang)
        elif export_format == "pdf":
            file_path = await export_to_pdf(data, "controller_export")
            file = FSInputFile(file_path, filename="controller_export.pdf")
            caption = get_text("pdf_export_success", lang)
        elif export_format == "word":
            file_path = await export_to_word(data, "controller_export")
            file = FSInputFile(file_path, filename="controller_export.docx")
            caption = get_text("word_export_success", lang)
        else:
            await callback.answer(get_text("invalid_export_format", lang))
            return
        
        # Send the file
        await callback.message.answer_document(
            document=file,
            caption=caption
        )
        
        # Update the message with success text
        success_text = get_text("export_success", lang).format(format=export_format.upper())
        await callback.message.edit_text(
            success_text,
            reply_markup=get_back_keyboard(lang)
        )
        
        await callback.answer()
        
    except Exception as e:
        error_text = get_text("export_error", lang).format(error=str(e))
        await callback.message.edit_text(
            error_text,
            reply_markup=get_back_keyboard(lang)
        )
        await callback.answer()

@router.message(F.text == "◀️ Orqaga")
async def handle_back(message: Message, state: FSMContext):
    """Back to main menu"""
    from .main_menu import handle_back as main_back
    await main_back(message, state)