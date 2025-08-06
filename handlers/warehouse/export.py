from aiogram import F
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext
import csv
import io
from datetime import datetime
from keyboards.warehouse_buttons import warehouse_main_menu, export_menu, export_reply_menu
from states.warehouse_states import WarehouseExportStates, WarehouseMainMenuStates

def get_warehouse_export_router():
    """Warehouse export router"""
    from utils.role_system import get_role_router
    router = get_role_router("warehouse")

    @router.message(F.text == "📤 Export")
    async def export_menu_handler(message: Message, state: FSMContext):
        """Export menu handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz',
                'role': 'warehouse'
            }
            
            lang = user.get('language', 'uz')
            await message.answer(
                "Qaysi formatda eksport qilmoqchisiz?",
                reply_markup=export_reply_menu(lang)
            )
            await state.set_state(WarehouseExportStates.exporting_data)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text == "Excelga export")
    async def export_excel_handler(message: Message, state: FSMContext):
        """Export to Excel handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            lang = user.get('language', 'uz')
            await message.answer("Excelga eksport qilish funksiyasi tez orada qo'shiladi.", reply_markup=export_reply_menu(lang))
            await state.set_state(WarehouseExportStates.exporting_data)
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    @router.message(F.text == "PDFga export")
    async def export_pdf_handler(message: Message, state: FSMContext):
        """Export to PDF handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            lang = user.get('language', 'uz')
            await message.answer("PDFga eksport qilish funksiyasi tez orada qo'shiladi.", reply_markup=export_reply_menu(lang))
            await state.set_state(WarehouseExportStates.exporting_data)
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    @router.message(F.text == "Wordga export")
    async def export_word_handler(message: Message, state: FSMContext):
        """Export to Word handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            lang = user.get('language', 'uz')
            await message.answer("Wordga eksport qilish funksiyasi tez orada qo'shiladi.", reply_markup=export_reply_menu(lang))
            await state.set_state(WarehouseExportStates.exporting_data)
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    @router.message(F.text == "◀️ Orqaga")
    async def export_back_handler(message: Message, state: FSMContext):
        """Export back handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            lang = user.get('language', 'uz')
            await message.answer("Ombor bosh menyusi", reply_markup=warehouse_main_menu(lang))
            await state.set_state(WarehouseMainMenuStates.main_menu)
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    @router.message(F.text == "📤 Export")
    async def export_handler(message: Message, state: FSMContext):
        """Handle data export"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz',
                'role': 'warehouse'
            }
            
            lang = user.get('language', 'uz')
            export_text = "📤 Ma'lumotlarni eksport qilish"
            
            await message.answer(
                export_text,
                reply_markup=warehouse_main_menu(lang)
            )
            await state.set_state(WarehouseExportStates.export_menu)
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "export_inventory")
    async def export_inventory_handler(callback: CallbackQuery, state: FSMContext):
        """Export inventory data to CSV"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            lang = user.get('language', 'uz')
            
            # Show processing message
            processing_text = "⏳ Ma'lumotlar tayyorlanmoqda..."
            await callback.message.edit_text(processing_text)
            
            # Mock inventory data (like other modules)
            inventory_data = [
                {
                    'id': 1,
                    'name': 'Cable',
                    'category': 'Electronics',
                    'quantity': 50,
                    'unit': 'metr',
                    'min_quantity': 10,
                    'price': 5000,
                    'description': 'Test cable',
                    'created_at': datetime.now(),
                    'updated_at': datetime.now()
                },
                {
                    'id': 2,
                    'name': 'Router',
                    'category': 'Networking',
                    'quantity': 5,
                    'unit': 'dona',
                    'min_quantity': 2,
                    'price': 150000,
                    'description': 'Test router',
                    'created_at': datetime.now(),
                    'updated_at': datetime.now()
                },
                {
                    'id': 3,
                    'name': 'Connector',
                    'category': 'Electronics',
                    'quantity': 100,
                    'unit': 'dona',
                    'min_quantity': 20,
                    'price': 500,
                    'description': 'Test connector',
                    'created_at': datetime.now(),
                    'updated_at': datetime.now()
                }
            ]
            
            if inventory_data:
                # Create CSV content
                output = io.StringIO()
                
                # CSV headers
                fieldnames = ['ID', 'Nomi', 'Kategoriya', 'Miqdor', 'Birlik', 'Min_miqdor', 'Narx', 'Tavsif', 'Yaratilgan', 'Yangilangan']
                
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()
                
                # Write data rows
                for item in inventory_data:
                    row_data = {
                        fieldnames[0]: item['id'],
                        fieldnames[1]: item['name'],
                        fieldnames[2]: item.get('category', ''),
                        fieldnames[3]: item['quantity'],
                        fieldnames[4]: item.get('unit', 'dona'),
                        fieldnames[5]: item.get('min_quantity', 0),
                        fieldnames[6]: item.get('price', 0),
                        fieldnames[7]: item.get('description', ''),
                        fieldnames[8]: item['created_at'].strftime('%Y-%m-%d %H:%M:%S') if item.get('created_at') else '',
                        fieldnames[9]: item['updated_at'].strftime('%Y-%m-%d %H:%M:%S') if item.get('updated_at') else ''
                    }
                    writer.writerow(row_data)
                
                # Create file
                csv_content = output.getvalue().encode('utf-8-sig')  # UTF-8 with BOM for Excel compatibility
                output.close()
                
                # Generate filename
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"inventory_export_{timestamp}.csv"
                
                # Send file
                file = BufferedInputFile(csv_content, filename=filename)
                
                success_text = f"✅ Inventar ma'lumotlari eksport qilindi!\n📊 Jami: {len(inventory_data)} ta mahsulot"
                
                await callback.message.answer_document(
                    document=file,
                    caption=success_text
                )
            else:
                error_text = "❌ Eksport qilinadigan ma'lumotlar yo'q"
                await callback.message.edit_text(error_text)
            
            await callback.answer()
            
        except Exception as e:
            await callback.message.edit_text("Eksport qilishda xatolik")
            await callback.answer()

    @router.callback_query(F.data == "export_orders")
    async def export_orders_handler(callback: CallbackQuery, state: FSMContext):
        """Export orders data to CSV"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            lang = user.get('language', 'uz')
            
            # Show processing message
            processing_text = "⏳ Ma'lumotlar tayyorlanmoqda..."
            await callback.message.edit_text(processing_text)
            
            # Mock orders data (like other modules)
            orders_data = [
                {
                    'id': 'WH001',
                    'description': 'Test order 1',
                    'status': 'completed',
                    'client_name': 'Test Client 1',
                    'client_phone': '+998901234567',
                    'technician_name': 'Test Technician',
                    'created_at': datetime.now(),
                    'completed_at': datetime.now()
                },
                {
                    'id': 'WH002',
                    'description': 'Test order 2',
                    'status': 'in_progress',
                    'client_name': 'Test Client 2',
                    'client_phone': '+998901234568',
                    'technician_name': 'Test Technician 2',
                    'created_at': datetime.now(),
                    'completed_at': None
                }
            ]
            
            if orders_data:
                # Create CSV content
                output = io.StringIO()
                
                # CSV headers
                fieldnames = ['ID', 'Tavsif', 'Holat', 'Mijoz', 'Telefon', 'Texnik', 'Yaratilgan', 'Tugallangan']
                
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()
                
                # Write data rows
                for order in orders_data:
                    row_data = {
                        fieldnames[0]: order['id'],
                        fieldnames[1]: order.get('description', ''),
                        fieldnames[2]: order.get('status', ''),
                        fieldnames[3]: order.get('client_name', ''),
                        fieldnames[4]: order.get('client_phone', ''),
                        fieldnames[5]: order.get('technician_name', ''),
                        fieldnames[6]: order['created_at'].strftime('%Y-%m-%d %H:%M:%S') if order.get('created_at') else '',
                        fieldnames[7]: order['completed_at'].strftime('%Y-%m-%d %H:%M:%S') if order.get('completed_at') else ''
                    }
                    writer.writerow(row_data)
                
                # Create file
                csv_content = output.getvalue().encode('utf-8-sig')
                output.close()
                
                # Generate filename
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"orders_export_{timestamp}.csv"
                
                # Send file
                file = BufferedInputFile(csv_content, filename=filename)
                
                success_text = f"✅ Buyurtmalar ma'lumotlari eksport qilindi!\n📊 Jami: {len(orders_data)} ta buyurtma"
                
                await callback.message.answer_document(
                    document=file,
                    caption=success_text
                )
            else:
                error_text = "❌ Eksport qilinadigan buyurtmalar yo'q"
                await callback.message.edit_text(error_text)
            
            await callback.answer()
            
        except Exception as e:
            await callback.message.edit_text("Eksport qilishda xatolik")
            await callback.answer()

    @router.callback_query(F.data == "export_issued_items")
    async def export_issued_items_handler(callback: CallbackQuery, state: FSMContext):
        """Export issued items data to CSV"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            lang = user.get('language', 'uz')
            
            # Show processing message
            processing_text = "⏳ Ma'lumotlar tayyorlanmoqda..."
            await callback.message.edit_text(processing_text)
            
            # Mock issued items data (like other modules)
            issued_data = [
                {
                    'id': 1,
                    'material_name': 'Cable',
                    'category': 'Electronics',
                    'quantity': 10,
                    'issued_by_name': 'Warehouse xodimi',
                    'order_id': 'WH001',
                    'order_description': 'Test order 1',
                    'issued_at': datetime.now()
                },
                {
                    'id': 2,
                    'material_name': 'Router',
                    'category': 'Networking',
                    'quantity': 1,
                    'issued_by_name': 'Warehouse xodimi',
                    'order_id': 'WH002',
                    'order_description': 'Test order 2',
                    'issued_at': datetime.now()
                }
            ]
            
            if issued_data:
                # Create CSV content
                output = io.StringIO()
                
                # CSV headers
                fieldnames = ['ID', 'Mahsulot', 'Kategoriya', 'Miqdor', 'Beruvchi', 'Buyurtma_ID', 'Buyurtma_tavsif', 'Berilgan_vaqt']
                
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()
                
                # Write data rows
                for item in issued_data:
                    row_data = {
                        fieldnames[0]: item['id'],
                        fieldnames[1]: item.get('material_name', ''),
                        fieldnames[2]: item.get('category', ''),
                        fieldnames[3]: item.get('quantity', 0),
                        fieldnames[4]: item.get('issued_by_name', ''),
                        fieldnames[5]: item.get('order_id', ''),
                        fieldnames[6]: item.get('order_description', ''),
                        fieldnames[7]: item['issued_at'].strftime('%Y-%m-%d %H:%M:%S') if item.get('issued_at') else ''
                    }
                    writer.writerow(row_data)
                
                # Create file
                csv_content = output.getvalue().encode('utf-8-sig')
                output.close()
                
                # Generate filename
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"issued_items_export_{timestamp}.csv"
                
                # Send file
                file = BufferedInputFile(csv_content, filename=filename)
                
                success_text = f"✅ Chiqarilgan mahsulotlar ma'lumotlari eksport qilindi!\n📊 Jami: {len(issued_data)} ta yozuv"
                
                await callback.message.answer_document(
                    document=file,
                    caption=success_text
                )
            else:
                error_text = "❌ Eksport qilinadigan ma'lumotlar yo'q"
                await callback.message.edit_text(error_text)
            
            await callback.answer()
            
        except Exception as e:
            await callback.message.edit_text("Eksport qilishda xatolik")
            await callback.answer()

    @router.callback_query(F.data == "export_full_report")
    async def export_full_report_handler(callback: CallbackQuery, state: FSMContext):
        """Export full warehouse report"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            lang = user.get('language', 'uz')
            
            # Show processing message
            processing_text = "⏳ To'liq hisobot tayyorlanmoqda..."
            await callback.message.edit_text(processing_text)
            
            # Mock data (like other modules)
            inventory_data = [
                {
                    'id': 1,
                    'name': 'Cable',
                    'quantity': 50,
                    'price': 5000
                },
                {
                    'id': 2,
                    'name': 'Router',
                    'quantity': 5,
                    'price': 150000
                }
            ]
            
            orders_data = [
                {
                    'id': 'WH001',
                    'status': 'completed'
                },
                {
                    'id': 'WH002',
                    'status': 'in_progress'
                }
            ]
            
            issued_data = [
                {
                    'id': 1,
                    'material_name': 'Cable',
                    'quantity': 10
                },
                {
                    'id': 2,
                    'material_name': 'Router',
                    'quantity': 1
                }
            ]
            
            # Create comprehensive report
            output = io.StringIO()
            
            # Write summary
            output.write("WAREHOUSE FULL REPORT\n")
            output.write("=" * 50 + "\n")
            output.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            output.write(f"Generated by: {user.get('full_name', 'Unknown')}\n\n")
            
            # Summary statistics
            output.write("SUMMARY STATISTICS\n")
            output.write("-" * 30 + "\n")
            output.write(f"Total Inventory Items: {len(inventory_data)}\n")
            output.write(f"Total Orders: {len(orders_data)}\n")
            output.write(f"Total Issued Items: {len(issued_data)}\n\n")
            
            # Inventory summary
            if inventory_data:
                total_value = sum(item.get('price', 0) * item.get('quantity', 0) for item in inventory_data)
                low_stock_count = sum(1 for item in inventory_data if item.get('quantity', 0) <= 10)
                
                output.write("INVENTORY SUMMARY\n")
                output.write("-" * 30 + "\n")
                output.write(f"Total Inventory Value: {total_value:,.0f} UZS\n")
                output.write(f"Low Stock Items: {low_stock_count}\n")
                output.write(f"Out of Stock Items: {sum(1 for item in inventory_data if item.get('quantity', 0) == 0)}\n\n")
            
            # Orders summary
            if orders_data:
                status_counts = {}
                for order in orders_data:
                    status = order.get('status', 'unknown')
                    status_counts[status] = status_counts.get(status, 0) + 1
                
                output.write("ORDERS SUMMARY\n")
                output.write("-" * 30 + "\n")
                for status, count in status_counts.items():
                    output.write(f"{status.title()}: {count}\n")
                output.write("\n")
            
            # Create file
            report_content = output.getvalue().encode('utf-8-sig')
            output.close()
            
            # Generate filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"warehouse_full_report_{timestamp}.txt"
            
            # Send file
            file = BufferedInputFile(report_content, filename=filename)
            
            success_text = f"✅ To'liq hisobot tayyor!\n📊 Inventar: {len(inventory_data)}\n📋 Buyurtmalar: {len(orders_data)}\n📤 Chiqarilgan: {len(issued_data)}"
            
            await callback.message.answer_document(
                document=file,
                caption=success_text
            )
            
            await callback.answer()
            
        except Exception as e:
            await callback.message.edit_text("Hisobotni eksport qilishda xatolik")
            await callback.answer()

    return router

# Mock functions (like other modules)
async def get_inventory_export_data():
    """Get inventory export data (mock function like other modules)"""
    try:
        return [
            {
                'id': 1,
                'name': 'Cable',
                'category': 'Electronics',
                'quantity': 50,
                'unit': 'metr',
                'min_quantity': 10,
                'price': 5000,
                'description': 'Test cable',
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'id': 2,
                'name': 'Router',
                'category': 'Networking',
                'quantity': 5,
                'unit': 'dona',
                'min_quantity': 2,
                'price': 150000,
                'description': 'Test router',
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
        ]
    except Exception as e:
        return []

async def get_orders_export_data():
    """Get orders export data (mock function like other modules)"""
    try:
        return [
            {
                'id': 'WH001',
                'description': 'Test order 1',
                'status': 'completed',
                'client_name': 'Test Client 1',
                'client_phone': '+998901234567',
                'technician_name': 'Test Technician',
                'created_at': datetime.now(),
                'completed_at': datetime.now()
            },
            {
                'id': 'WH002',
                'description': 'Test order 2',
                'status': 'in_progress',
                'client_name': 'Test Client 2',
                'client_phone': '+998901234568',
                'technician_name': 'Test Technician 2',
                'created_at': datetime.now(),
                'completed_at': None
            }
        ]
    except Exception as e:
        return []

async def get_issued_items_export_data():
    """Get issued items export data (mock function like other modules)"""
    try:
        return [
            {
                'id': 1,
                'material_name': 'Cable',
                'category': 'Electronics',
                'quantity': 10,
                'issued_by_name': 'Warehouse xodimi',
                'order_id': 'WH001',
                'order_description': 'Test order 1',
                'issued_at': datetime.now()
            },
            {
                'id': 2,
                'material_name': 'Router',
                'category': 'Networking',
                'quantity': 1,
                'issued_by_name': 'Warehouse xodimi',
                'order_id': 'WH002',
                'order_description': 'Test order 2',
                'issued_at': datetime.now()
            }
        ]
    except Exception as e:
        return []
