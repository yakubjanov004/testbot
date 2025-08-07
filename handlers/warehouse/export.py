from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext
from datetime import datetime
from keyboards.warehouse_buttons import get_warehouse_main_keyboard, export_menu, export_reply_menu
from states.warehouse_states import WarehouseExportStates, WarehouseMainMenuStates
from utils.export_utils import create_export_file, get_available_export_types, get_available_export_formats
from filters.role_filter import RoleFilter

def get_warehouse_export_router():
    """Warehouse export router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("warehouse")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text == "📤 Export")
    async def export_menu_handler(message: Message, state: FSMContext):
        """Export menu handler"""
        try:
            # Debug logging
            print(f"Warehouse export handler called by user {message.from_user.id}")
            
            # Mock user data
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz',
                'role': 'warehouse'
            }
            
            lang = user.get('language', 'uz')
            export_types = get_available_export_types('warehouse')
            
            # Export type names in Uzbek
            export_type_names = {
                'inventory': '📦 Inventarizatsiya',
                'issued_items': '📋 Berilgan materiallar',
                'orders': '📑 Buyurtmalar',
                'statistics': '📊 Statistika'
            }
            
            text = "📤 Export qilish\n\nQaysi ma'lumotlarni export qilmoqchisiz?\n\n"
            text += "Mavjud export turlari:\n"
            for export_type in export_types:
                text += f"• {export_type_names.get(export_type, export_type)}\n"
            
            await message.answer(
                text,
                reply_markup=export_menu(lang, export_types)
            )
            await state.set_state(WarehouseExportStates.exporting_data)
            
            print(f"Warehouse export handler completed successfully")
            
        except Exception as e:
            # print(f"Error in warehouse export handler: {str(e)}")
            # await message.answer("❌ Xatolik yuz berdi")
            pass

    @router.callback_query(F.data.startswith("export_"))
    async def handle_export_selection(callback: CallbackQuery, state: FSMContext):
        """Handle export type selection"""
        try:
            await callback.answer()
            
            export_type = callback.data.replace("export_", "")
            
            # Skip if it's a format or back button
            if export_type in ['back', 'format_csv', 'format_xlsx', 'format_docx', 'format_pdf']:
                return
            
            available_types = get_available_export_types('warehouse')
            
            if export_type not in available_types:
                await callback.message.answer("❌ Noto'g'ri export turi")
                return
            
            # Store selected export type
            await state.update_data(selected_export_type=export_type)
            
            # Export type names in Uzbek
            export_type_names = {
                'inventory': 'Inventarizatsiya',
                'issued_items': 'Berilgan materiallar',
                'orders': 'Buyurtmalar',
                'statistics': 'Statistika'
            }
            
            # Show format selection
            formats = get_available_export_formats()
            text = f"📤 {export_type_names.get(export_type, export_type)} export\n\n"
            text += "Qaysi formatda export qilmoqchisiz?\n\n"
            text += "📄 CSV - Universal format (Excel, Google Sheets)\n"
            text += "📊 Excel - Microsoft Excel formati\n"
            text += "📝 Word - Microsoft Word formati\n"
            text += "📑 PDF - Chop etish uchun qulay format"
            
            keyboard = []
            for fmt in formats:
                format_name = {
                    'csv': '📄 CSV',
                    'xlsx': '📊 Excel',
                    'docx': '📝 Word',
                    'pdf': '📑 PDF'
                }.get(fmt, fmt.upper())
                
                keyboard.append([
                    format_name,
                    f"export_format_{fmt}"
                ])
            
            keyboard.append(["◀️ Orqaga", "export_back"])
            
            from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=btn[0], callback_data=btn[1])]
                for btn in keyboard
            ])
            
            await callback.message.edit_text(text, reply_markup=markup)
            
        except Exception as e:
            print(f"Error in export selection: {str(e)}")
            await callback.message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data.startswith("export_format_"))
    async def handle_export_format(callback: CallbackQuery, state: FSMContext):
        """Handle export format selection"""
        try:
            await callback.answer("📥 Export tayyorlanmoqda...")
            
            format_type = callback.data.replace("export_format_", "")
            data = await state.get_data()
            export_type = data.get('selected_export_type')
            
            if not export_type:
                await callback.message.answer("❌ Export turi tanlanmagan")
                return
            
            # Export type names in Uzbek
            export_type_names = {
                'inventory': 'Inventarizatsiya',
                'issued_items': 'Berilgan materiallar',
                'orders': 'Buyurtmalar',
                'statistics': 'Statistika'
            }
            
            format_names = {
                'csv': 'CSV',
                'xlsx': 'Excel',
                'docx': 'Word',
                'pdf': 'PDF'
            }
            
            # Create export file
            file_content, filename = create_export_file(export_type, format_type)
            
            # Send success message
            await callback.message.answer(
                f"✅ {export_type_names.get(export_type, export_type)} ma'lumotlari {format_names.get(format_type, format_type)} formatida export qilindi!\n\n"
                f"📁 Fayl nomi: {filename}\n"
                f"📊 Fayl hajmi: {len(file_content.read()):,} bayt\n\n"
                f"Fayl yuborilmoqda...",
                reply_markup=get_warehouse_main_keyboard('uz')
            )
            
            # Reset file position
            file_content.seek(0)
            
            # Send the actual file
            await callback.message.answer_document(
                BufferedInputFile(
                    file_content.read(),
                    filename=filename
                ),
                caption=f"📤 {export_type_names.get(export_type, export_type)} export\n"
                        f"📅 Sana: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                        f"📄 Format: {format_names.get(format_type, format_type)}\n\n"
                        f"✅ Export muvaffaqiyatli yakunlandi!"
            )
            
            await state.set_state(WarehouseMainMenuStates.main_menu)
            
        except Exception as e:
            print(f"Error in export format handler: {str(e)}")
            await callback.message.answer("❌ Export xatoligi yuz berdi")

    @router.callback_query(F.data == "warehouse_export_stats")
    async def handle_warehouse_export_stats(callback: CallbackQuery, state: FSMContext):
        """Handle warehouse export stats button"""
        try:
            await callback.answer("📊 Statistika export tayyorlanmoqda...")
            
            from utils.export_utils import create_export_file
            from aiogram.types import BufferedInputFile
            
            # Create export file in CSV format by default
            file_content, filename = create_export_file("statistics", "csv")
            
            # Send success message
            await callback.message.answer(
                "✅ Statistika export tayyor!\n"
                f"📁 Fayl: {filename}\n"
                f"📊 Fayl hajmi: {len(file_content.read()):,} bayt"
            )
            
            # Reset file position
            file_content.seek(0)
            
            # Send the actual file
            await callback.message.answer_document(
                BufferedInputFile(
                    file_content.read(),
                    filename=filename
                ),
                caption=f"📤 Statistika export\n"
                        f"📅 Sana: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                        f"📄 Format: CSV\n\n"
                        f"✅ Export muvaffaqiyatli yakunlandi!"
            )
            
        except Exception as e:
            print(f"Error in stats export: {str(e)}")
            await callback.message.answer("❌ Export xatoligi yuz berdi")

    @router.callback_query(F.data == "warehouse_back")
    async def handle_warehouse_back(callback: CallbackQuery, state: FSMContext):
        """Handle warehouse back button"""
        try:
            await callback.answer()
            
            # Return to warehouse main menu
            await callback.message.answer("Ombor bosh menyusi", reply_markup=get_warehouse_main_keyboard('uz'))
            await state.set_state(WarehouseMainMenuStates.main_menu)
            
        except Exception as e:
            await callback.message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "export_back")
    async def handle_export_back(callback: CallbackQuery, state: FSMContext):
        """Handle export back button"""
        try:
            await callback.answer()
            
            # Return to main export menu
            await export_menu_handler(callback.message, state)
            
        except Exception as e:
            await callback.message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text == "◀️ Orqaga")
    async def export_back_handler(message: Message, state: FSMContext):
        """Export back handler"""
        try:
            # Mock user data
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            lang = user.get('language', 'uz')
            await message.answer("Ombor bosh menyusi", reply_markup=get_warehouse_main_keyboard(lang))
            await state.set_state(WarehouseMainMenuStates.main_menu)
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    return router
