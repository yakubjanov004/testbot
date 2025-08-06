import json
import html
from typing import List, Dict
from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from states.warehouse_states import WarehouseWorkflowStates
from filters.role_filter import RoleFilter

class WarehouseWorkflowFSM(StatesGroup):
    viewing_request = State()
    entering_return_reason = State()
    preparing_equipment = State()

def get_warehouse_inbox_router():
    """Warehouse inbox router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("warehouse")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)
    
    @router.callback_query(F.data.startswith("open_inbox_"))
    async def handle_inbox_notification(callback: CallbackQuery, state: FSMContext):
        """Handle inbox notification button click"""
        try:
            await callback.answer()
            
            # Extract request ID
            request_id_short = callback.data.replace("open_inbox_", "")
            
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz',
                'role': 'warehouse'
            }
            
            # Show inbox
            await show_warehouse_inbox_from_notification(callback.message, state, request_id_short)
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")
    
    async def show_warehouse_inbox_from_notification(message: Message, state: FSMContext, target_request_id: str = None):
        """Show warehouse inbox with focus on specific request"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz',
                'role': 'warehouse'
            }
            
            lang = user.get('language', 'uz')
            
            # Mock inbox messages (like other modules)
            inbox_messages = [
                {
                    'id': 1,
                    'application_id': 'WH001',
                    'message': 'Test message 1'
                },
                {
                    'id': 2,
                    'application_id': 'WH002',
                    'message': 'Test message 2'
                }
            ]
            
            if not inbox_messages:
                text = "📭 Inbox bo'sh"
                await message.answer(text)
                return
            
            # Find target request index if specified
            target_index = 0
            if target_request_id:
                for i, msg in enumerate(inbox_messages):
                    if msg['application_id'].startswith(target_request_id):
                        target_index = i
                        break
            
            # Mock requests data (like other modules)
            requests = [
                {
                    'id': 'WH001',
                    'client_name': 'Test Client 1',
                    'description': 'Test description 1',
                    'created_at': datetime.now(),
                    'materials': [
                        {'name': 'Cable', 'quantity': 2, 'unit': 'dona'},
                        {'name': 'Router', 'quantity': 1, 'unit': 'dona'}
                    ],
                    'inbox_message': inbox_messages[0]
                },
                {
                    'id': 'WH002',
                    'client_name': 'Test Client 2',
                    'description': 'Test description 2',
                    'created_at': datetime.now(),
                    'materials': [
                        {'name': 'Connector', 'quantity': 5, 'unit': 'dona'}
                    ],
                    'inbox_message': inbox_messages[1]
                }
            ]
            
            if not requests:
                text = "📭 Inbox bo'sh"
                await message.answer(text)
                return
            
            await state.update_data(
                warehouse_requests=requests,
                current_index=target_index
            )
            
            # Display the targeted request
            await display_warehouse_request(message, state, requests, target_index, lang)
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    @router.message(F.text == "📥 Inbox")
    async def show_warehouse_inbox(message: Message, state: FSMContext):
        """Show warehouse inbox with all warehouse-related requests"""
        try:
            # Debug logging
            print(f"Warehouse inbox handler called by user {message.from_user.id}")
            
            # Check user role first - only process if user is warehouse
            # from loader import get_user_role
            # user_role = get_user_role(message.from_user.id)
            # if user_role != 'warehouse':
            #     return  # Skip processing for non-warehouse users
            
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz',
                'role': 'warehouse'
            }
            
            lang = user.get('language', 'uz')
            
            # Mock applications data (like other modules)
            applications = [
                {
                    'id': 'WH001',
                    'application_details': {
                        'id': 'WH001',
                        'client_name': 'Test Client 1',
                        'description': 'Test description 1',
                        'created_at': datetime.now(),
                        'materials': [
                            {'name': 'Cable', 'quantity': 2, 'unit': 'dona'},
                            {'name': 'Router', 'quantity': 1, 'unit': 'dona'}
                        ]
                    }
                },
                {
                    'id': 'WH002',
                    'application_details': {
                        'id': 'WH002',
                        'client_name': 'Test Client 2',
                        'description': 'Test description 2',
                        'created_at': datetime.now(),
                        'materials': [
                            {'name': 'Connector', 'quantity': 5, 'unit': 'dona'}
                        ]
                    }
                }
            ]
            
            if not applications:
                no_requests_text = "📭 Sizga biriktirilgan zayavkalar yo'q."
                await message.answer(no_requests_text)
                return

            await state.update_data(application_list=applications, current_index=0)
            inbox_title = "📥 <b>Ombor Inbox - Sizga biriktirilgan zayavkalar:</b>"
            
            # Send the title separately, so the first request can be deleted on navigation
            await message.answer(
                inbox_title,
                parse_mode='HTML'
            )
            
            # Display first request in a new message
            await display_application(message, state, lang, applications, 0)
            
            print(f"Warehouse inbox handler completed successfully")
            
        except Exception as e:
            print(f"Error in warehouse inbox handler: {str(e)}")
            await message.answer("Xatolik yuz berdi")

    async def display_application(message: Message, state: FSMContext, lang: str, applications: List[Dict], index: int):
        """Display a single application with pagination buttons - detailed view."""
        try:
            app = applications[index]
            app_id = app['id']
            app_details = app.get('application_details', {})
            
            # Get basic info
            client_name = app_details.get('client_name', 'N/A')
            created = app_details.get('created_at', '').strftime('%d.%m.%Y %H:%M') if app_details.get('created_at') else '-'
            description = app_details.get('description', 'Tavsif yo\'q')
            diagnosis = app_details.get('diagnosis', 'Diagnostika yo\'q')
            
            # Get materials info
            materials = app_details.get('materials', [])
            materials_text = ""
            if materials:
                try:
                    if isinstance(materials, str):
                        materials = json.loads(materials)
                    
                    materials_text = "\n"
                    for i, material in enumerate(materials, 1):
                        name = material.get('name', 'N/A')
                        quantity = material.get('quantity', 0)
                        unit = material.get('unit', 'dona')
                        materials_text += f"  {i}. {name} - {quantity} {unit}\n"
                except Exception as e:
                    materials_text = "\n❌ Materiallar ma'lumotida xatolik\n"
            else:
                materials_text = "\n❌ Materiallar ko'rsatilmagan\n"
            
            # Mock comments count (like other modules)
            comments_count = 2

            # More detailed text with better formatting
            text = (
                f"📦 <b>Zayavka #{app_id[:8]}</b>\n"
                f"👤 <b>Mijoz:</b> {client_name}\n"
                f"📅 <b>Sana:</b> {created}\n"
                f"📄 <b>Tavsif:</b> {description}\n"
                f"🔧 <b>Diagnostika:</b> {diagnosis}\n"
                f"💬 <b>Izohlar:</b> {comments_count} ta\n"
                f"📦 <b>Materiallar kerak:</b>{materials_text}"
            )
            
            # Create action buttons
            buttons = []
            
            # Add action buttons
            action_buttons = []
            
            # Add complete button
            action_buttons.append(InlineKeyboardButton(
                text="✅ Yakunlash",
                callback_data=f"wh_complete_{app_id}"
            ))
            
            # Add return to technician button
            action_buttons.append(InlineKeyboardButton(
                text="🔧 Texnikka qaytarish",
                callback_data=f"wh_return_tech_{app_id}"
            ))
            
            buttons.append(action_buttons)
            
            # Navigation buttons
            nav_buttons = []
            if index > 0:
                nav_buttons.append(InlineKeyboardButton(
                    text="⬅️ Oldingi",
                    callback_data="wh_prev"
                ))
            if index < len(applications) - 1:
                nav_buttons.append(InlineKeyboardButton(
                    text="Keyingisi ➡️",
                    callback_data="wh_next"
                ))
            
            if nav_buttons:
                buttons.append(nav_buttons)

            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            
            await message.answer(
                text,
                parse_mode='HTML',
                reply_markup=keyboard
            )
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    async def display_application_edit(message: Message, state: FSMContext, lang: str, applications: List[Dict], index: int):
        """Display a single application by editing the current message."""
        try:
            app = applications[index]
            app_id = app['id']
            app_details = app.get('application_details', {})
            
            # Get basic info
            client_name = app_details.get('client_name', 'N/A')
            created = app_details.get('created_at', '').strftime('%d.%m.%Y %H:%M') if app_details.get('created_at') else '-'
            description = app_details.get('description', 'Tavsif yo\'q')
            diagnosis = app_details.get('diagnosis', 'Diagnostika yo\'q')
            
            # Get materials info
            materials = app_details.get('materials', [])
            materials_text = ""
            if materials:
                try:
                    if isinstance(materials, str):
                        materials = json.loads(materials)
                    
                    materials_text = "\n"
                    for i, material in enumerate(materials, 1):
                        name = material.get('name', 'N/A')
                        quantity = material.get('quantity', 0)
                        unit = material.get('unit', 'dona')
                        materials_text += f"  {i}. {name} - {quantity} {unit}\n"
                except Exception as e:
                    materials_text = "\n❌ Materiallar ma'lumotida xatolik\n"
            else:
                materials_text = "\n❌ Materiallar ko'rsatilmagan\n"
            
            # Mock comments count (like other modules)
            comments_count = 2

            # More detailed text with better formatting
            text = (
                f"📦 <b>Zayavka #{app_id[:8]}</b>\n"
                f"👤 <b>Mijoz:</b> {client_name}\n"
                f"📅 <b>Sana:</b> {created}\n"
                f"📄 <b>Tavsif:</b> {description}\n"
                f"🔧 <b>Diagnostika:</b> {diagnosis}\n"
                f"💬 <b>Izohlar:</b> {comments_count} ta\n"
                f"📦 <b>Materiallar kerak:</b>{materials_text}"
            )
            
            # Create action buttons
            buttons = []
            
            # Add action buttons
            action_buttons = []
            
            # Add complete button
            action_buttons.append(InlineKeyboardButton(
                text="✅ Yakunlash",
                callback_data=f"wh_complete_{app_id}"
            ))
            
            # Add return to technician button
            action_buttons.append(InlineKeyboardButton(
                text="🔧 Texnikka qaytarish",
                callback_data=f"wh_return_tech_{app_id}"
            ))
            
            buttons.append(action_buttons)
            
            # Navigation buttons
            nav_buttons = []
            if index > 0:
                nav_buttons.append(InlineKeyboardButton(
                    text="⬅️ Oldingi",
                    callback_data="wh_prev"
                ))
            if index < len(applications) - 1:
                nav_buttons.append(InlineKeyboardButton(
                    text="Keyingisi ➡️",
                    callback_data="wh_next"
                ))
            
            if nav_buttons:
                buttons.append(nav_buttons)

            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            
            # Edit the current message instead of sending a new one
            await message.edit_text(text, parse_mode='HTML', reply_markup=keyboard)
            
        except Exception as e:
            await message.edit_text("Xatolik yuz berdi")

    @router.callback_query(F.data == "wh_next")
    async def warehouse_next(callback: CallbackQuery, state: FSMContext):
        """Navigate to next application"""
        try:
            data = await state.get_data()
            applications = data.get('application_list', [])
            current_index = data.get('current_index', 0)
            
            if current_index < len(applications) - 1:
                new_index = current_index + 1
                await state.update_data(current_index=new_index)
                
                # Mock user data (like other modules)
                user = {
                    'id': 1,
                    'full_name': 'Warehouse xodimi',
                    'language': 'uz'
                }
                lang = user.get('language', 'uz')
                
                await display_application(callback.message, state, lang, applications, new_index)
            else:
                await callback.answer("Oxirgi zayavka")
            
            await callback.answer()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "wh_prev")
    async def warehouse_prev(callback: CallbackQuery, state: FSMContext):
        """Navigate to previous application"""
        try:
            data = await state.get_data()
            applications = data.get('application_list', [])
            current_index = data.get('current_index', 0)
            
            if current_index > 0:
                new_index = current_index - 1
                await state.update_data(current_index=new_index)
                
                # Mock user data (like other modules)
                user = {
                    'id': 1,
                    'full_name': 'Warehouse xodimi',
                    'language': 'uz'
                }
                lang = user.get('language', 'uz')
                
                await display_application(callback.message, state, lang, applications, new_index)
            else:
                await callback.answer("Birinchi zayavka")
            
            await callback.answer()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("wh_prepare_"))
    async def prepare_equipment(callback: CallbackQuery, state: FSMContext):
        """Prepare equipment for warehouse"""
        try:
            request_id_short = callback.data.replace("wh_prepare_", "")
            
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            lang = user.get('language', 'uz')
            
            # Mock success response (like other modules)
            text = f"✅ Uskuna tayyorlandi! (Ariza: {request_id_short})"
            await callback.message.edit_text(text)
            await callback.answer()
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("wh_complete_"))
    async def complete_warehouse_task(callback: CallbackQuery, state: FSMContext):
        """Complete warehouse task"""
        try:
            request_id_short = callback.data.replace("wh_complete_", "")
            
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            lang = user.get('language', 'uz')
            
            # Mock success response (like other modules)
            text = (
                f"✅ <b>Ombor yakunlandi!</b>\n"
                f"📦 Ombor: ✅ Yakunlandi\n"
                f"🔧 Texnik: ⏳ Kutilmoqda\n"
                f"📝 Ariza ID: {request_id_short}\n"
                f"ℹ️ Texnik ham yakunlagandan keyin zayavka to'liq yopiladi"
            )
            
            # Update the message with completion status
            await callback.message.edit_text(text, parse_mode='HTML')
            await callback.answer("✅ Zayavka yakunlandi!")
            
            # Remove the application from the list and show next one
            data = await state.get_data()
            applications = data.get('application_list', [])
            current_index = data.get('current_index', 0)
            
            # Remove completed application
            if applications and current_index < len(applications):
                applications.pop(current_index)
                await state.update_data(application_list=applications)
                
                if applications:
                    # Show next application or previous if at end
                    new_index = min(current_index, len(applications) - 1)
                    await state.update_data(current_index=new_index)
                    
                    # Show updated application list
                    await display_application_edit(callback.message, state, lang, applications, new_index)
                else:
                    # No more applications
                    await callback.message.edit_text("📭 Barcha zayavkalar yakunlandi!")
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)





    @router.callback_query(F.data.startswith("wh_return_tech_"))
    async def return_to_technician(callback: CallbackQuery, state: FSMContext):
        """Return request to technician"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            lang = user.get('language', 'uz')
            request_id = callback.data.replace("wh_return_tech_", "")
            
            # Update message with return status
            text = (
                f"🔧 <b>Zayavka texnikka qaytarildi!</b>\n"
                f"📦 Ombor: ❌ Qaytarildi\n"
                f"🔧 Texnik: ⏳ Yangi vazifa\n"
                f"📝 Ariza ID: {request_id}\n"
                f"ℹ️ Texnik zayavkani qayta ko'rib chiqadi"
            )
            
            await callback.message.edit_text(text, parse_mode='HTML')
            await callback.answer("✅ Zayavka texnikka qaytarildi!")
            
            # Remove the application from the list and show next one
            data = await state.get_data()
            applications = data.get('application_list', [])
            current_index = data.get('current_index', 0)
            
            # Remove returned application
            if applications and current_index < len(applications):
                applications.pop(current_index)
                await state.update_data(application_list=applications)
                
                if applications:
                    # Show next application or previous if at end
                    new_index = min(current_index, len(applications) - 1)
                    await state.update_data(current_index=new_index)
                    
                    # Show updated application list
                    await display_application_edit(callback.message, state, lang, applications, new_index)
                else:
                    # No more applications
                    await callback.message.edit_text("📭 Barcha zayavkalar qaytarildi!")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi!", show_alert=True)

    async def back_to_inbox(callback: CallbackQuery, state: FSMContext):
        """Return to warehouse inbox"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz',
                'role': 'warehouse'
            }
            
            lang = user.get('language', 'uz')
            
            # Mock applications data (like other modules)
            applications = [
                {
                    'id': 'WH001',
                    'application_details': {
                        'id': 'WH001',
                        'client_name': 'Test Client 1',
                        'description': 'Test description 1',
                        'created_at': datetime.now(),
                        'materials': [
                            {'name': 'Cable', 'quantity': 2, 'unit': 'dona'},
                            {'name': 'Router', 'quantity': 1, 'unit': 'dona'}
                        ]
                    }
                },
                {
                    'id': 'WH002',
                    'application_details': {
                        'id': 'WH002',
                        'client_name': 'Test Client 2',
                        'description': 'Test description 2',
                        'created_at': datetime.now(),
                        'materials': [
                            {'name': 'Connector', 'quantity': 5, 'unit': 'dona'}
                        ]
                    }
                }
            ]
            
            if not applications:
                no_requests_text = "📭 Sizga biriktirilgan zayavkalar yo'q."
                await callback.message.edit_text(no_requests_text)
                return

            await state.update_data(application_list=applications, current_index=0)
            inbox_title = "📥 <b>Ombor Inbox - Sizga biriktirilgan zayavkalar:</b>"
            
            # Display first request
            await display_application_edit(callback.message, state, lang, applications, 0)
            
        except Exception as e:
            await callback.message.edit_text("Xatolik yuz berdi")




    async def display_warehouse_request(message: Message, state: FSMContext, requests: List[Dict], index: int, lang: str):
        """Display warehouse request (helper function)"""
        try:
            if index < len(requests):
                request = requests[index]
                text = f"📦 Zayavka #{request['id']}\n👤 Mijoz: {request['client_name']}\n📄 Tavsif: {request['description']}"
                await message.answer(text)
            else:
                await message.answer("Zayavka topilmadi")
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    return router

# Mock functions (like other modules)
async def get_warehouse_inbox_requests():
    """Get warehouse inbox requests (mock function like other modules)"""
    try:
        return [
            {
                'id': 'WH001',
                'client_name': 'Test Client 1',
                'description': 'Test description 1',
                'created_at': datetime.now(),
                'materials': [
                    {'name': 'Cable', 'quantity': 2, 'unit': 'dona'},
                    {'name': 'Router', 'quantity': 1, 'unit': 'dona'}
                ]
            },
            {
                'id': 'WH002',
                'client_name': 'Test Client 2',
                'description': 'Test description 2',
                'created_at': datetime.now(),
                'materials': [
                    {'name': 'Connector', 'quantity': 5, 'unit': 'dona'}
                ]
            }
        ]
    except Exception as e:
        return []