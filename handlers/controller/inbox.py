"""
Controller Inbox - Soddalashtirilgan versiya

Bu modul controller uchun inbox funksionalligini o'z ichiga oladi.
Call center supervisor yoki texniklarga tayinlash funksiyasi bilan.
"""

from datetime import datetime, timedelta
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from states.controller_states import ControllerRequestStates
from filters.role_filter import RoleFilter

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'controller',
        'language': 'uz',
        'full_name': 'Test Controller',
        'phone_number': '+998901234567'
    }

async def get_users_by_role(role: str):
    """Mock users by role"""
    if role == 'technician':
        return [
            {
                'id': 1,
                'full_name': 'Ahmad Toshmatov',
                'role': 'technician',
                'telegram_id': 123456789,
                'active_requests': 2,
                'specialization': 'Internet ulanish'
            },
            {
                'id': 2,
                'full_name': 'Malika Karimova',
                'role': 'technician',
                'telegram_id': 987654321,
                'active_requests': 1,
                'specialization': 'TV signal'
            },
            {
                'id': 3,
                'full_name': 'Jasur Rahimov',
                'role': 'technician',
                'telegram_id': 111222333,
                'active_requests': 0,
                'specialization': 'Router va jihozlar'
            },
            {
                'id': 4,
                'full_name': 'Dilfuza Abdullayeva',
                'role': 'technician',
                'telegram_id': 444555666,
                'active_requests': 3,
                'specialization': 'WiFi va signal'
            }
        ]
    elif role == 'call_center_supervisor':
        return [
            {
                'id': 5,
                'full_name': 'Call Center Supervisor',
                'role': 'call_center_supervisor',
                'telegram_id': 777888999,
                'active_requests': 0
            }
        ]
    return []

async def get_user_lang(user_id: int) -> str:
    """Mock user language"""
    return 'uz'

# Mock application data
async def get_controller_applications():
    """Mock get controller applications"""
    now = datetime.now()
    
    return [
        {
            'id': 'req_001_2024_01_15',
            'workflow_type': 'connection_request',
            'current_status': 'sent_to_controller',
            'contact_info': {
                'full_name': 'Aziz Karimov',
                'phone': '+998901234567',
                'phone_number': '+998901234567',
                'email': 'aziz.karimov@example.com'
            },
            'created_at': now - timedelta(hours=3),
            'description': 'Internet ulanish arizasi\nTariff: 100 Mbps\nB2C mijoz\nManzil: Tashkent, Chorsu tumani, 15-uy',
            'location': 'Tashkent, Chorsu tumani, 15-uy',
            'priority': 'high',
            'tariff': '100 Mbps',
            'connection_type': 'B2C',
            'equipment_needed': 'Router, optic kabel',
            'estimated_cost': '500,000 so\'m',
            'expected_completion': '3-5 kun',
            'additional_info': 'Mijoz bilan bog\'landi, batafsil ma\'lumot olingan. Yangi uy, optic kabel kerak.',
            'assigned_to': None
        },
        {
            'id': 'req_002_2024_01_16',
            'workflow_type': 'technical_service',
            'current_status': 'sent_to_controller',
            'contact_info': {
                'full_name': 'Malika Toshmatova',
                'phone': '+998901234568',
                'phone_number': '+998901234568',
                'email': 'malika.toshmatova@example.com'
            },
            'created_at': now - timedelta(hours=2, minutes=30),
            'description': 'TV signal yo\'q\nKabel uzilgan\nManzil: Tashkent, Yunusabad tumani, 45-uy',
            'location': 'Tashkent, Yunusabad tumani, 45-uy',
            'priority': 'medium',
            'service_type': 'TV signal repair',
            'equipment_needed': 'Yangi kabel',
            'estimated_cost': '150,000 so\'m',
            'expected_completion': '1-2 kun',
            'additional_info': 'Mijoz uyda emas, keyinroq qayta urinib ko\'rish kerak. TV kanallar ko\'rinmayapti.',
            'assigned_to': None
        },
        {
            'id': 'req_003_2024_01_17',
            'workflow_type': 'connection_request',
            'current_status': 'sent_to_controller',
            'contact_info': {
                'full_name': 'Jasur Rahimov',
                'phone': '+998901234569',
                'phone_number': '+998901234569',
                'email': 'jasur.rahimov@company.uz'
            },
            'created_at': now - timedelta(hours=1, minutes=45),
            'description': 'Internet ulanish arizasi\nTariff: 50 Mbps\nB2B mijoz\nManzil: Tashkent, Sergeli tumani, 78-uy',
            'location': 'Tashkent, Sergeli tumani, 78-uy',
            'priority': 'normal',
            'tariff': '50 Mbps',
            'connection_type': 'B2B',
            'company_name': 'Rahimov Trading LLC',
            'equipment_needed': 'Router, switch',
            'estimated_cost': '800,000 so\'m',
            'expected_completion': '5-7 kun',
            'additional_info': 'Mijoz bilan bog\'landi, batafsil ma\'lumot olingan. Ish vaqti: 9:00-18:00.',
            'assigned_to': None
        },
        {
            'id': 'req_004_2024_01_18',
            'workflow_type': 'call_center_direct',
            'current_status': 'sent_to_controller',
            'contact_info': {
                'full_name': 'Dilfuza Karimova',
                'phone': '+998901234570',
                'phone_number': '+998901234570',
                'email': 'dilfuza.karimova@example.com'
            },
            'created_at': now - timedelta(hours=1, minutes=20),
            'description': 'Internet sekin ishlaydi\nTezlik past\nManzil: Tashkent, Chilanzar tumani, 23-uy',
            'location': 'Tashkent, Chilanzar tumani, 23-uy',
            'priority': 'high',
            'service_type': 'Speed optimization',
            'current_speed': '1 Mbps',
            'expected_speed': '50 Mbps',
            'estimated_cost': '200,000 so\'m',
            'expected_completion': '2-3 kun',
            'additional_info': '24/7 internet kerak. Download tezligi 1 Mbps, 50 Mbps ga oshirish kerak.',
            'assigned_to': None
        },
        {
            'id': 'req_005_2024_01_19',
            'workflow_type': 'technical_service',
            'current_status': 'sent_to_controller',
            'contact_info': {
                'full_name': 'Asadbek Abdullayev',
                'phone': '+998901234571',
                'phone_number': '+998901234571',
                'email': 'asadbek.abdullayev@example.com'
            },
            'created_at': now - timedelta(hours=1, minutes=10),
            'description': 'Router ishlamayapti\nYangi router kerak\nManzil: Tashkent, Shayxontohur tumani, 67-uy',
            'location': 'Tashkent, Shayxontohur tumani, 67-uy',
            'priority': 'urgent',
            'service_type': 'Router replacement',
            'equipment_needed': 'Yangi router',
            'estimated_cost': '300,000 so\'m',
            'expected_completion': '1 kun',
            'additional_info': 'Mijoz uyda, router muammosi tasdiqlandi. Router yonib-o\'chib turadi.',
            'assigned_to': None
        }
    ]

# Mock assignment functions
async def assign_to_technician(application_id: str, technician_id: int):
    """Mock assign to technician"""
    print(f"Mock: Assigning application {application_id} to technician {technician_id}")
    return True

async def assign_to_call_center_supervisor(application_id: str):
    """Mock assign to call center supervisor"""
    print(f"Mock: Assigning application {application_id} to call center supervisor")
    return True

def get_controller_inbox_router():
    """Get controller inbox router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("controller")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.callback_query(F.data.startswith("open_inbox_"))
    async def handle_inbox_notification(callback: CallbackQuery, state: FSMContext):
        """Handle inbox notification button click"""
        try:
            await callback.answer()
            
            # Extract request ID
            request_id_short = callback.data.replace("open_inbox_", "")
            
            # Get user
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user:
                return
            
            # Show inbox
            await show_controller_inbox_from_notification(callback.message, state, request_id_short)
            
        except Exception as e:
            print(f"Error handling inbox notification: {e}")
            await callback.answer("Xatolik yuz berdi")
    
    async def show_controller_inbox_from_notification(message: Message, state: FSMContext, target_request_id: str = None):
        """Show controller inbox with focus on specific request"""
        try:
            user = await get_user_by_telegram_id(message.chat.id)
            if not user or user['role'] != 'controller':
                return
            
            lang = user.get('language', 'uz')
            
            # Get applications
            applications = await get_controller_applications()
            
            if not applications:
                text = "📭 Inbox bo'sh"
                await message.answer(text)
                return
            
            # Find target request index if specified
            target_index = 0
            if target_request_id:
                for i, app in enumerate(applications):
                    if app['id'].startswith(target_request_id):
                        target_index = i
                        break
            
            await state.update_data(
                applications=applications,
                current_index=target_index
            )
            
            await display_controller_request(message, state, applications, target_index, lang, user)
            
        except Exception as e:
            print(f"Error in show_controller_inbox_from_notification: {e}")

    @router.message(F.text == "📥 Inbox")
    async def show_controller_inbox(message: Message, state: FSMContext):
        """Controller inbox handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'controller':
                return
            
            lang = user.get('language', 'uz')
            
            # Get applications
            applications = await get_controller_applications()
            
            if not applications:
                text = "📭 Inbox bo'sh"
                await message.answer(text)
                return
            
            await state.update_data(
                applications=applications,
                current_index=0
            )
            
            await display_controller_request(message, state, applications, 0, lang, user)
            
        except Exception as e:
            print(f"Error in show_controller_inbox: {str(e)}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    async def display_controller_request(event, state: FSMContext, applications, index, lang, user):
        """Display a single request with assignment options"""
        try:
            app = applications[index]
            full_id = app['id']
            short_id = full_id[:8]
            
            print(f"Displaying request {short_id} for user {user['id']}")
            
            # Format workflow type
            workflow_emoji = {
                'connection_request': '🔌',
                'technical_service': '🔧',
                'call_center_direct': '📞'
            }.get(app['workflow_type'], '📋')
            
            workflow_name = {
                'connection_request': 'Ulanish',
                'technical_service': 'Texnik xizmat',
                'call_center_direct': 'Call Center'
            }.get(app['workflow_type'], app['workflow_type'])
            
            # Format priority
            priority_emoji = {
                'urgent': '🚨',
                'high': '🔴',
                'medium': '🟡', 
                'normal': '🟢'
            }.get(app['priority'], '🟢')
            
            priority_text = {
                'urgent': 'Shoshilinch',
                'high': 'Yuqori',
                'medium': 'O\'rtacha',
                'normal': 'Oddiy'
            }.get(app['priority'], 'Oddiy')
            
            # Format date
            created_date = app['created_at'].strftime('%d.%m.%Y %H:%M')
            
            # Get additional details
            tariff_info = app.get('tariff', '')
            connection_type = app.get('connection_type', '')
            equipment_needed = app.get('equipment_needed', '')
            estimated_cost = app.get('estimated_cost', '')
            expected_completion = app.get('expected_completion', '')
            company_name = app.get('company_name', '')
            additional_info = app.get('additional_info', '')
            
            # Clean text with essential information
            text = (
                f"{workflow_emoji} <b>Controller Inbox</b>\n\n"
                f"🆔 <b>ID:</b> {short_id}-{full_id[8:12].upper()}\n"
                f"📋 <b>Tur:</b> {workflow_name}\n"
                f"👤 <b>Mijoz:</b> {app['contact_info']['full_name']}\n"
                f"📞 <b>Telefon:</b> {app['contact_info']['phone']}\n"
                f"📍 <b>Manzil:</b> {app['location']}\n"
                f"📅 <b>Yaratilgan:</b> {created_date}\n"
                f"{priority_emoji} <b>Muhimlik:</b> {priority_text}\n"
                f"📝 <b>Tavsif:</b> {app['description'][:100]}{'...' if len(app['description']) > 100 else ''}\n"
            )
            
            # Add essential additional details
            if tariff_info:
                text += f"📊 <b>Tarif:</b> {tariff_info}\n"
            if connection_type:
                text += f"🔗 <b>Ulanish turi:</b> {connection_type}\n"
            if equipment_needed:
                text += f"🔧 <b>Kerakli jihozlar:</b> {equipment_needed}\n"
            if estimated_cost:
                text += f"💰 <b>Narx:</b> {estimated_cost}\n"
            if expected_completion:
                text += f"⏱ <b>Muddat:</b> {expected_completion}\n"
            if company_name:
                text += f"🏢 <b>Kompaniya:</b> {company_name}\n"
            
            # Add additional info if available
            if additional_info:
                text += f"\n📋 <b>Qo'shimcha ma'lumot:</b>\n{additional_info}\n"
            
            text += f"\n📊 <b>Ariza {index + 1}/{len(applications)}</b>"
            
            # Create action buttons
            buttons = []
            
            # Assignment buttons
            assignment_buttons = []
            
            # Call Center Supervisor button (always available)
            assignment_buttons.append(InlineKeyboardButton(
                text="📞 Call Center Supervisor",
                callback_data=f"ctrl_assign_ccsupervisor_{full_id}"
            ))
            
            # Technician button
            assignment_buttons.append(InlineKeyboardButton(
                text="🔧 Texnik tanlash",
                callback_data=f"ctrl_assign_tech_{full_id}"
            ))
            
            buttons.append(assignment_buttons)
            
            # Navigation buttons
            nav_buttons = []
            
            # Previous button
            if index > 0:
                nav_buttons.append(
                    InlineKeyboardButton(
                        text="⬅️ Oldingi",
                        callback_data=f"ctrl_prev_{index}"
                    )
                )
            
            # Next button
            if index < len(applications) - 1:
                nav_buttons.append(
                    InlineKeyboardButton(
                        text="Keyingi ➡️",
                        callback_data=f"ctrl_next_{index}"
                    )
                )
            
            # Add navigation buttons if they exist
            if nav_buttons:
                buttons.append(nav_buttons)
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            
            print(f"Sending message for request {short_id}")
            try:
                # Check if this is a callback query (inline keyboard event)
                if hasattr(event, 'message') and hasattr(event, 'from_user'):
                    # This is a CallbackQuery - edit the existing message
                    await event.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                    print(f"Successfully edited message for request {short_id}")
                else:
                    # This is a Message - send new message
                    await event.answer(text, reply_markup=keyboard, parse_mode='HTML')
                    print(f"Successfully sent new message for request {short_id}")
            except Exception as e:
                print(f"Error sending message for request {short_id}: {e}")
                if "message can't be edited" in str(e):
                    # If edit fails, try to send a new message
                    if hasattr(event, 'message') and hasattr(event, 'from_user'):
                        # For callback events, try to send a new message via bot
                        from aiogram import Bot
                        bot = Bot.get_current()
                        await bot.send_message(event.from_user.id, text, reply_markup=keyboard, parse_mode='HTML')
                        print(f"Sent new message via bot for request {short_id}")
                    else:
                        # For message events, try answer again
                        await event.answer(text, reply_markup=keyboard, parse_mode='HTML')
                        print(f"Sent new message for request {short_id}")
                else:
                    raise
            
        except Exception as e:
            print(f"Error in display_controller_request: {e}")
            error_text = "Xatolik yuz berdi"
            try:
                if hasattr(event, 'message') and hasattr(event.message, 'edit_text'):
                    await event.message.edit_text(error_text)
                elif hasattr(event, 'edit_text'):
                    await event.edit_text(error_text)
                else:
                    print("Cannot display error message - no edit_text method available")
            except Exception as edit_error:
                print(f"Error editing message: {edit_error}")

    @router.callback_query(F.data.startswith("ctrl_assign_ccsupervisor_"))
    async def assign_to_call_center_supervisor(callback: CallbackQuery, state: FSMContext):
        """Assign to call center supervisor"""
        try:
            await callback.answer()
            
            full_id = callback.data.replace("ctrl_assign_ccsupervisor_", "")
            short_id = full_id[:8]
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            # Get application data
            data = await state.get_data()
            applications = data.get('applications', [])
            current_index = data.get('current_index', 0)
            
            if not applications or current_index >= len(applications):
                await callback.answer("Ariza topilmadi")
                return
            
            application = applications[current_index]
            
            # Mock assignment
            success = await assign_to_call_center_supervisor(full_id)
            
            if success:
                # Update application status
                applications[current_index]['assigned_to'] = 'call_center_supervisor'
                await state.update_data(applications=applications)
                
                text = (
                    f"✅ <b>Tayinlash muvaffaqiyatli!</b>\n\n"
                    f"📝 Ariza ID: {short_id}\n"
                    f"👤 Mijoz: {application['contact_info']['full_name']}\n"
                    f"📞 Call Center Supervisor'ga yuborildi\n\n"
                    f"Ariza sizning inboxingizdan o'chirilib, call center supervisor inboxiga o'tdi."
                )
                
                await callback.message.edit_text(text, parse_mode='HTML')
                
                # Remove the request from current session
                updated_applications = [a for a in applications if a['id'] != full_id]
                new_index = current_index
                
                if updated_applications:
                    # Adjust index if needed
                    if new_index >= len(updated_applications):
                        new_index = len(updated_applications) - 1
                    
                    await state.update_data(
                        applications=updated_applications,
                        current_index=new_index
                    )
                    
                    # Show next request after 2 seconds
                    import asyncio
                    await asyncio.sleep(2)
                    await display_controller_request(callback, state, updated_applications, new_index, lang, user)
                else:
                    await state.clear()
                    
                await callback.answer()
            else:
                await callback.answer("Tayinlashda xatolik yuz berdi", show_alert=True)
                
        except Exception as e:
            print(f"Error in assign_to_call_center_supervisor: {str(e)}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("ctrl_assign_tech_"))
    async def assign_to_technician(callback: CallbackQuery, state: FSMContext):
        """Assign to technician"""
        try:
            await callback.answer()
            
            full_id = callback.data.replace("ctrl_assign_tech_", "")
            short_id = full_id[:8]
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            # Get application data from state
            data = await state.get_data()
            applications = data.get('applications', [])
            current_index = data.get('current_index', 0)
            
            if not applications or current_index >= len(applications):
                await callback.answer("Ariza topilmadi")
                return
            
            application = applications[current_index]
            
            # Get available technicians
            technicians = await get_users_by_role('technician')
            
            if not technicians:
                await callback.message.edit_text("Texniklar topilmadi")
                return
            
            # Create selection keyboard
            buttons = []
            for tech in technicians:
                buttons.append([InlineKeyboardButton(
                    text=f"🔧 {tech.get('full_name', 'N/A')} ({tech.get('specialization', 'Texnik')}) - {tech.get('active_requests', 0)} ariza",
                    callback_data=f"ctrl_select_tech_{full_id}_{tech['id']}"
                )])
            
            text = (
                f"🔧 <b>Texnik tanlang</b>\n\n"
                f"📝 Ariza ID: {short_id}\n"
                f"👤 Mijoz: {application['contact_info']['full_name']}\n\n"
                f"Quyidagi texniklardan birini tanlang:"
            )
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            await callback.message.edit_text(
                text=text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in assign_to_technician: {str(e)}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("ctrl_select_tech_"))
    async def select_technician(callback: CallbackQuery, state: FSMContext):
        """Select technician for assignment"""
        try:
            parts = callback.data.replace("ctrl_select_tech_", "").split("_")
            full_id = parts[0]
            technician_id = int(parts[1])
            short_id = full_id[:8]
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            # Get application data
            data = await state.get_data()
            applications = data.get('applications', [])
            current_index = data.get('current_index', 0)
            
            if not applications or current_index >= len(applications):
                await callback.answer("Ariza topilmadi")
                return
            
            application = applications[current_index]
            
            # Get technician info
            technicians = await get_users_by_role('technician')
            technician = next((t for t in technicians if t['id'] == technician_id), None)
            
            if not technician:
                await callback.answer("Texnik topilmadi")
                return
            
            # Mock assignment
            success = await assign_to_technician(full_id, technician_id)
            
            if success:
                # Update application status
                applications[current_index]['assigned_to'] = f"technician_{technician_id}"
                await state.update_data(applications=applications)
                
                text = (
                    f"✅ <b>Tayinlash muvaffaqiyatli!</b>\n\n"
                    f"📝 Ariza ID: {short_id}\n"
                    f"👤 Mijoz: {application['contact_info']['full_name']}\n"
                    f"🔧 Texnik: {technician.get('full_name', 'N/A')}\n"
                    f"📊 Ixtisoslik: {technician.get('specialization', 'Texnik')}\n\n"
                    f"Ariza sizning inboxingizdan o'chirilib, texnik inboxiga o'tdi."
                )
                
                await callback.message.edit_text(text, parse_mode='HTML')
                
                # Remove the request from current session
                updated_applications = [a for a in applications if a['id'] != full_id]
                new_index = current_index
                
                if updated_applications:
                    # Adjust index if needed
                    if new_index >= len(updated_applications):
                        new_index = len(updated_applications) - 1
                    
                    await state.update_data(
                        applications=updated_applications,
                        current_index=new_index
                    )
                    
                    # Show next request after 2 seconds
                    import asyncio
                    await asyncio.sleep(2)
                    await display_controller_request(callback, state, updated_applications, new_index, lang, user)
                else:
                    await state.clear()
                    
                await callback.answer()
            else:
                await callback.answer("Tayinlashda xatolik yuz berdi", show_alert=True)
                
        except Exception as e:
            print(f"Error in select_technician: {str(e)}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("ctrl_prev_"))
    async def navigate_previous(callback: CallbackQuery, state: FSMContext):
        """Navigate to previous request"""
        try:
            await callback.answer()
            
            # Extract index from callback data
            current_index = int(callback.data.replace("ctrl_prev_", ""))
            new_index = current_index - 1
            
            if new_index < 0:
                await callback.answer("Birinchi ariza", show_alert=True)
                return
            
            # Get user and data
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            data = await state.get_data()
            applications = data.get('applications', [])
            
            if not applications or new_index >= len(applications):
                await callback.answer("Ariza topilmadi", show_alert=True)
                return
            
            # Update current index
            await state.update_data(current_index=new_index)
            
            # Display the previous request
            await display_controller_request(callback, state, applications, new_index, lang, user)
            
        except Exception as e:
            print(f"Error in navigate_previous: {str(e)}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("ctrl_next_"))
    async def navigate_next(callback: CallbackQuery, state: FSMContext):
        """Navigate to next request"""
        try:
            await callback.answer()
            
            # Extract index from callback data
            current_index = int(callback.data.replace("ctrl_next_", ""))
            new_index = current_index + 1
            
            # Get user and data
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            data = await state.get_data()
            applications = data.get('applications', [])
            
            if not applications or new_index >= len(applications):
                await callback.answer("Oxirgi ariza", show_alert=True)
                return
            
            # Update current index
            await state.update_data(current_index=new_index)
            
            # Display the next request
            await display_controller_request(callback, state, applications, new_index, lang, user)
            
        except Exception as e:
            print(f"Error in navigate_next: {str(e)}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    return router