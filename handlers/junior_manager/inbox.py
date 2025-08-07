"""
Junior Manager Inbox - To'liq yangilangan versiya

Bu modul kichik menejer uchun inbox funksionalligini o'z ichiga oladi.
Mijoz bilan bog'lanish va controllerga yuborish funksiyalari bilan.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.junior_manager_buttons import (
    get_contact_note_keyboard,
    get_controller_note_keyboard,
    get_send_to_controller_confirmation_keyboard,
    get_edit_controller_note_keyboard,
    get_back_to_application_keyboard
)
from datetime import datetime, timedelta
from filters.role_filter import RoleFilter
from states.junior_manager_states import JuniorManagerStates

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'junior_manager',
        'language': 'uz',
        'full_name': 'Test Junior Manager',
        'phone_number': '+998901234567'
    }

async def get_junior_manager_applications(user_id: int):
    """Mock get junior manager applications with comprehensive data"""
    now = datetime.now()
    
    return [
        {
            'id': 'req_001_2024_01_15',
            'workflow_type': 'connection_request',
            'current_status': 'assigned_to_junior_manager',
            'contact_info': {
                'full_name': 'Aziz Karimov',
                'phone': '+998901234567',
                'phone_number': '+998901234567',
                'email': 'aziz.karimov@example.com'
            },
            'created_at': now - timedelta(hours=2),
            'description': 'Internet ulanish arizasi\nTariff: 100 Mbps\nB2C mijoz\nManzil: Tashkent, Chorsu tumani, 15-uy\nQo\'shimcha ma\'lumot: Yangi uy, optic kabel kerak',
            'location': 'Tashkent, Chorsu tumani, 15-uy',
            'priority': 'high',
            'region': 'Toshkent shahri',
            'address': 'Chorsu tumani, 15-uy',
            'tariff': '100 Mbps',
            'connection_type': 'B2C',
            'equipment_needed': 'Router, optic kabel',
            'estimated_cost': '500,000 so\'m',
            'expected_completion': '3-5 kun',
            'client_preferences': 'Yangi uy, yuqori tezlik kerak',
            'technical_requirements': 'Optic kabel o\'rnatish kerak',
            'contact_attempts': 0,
            'last_contact_date': None,
            'notes': ''
        },
        {
            'id': 'req_002_2024_01_16',
            'workflow_type': 'technical_service',
            'current_status': 'assigned_to_junior_manager',
            'contact_info': {
                'full_name': 'Malika Toshmatova',
                'phone': '+998901234568',
                'phone_number': '+998901234568',
                'email': 'malika.toshmatova@example.com'
            },
            'created_at': now - timedelta(hours=1, minutes=30),
            'description': 'TV signal yo\'q\nKabel uzilgan\nManzil: Tashkent, Yunusabad tumani, 45-uy\nMuammo: TV kanallar ko\'rinmayapti',
            'location': 'Tashkent, Yunusabad tumani, 45-uy',
            'priority': 'medium',
            'region': 'Toshkent shahri',
            'address': 'Yunusabad tumani, 45-uy',
            'service_type': 'TV signal repair',
            'equipment_needed': 'Yangi kabel',
            'estimated_cost': '150,000 so\'m',
            'expected_completion': '1-2 kun',
            'client_preferences': 'Tez yechim kerak',
            'technical_requirements': 'Kabel almashtirish',
            'contact_attempts': 1,
            'last_contact_date': now - timedelta(hours=1),
            'notes': 'Mijoz uyda emas, keyinroq qayta urinib ko\'rish kerak'
        },
        {
            'id': 'req_003_2024_01_17',
            'workflow_type': 'connection_request',
            'current_status': 'assigned_to_junior_manager',
            'contact_info': {
                'full_name': 'Jasur Rahimov',
                'phone': '+998901234569',
                'phone_number': '+998901234569',
                'email': 'jasur.rahimov@company.uz'
            },
            'created_at': now - timedelta(minutes=45),
            'description': 'Internet ulanish arizasi\nTariff: 50 Mbps\nB2B mijoz\nManzil: Tashkent, Sergeli tumani, 78-uy\nKompaniya: "Rahimov Trading" LLC',
            'location': 'Tashkent, Sergeli tumani, 78-uy',
            'priority': 'normal',
            'region': 'Toshkent shahri',
            'address': 'Sergeli tumani, 78-uy',
            'tariff': '50 Mbps',
            'connection_type': 'B2B',
            'company_name': 'Rahimov Trading LLC',
            'equipment_needed': 'Router, switch',
            'estimated_cost': '800,000 so\'m',
            'expected_completion': '5-7 kun',
            'client_preferences': 'Ish vaqti: 9:00-18:00',
            'technical_requirements': 'Ofis uchun maxsus jihozlar',
            'contact_attempts': 2,
            'last_contact_date': now - timedelta(minutes=30),
            'notes': 'Mijoz bilan bog\'landi, batafsil ma\'lumot olingan'
        },
        {
            'id': 'req_004_2024_01_18',
            'workflow_type': 'call_center_direct',
            'current_status': 'assigned_to_junior_manager',
            'contact_info': {
                'full_name': 'Dilfuza Karimova',
                'phone': '+998901234570',
                'phone_number': '+998901234570',
                'email': 'dilfuza.karimova@example.com'
            },
            'created_at': now - timedelta(minutes=20),
            'description': 'Internet sekin ishlaydi\nTezlik past\nManzil: Tashkent, Chilanzar tumani, 23-uy\nMuammo: Download tezligi 1 Mbps',
            'location': 'Tashkent, Chilanzar tumani, 23-uy',
            'priority': 'high',
            'region': 'Toshkent shahri',
            'address': 'Chilanzar tumani, 23-uy',
            'service_type': 'Speed optimization',
            'current_speed': '1 Mbps',
            'expected_speed': '50 Mbps',
            'estimated_cost': '200,000 so\'m',
            'expected_completion': '2-3 kun',
            'client_preferences': '24/7 internet kerak',
            'technical_requirements': 'Tezlikni oshirish',
            'contact_attempts': 0,
            'last_contact_date': None,
            'notes': ''
        },
        {
            'id': 'req_005_2024_01_19',
            'workflow_type': 'technical_service',
            'current_status': 'assigned_to_junior_manager',
            'contact_info': {
                'full_name': 'Asadbek Abdullayev',
                'phone': '+998901234571',
                'phone_number': '+998901234571',
                'email': 'asadbek.abdullayev@example.com'
            },
            'created_at': now - timedelta(minutes=10),
            'description': 'Router ishlamayapti\nYangi router kerak\nManzil: Tashkent, Shayxontohur tumani, 67-uy\nMuammo: Router yonib-o\'chib turadi',
            'location': 'Tashkent, Shayxontohur tumani, 67-uy',
            'priority': 'urgent',
            'region': 'Toshkent shahri',
            'address': 'Shayxontohur tumani, 67-uy',
            'service_type': 'Router replacement',
            'equipment_needed': 'Yangi router',
            'estimated_cost': '300,000 so\'m',
            'expected_completion': '1 kun',
            'client_preferences': 'Shoshilinch yordam kerak',
            'technical_requirements': 'Router almashtirish',
            'contact_attempts': 1,
            'last_contact_date': now - timedelta(minutes=5),
            'notes': 'Mijoz uyda, router muammosi tasdiqlandi'
        }
    ]

# Mock controller functions
async def send_to_controller(application_id: str, additional_info: str, junior_manager_id: int):
    """Mock send to controller"""
    print(f"Mock: Sending application {application_id} to controller with info: {additional_info}")
    return True

async def update_application_status(application_id: str, status: str, notes: str = ""):
    """Mock update application status"""
    print(f"Mock: Updating application {application_id} status to {status}")
    return True

def get_junior_manager_inbox_router():
    """Router for junior manager inbox functionality"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("junior_manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["📥 Inbox", "📥 Входящие"]))
    async def view_inbox(message: Message, state: FSMContext):
        """Junior manager view inbox handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                return
            
            lang = user.get('language', 'uz')
            
            # Get junior manager applications
            applications = await get_junior_manager_applications(message.from_user.id)
            
            if not applications:
                no_applications_text = (
                    "📭 Hozircha sizga biriktirilgan arizalar yo'q."
                    if lang == 'uz' else
                    "📭 Пока нет заявок, назначенных вам."
                )
                
                await message.answer(
                    text=no_applications_text,
                    reply_markup=get_back_to_application_keyboard(lang)
                )
                return
            
            # Store applications in state
            await state.update_data(
                applications=applications,
                current_app_index=0
            )
            
            # Show first application
            await show_application_details(message, applications[0], applications, 0)
            
        except Exception as e:
            print(f"Error in view_inbox: {e}")

    async def show_application_details(message_or_callback, application, applications, index):
        """Show application details with comprehensive information"""
        try:
            # Format workflow type
            workflow_type_emoji = {
                'connection_request': '🔌',
                'technical_service': '🔧',
                'call_center_direct': '📞'
            }.get(application['workflow_type'], '📄')
            
            workflow_type_text = {
                'connection_request': 'Ulanish arizasi',
                'technical_service': 'Texnik xizmat',
                'call_center_direct': 'Call Center'
            }.get(application['workflow_type'], 'Boshqa')
            
            # Format status
            status_emoji = {
                'assigned_to_junior_manager': '👨‍💼',
                'in_progress': '🟠',
                'completed': '🟢',
                'cancelled': '🔴',
                'pending': '🟡'
            }.get(application['current_status'], '⚪')
            
            status_text = {
                'assigned_to_junior_manager': 'Kichik menejerga tayinlangan',
                'in_progress': 'Jarayonda',
                'completed': 'Bajarilgan',
                'cancelled': 'Bekor qilingan',
                'pending': 'Kutilmoqda'
            }.get(application['current_status'], 'Noma\'lum')
            
            # Format priority
            priority_emoji = {
                'urgent': '🚨',
                'high': '🔴',
                'normal': '🟡',
                'low': '🟢'
            }.get(application.get('priority', 'normal'), '🟡')
            
            priority_text = {
                'urgent': 'Shoshilinch',
                'high': 'Yuqori',
                'normal': 'O\'rtacha',
                'low': 'Past'
            }.get(application.get('priority', 'normal'), 'O\'rtacha')
            
            # Format date
            created_date = application['created_at'].strftime('%d.%m.%Y %H:%M')
            
            # Get additional details
            tariff_info = application.get('tariff', 'N/A')
            connection_type = application.get('connection_type', 'N/A')
            equipment_needed = application.get('equipment_needed', 'N/A')
            estimated_cost = application.get('estimated_cost', 'N/A')
            expected_completion = application.get('expected_completion', 'N/A')
            company_name = application.get('company_name', '')
            contact_attempts = application.get('contact_attempts', 0)
            last_contact = application.get('last_contact_date')
            notes = application.get('notes', '')
            
            # Contact status
            contact_status = "📞 Bog'lanmagan" if contact_attempts == 0 else f"📞 Bog'lanishlar: {contact_attempts}"
            if last_contact:
                contact_status += f"\n⏰ Oxirgi: {last_contact.strftime('%d.%m.%Y %H:%M')}"
            
            # To'liq ma'lumot
            text = (
                f"{workflow_type_emoji} <b>{workflow_type_text} - To'liq ma'lumot</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"📅 <b>Sana:</b> {created_date}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📞 <b>Telefon:</b> {application['contact_info']['phone']}\n"
                f"📧 <b>Email:</b> {application['contact_info'].get('email', 'N/A')}\n"
                f"🏛️ <b>Hudud:</b> {application.get('region', 'Noma\'lum')}\n"
                f"🏠 <b>Manzil:</b> {application.get('address', 'Noma\'lum')}\n"
                f"📝 <b>Tavsif:</b> {application['description'][:100]}{'...' if len(application['description']) > 100 else ''}\n"
                f"{status_emoji} <b>Holat:</b> {status_text}\n"
                f"{priority_emoji} <b>Ustuvorlik:</b> {priority_text}\n"
            )
            
            # Add additional details if available
            if tariff_info != 'N/A':
                text += f"📊 <b>Tarif:</b> {tariff_info}\n"
            if connection_type != 'N/A':
                text += f"🔗 <b>Ulanish turi:</b> {connection_type}\n"
            if equipment_needed != 'N/A':
                text += f"🔧 <b>Kerakli jihozlar:</b> {equipment_needed}\n"
            if estimated_cost != 'N/A':
                text += f"💰 <b>Taxminiy narx:</b> {estimated_cost}\n"
            if expected_completion != 'N/A':
                text += f"⏱ <b>Taxminiy muddat:</b> {expected_completion}\n"
            if company_name:
                text += f"🏢 <b>Kompaniya:</b> {company_name}\n"
            
            # Add contact information
            text += f"\n{contact_status}\n"
            
            if notes:
                text += f"📝 <b>Izohlar:</b> {notes}\n"
            
            text += f"\n📊 <b>Ariza #{index + 1} / {len(applications)}</b>"
            
            # Create navigation keyboard
            keyboard = get_applications_navigation_keyboard(index, len(applications))
            
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer(text, reply_markup=keyboard, parse_mode='HTML')
            else:
                await message_or_callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                
        except Exception as e:
            print(f"Error in show_application_details: {e}")

    @router.callback_query(F.data == "jm_prev_application")
    async def show_previous_application(callback: CallbackQuery, state: FSMContext):
        """Show previous application"""
        try:
            await callback.answer()
            
            # Get current index from state
            data = await state.get_data()
            current_index = data.get('current_app_index', 0)
            applications = data.get('applications', [])
            
            if not applications:
                await callback.answer("Arizalar topilmadi")
                return
            
            if current_index > 0:
                new_index = current_index - 1
                await state.update_data(current_app_index=new_index)
                await show_application_details(callback, applications[new_index], applications, new_index)
            else:
                await callback.answer("Bu birinchi ariza")
                
        except Exception as e:
            print(f"Error in show_previous_application: {e}")

    @router.callback_query(F.data == "jm_next_application")
    async def show_next_application(callback: CallbackQuery, state: FSMContext):
        """Show next application"""
        try:
            await callback.answer()
            
            # Get current index from state
            data = await state.get_data()
            current_index = data.get('current_app_index', 0)
            applications = data.get('applications', [])
            
            if not applications:
                await callback.answer("Arizalar topilmadi")
                return
            
            if current_index < len(applications) - 1:
                new_index = current_index + 1
                await state.update_data(current_app_index=new_index)
                await show_application_details(callback, applications[new_index], applications, new_index)
            else:
                await callback.answer("Bu oxirgi ariza")
                
        except Exception as e:
            print(f"Error in show_next_application: {e}")

    @router.callback_query(F.data == "jm_contact_client")
    async def contact_client_handler(callback: CallbackQuery, state: FSMContext):
        """Handle contact client button"""
        try:
            await callback.answer()
            
            # Get current application
            data = await state.get_data()
            current_index = data.get('current_app_index', 0)
            applications = data.get('applications', [])
            
            if not applications or current_index >= len(applications):
                await callback.answer("Ariza topilmadi")
                return
            
            application = applications[current_index]
            
            # Update contact attempts
            application['contact_attempts'] += 1
            application['last_contact_date'] = datetime.now()
            
            # Update state
            applications[current_index] = application
            await state.update_data(applications=applications)
            
            # Show contact information
            contact_text = (
                f"📞 <b>Mijoz bilan bog'lanish</b>\n\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📞 <b>Telefon:</b> {application['contact_info']['phone']}\n"
                f"📧 <b>Email:</b> {application['contact_info'].get('email', 'N/A')}\n"
                f"🏠 <b>Manzil:</b> {application.get('address', 'Noma\'lum')}\n"
                f"📝 <b>Ariza ID:</b> {application['id']}\n"
                f"📊 <b>Bog'lanishlar soni:</b> {application['contact_attempts']}\n"
                f"⏰ <b>Oxirgi bog'lanish:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
                f"💡 <b>Maslahat:</b>\n"
                f"• Mijoz bilan bog'laning\n"
                f"• Qo'shimcha ma'lumotlarni oling\n"
                f"• Texnik talablarni aniqlang\n"
                f"• Narx va muddatni kelishib oling"
            )
            
            # Create action buttons
            buttons = []
            
            # Add contact note button
            buttons.append([InlineKeyboardButton(
                text="📝 Bog'lanish izohini qo'shish",
                callback_data="jm_add_contact_note"
            )])
            
            # Add back button
            buttons.append([InlineKeyboardButton(
                text="⬅️ Orqaga qaytish",
                callback_data="jm_back_to_application"
            )])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            
            await callback.message.edit_text(
                contact_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in contact_client_handler: {e}")
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "jm_add_contact_note")
    async def add_contact_note_handler(callback: CallbackQuery, state: FSMContext):
        """Handle add contact note button"""
        try:
            await callback.answer()
            
            # Get current application
            data = await state.get_data()
            current_index = data.get('current_app_index', 0)
            applications = data.get('applications', [])
            
            if not applications or current_index >= len(applications):
                await callback.answer("Ariza topilmadi")
                return
            
            application = applications[current_index]
            
            # Store application info in state
            await state.update_data(
                current_application_id=application['id'],
                current_application_data=application
            )
            
            # Show text input prompt
            input_text = (
                f"📝 <b>Bog'lanish izohini kiriting</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📞 <b>Telefon:</b> {application['contact_info']['phone']}\n\n"
                f"📝 Iltimos, bog'lanish natijasini yozing:\n"
                f"• Mijoz talablari\n"
                f"• Qo'shimcha ma'lumotlar\n"
                f"• Texnik talablar\n"
                f"• Narx va muddat"
            )
            
            # Create cancel button
            keyboard = get_contact_note_keyboard(lang)
            
            await callback.message.edit_text(
                input_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
            # Set state to wait for contact note input
            await state.set_state(JuniorManagerStates.waiting_for_contact_note)
            
        except Exception as e:
            print(f"Error in add_contact_note_handler: {e}")
            await callback.answer("Xatolik yuz berdi")

    @router.message(JuniorManagerStates.waiting_for_contact_note)
    async def handle_contact_note_input(message: Message, state: FSMContext):
        """Handle text input for contact note"""
        try:
            # Get the note text
            note_text = message.text.strip()
            
            if len(note_text) < 10:
                await message.answer(
                    "⚠️ Iltimos, kamida 10 ta belgi kiriting. Bog'lanish natijasini batafsil yozing."
                )
                return
            
            # Get application data from state
            data = await state.get_data()
            application = data.get('current_application_data')
            
            if not application:
                await message.answer("❌ Ariza ma'lumotlari topilmadi. Iltimos, qaytadan urinib ko'ring.")
                return
            
            # Update application notes
            applications = data.get('applications', [])
            current_index = data.get('current_app_index', 0)
            
            if applications and current_index < len(applications):
                applications[current_index]['notes'] = note_text
                await state.update_data(applications=applications)
            
            # Show confirmation
            confirmation_text = (
                f"✅ <b>Bog'lanish izohi qo'shildi!</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📝 <b>Izoh:</b>\n"
                f"<i>{note_text}</i>\n\n"
                f"📅 <b>Qo'shilgan vaqt:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}"
            )
            
            # Create back button
            keyboard = get_back_to_application_keyboard(lang)
            
            await message.answer(
                confirmation_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
            # Clear the waiting state
            await state.clear()
            
        except Exception as e:
            print(f"Error in handle_contact_note_input: {e}")
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "jm_send_to_controller")
    async def send_to_controller_handler(callback: CallbackQuery, state: FSMContext):
        """Handle send to controller button"""
        try:
            await callback.answer()
            
            # Get current application
            data = await state.get_data()
            current_index = data.get('current_app_index', 0)
            applications = data.get('applications', [])
            
            if not applications or current_index >= len(applications):
                await callback.answer("Ariza topilmadi")
                return
            
            application = applications[current_index]
            
            # Store application info in state for later use
            await state.update_data(
                current_application_id=application['id'],
                current_application_data=application
            )
            
            # Show text input prompt
            input_text = (
                f"📝 <b>Controller'ga qo'shimcha ma'lumot kiriting</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📞 <b>Telefon:</b> {application['contact_info']['phone']}\n"
                f"📝 <b>Asosiy tavsif:</b> {application['description'][:100]}{'...' if len(application['description']) > 100 else ''}\n\n"
                f"📝 <b>Qo'shimcha ma'lumotlarni yozing:</b>\n"
                f"• Mijoz bilan bog'lanish natijasi\n"
                f"• Qo'shimcha texnik talablar\n"
                f"• Narx va muddat kelishuvi\n"
                f"• Maxsus talablar yoki cheklovlar"
            )
            
            # Create cancel button
            cancel_button = InlineKeyboardButton(
                text="❌ Bekor qilish",
                callback_data="jm_back_to_application"
            )
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[cancel_button]])
            
            await callback.message.edit_text(
                input_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
            # Set state to wait for text input
            await state.set_state(JuniorManagerStates.waiting_for_controller_note)
            
        except Exception as e:
            print(f"Error in send_to_controller_handler: {e}")
            await callback.answer("Xatolik yuz berdi")

    @router.message(JuniorManagerStates.waiting_for_controller_note)
    async def handle_controller_note_input(message: Message, state: FSMContext):
        """Handle text input for controller note"""
        try:
            # Get the note text
            note_text = message.text.strip()
            
            if len(note_text) < 20:
                await message.answer(
                    "⚠️ Iltimos, kamida 20 ta belgi kiriting. Qo'shimcha ma'lumotlarni batafsil yozing."
                )
                return
            
            # Store the note in state
            await state.update_data(controller_note=note_text)
            
            # Get application data from state
            data = await state.get_data()
            application = data.get('current_application_data')
            
            if not application:
                await message.answer("❌ Ariza ma'lumotlari topilmadi. Iltimos, qaytadan urinib ko'ring.")
                return
            
            # Show review and confirmation
            review_text = (
                f"📋 <b>Yuborishdan oldin tekshirish</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📞 <b>Telefon:</b> {application['contact_info']['phone']}\n"
                f"🏠 <b>Manzil:</b> {application.get('address', 'Noma\'lum')}\n"
                f"📝 <b>Asosiy tavsif:</b> {application['description'][:100]}{'...' if len(application['description']) > 100 else ''}\n\n"
                f"📝 <b>Qo'shimcha ma'lumotlar:</b>\n"
                f"<i>{note_text}</i>\n\n"
                f"Controller'ga yuborishni tasdiqlaysizmi?"
            )
            
            # Create confirmation buttons
            keyboard = get_send_to_controller_confirmation_keyboard(lang)
            
            await message.answer(
                review_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
            # Clear the waiting state
            await state.clear()
            
        except Exception as e:
            print(f"Error in handle_controller_note_input: {e}")
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "jm_edit_controller_note")
    async def edit_controller_note_handler(callback: CallbackQuery, state: FSMContext):
        """Handle edit controller note button"""
        try:
            await callback.answer()
            
            # Get application data from state
            data = await state.get_data()
            application = data.get('current_application_data')
            
            if not application:
                await callback.answer("Ariza ma'lumotlari topilmadi")
                return
            
            # Show text input prompt again
            input_text = (
                f"📝 <b>Controller'ga qo'shimcha ma'lumot kiriting</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📞 <b>Telefon:</b> {application['contact_info']['phone']}\n"
                f"📝 <b>Asosiy tavsif:</b> {application['description'][:100]}{'...' if len(application['description']) > 100 else ''}\n\n"
                f"📝 <b>Qo'shimcha ma'lumotlarni yozing:</b>"
            )
            
            # Create cancel button
            keyboard = get_edit_controller_note_keyboard(lang)
            
            await callback.message.edit_text(
                input_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
            # Set state to wait for text input again
            await state.set_state(JuniorManagerStates.waiting_for_controller_note)
            
        except Exception as e:
            print(f"Error in edit_controller_note_handler: {e}")
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "jm_confirm_send_to_controller")
    async def confirm_send_to_controller_handler(callback: CallbackQuery, state: FSMContext):
        """Handle confirmation to send to controller"""
        try:
            await callback.answer()
            
            # Get application data and note from state
            data = await state.get_data()
            application = data.get('current_application_data')
            note_text = data.get('controller_note', '')
            
            if not application:
                await callback.answer("Ariza ma'lumotlari topilmadi")
                return
            
            # Mock sending to controller
            success = await send_to_controller(application['id'], note_text, callback.from_user.id)
            
            if success:
                # Update application status
                await update_application_status(application['id'], 'sent_to_controller', note_text)
                
                success_text = (
                    f"✅ <b>Ariza muvaffaqiyatli yuborildi!</b>\n\n"
                    f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                    f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                    f"📤 <b>Yuborilgan vaqt:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
                    f"👨‍💼 <b>Yuboruvchi:</b> Kichik menejer\n\n"
                    f"📝 <b>Qo'shimcha ma'lumotlar:</b>\n"
                    f"<i>{note_text}</i>\n\n"
                    f"📋 Ariza controller'ga yuborildi va keyingi bosqichga o'tdi."
                )
                
                # Create back to inbox button
                back_button = InlineKeyboardButton(
                    text="📥 Inbox'ga qaytish",
                    callback_data="jm_back_to_inbox"
                )
                keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button]])
                
                await callback.message.edit_text(
                    success_text,
                    reply_markup=keyboard,
                    parse_mode='HTML'
                )
            else:
                await callback.answer("Yuborishda xatolik yuz berdi", show_alert=True)
            
        except Exception as e:
            print(f"Error in confirm_send_to_controller_handler: {e}")
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "jm_back_to_application")
    async def back_to_application_handler(callback: CallbackQuery, state: FSMContext):
        """Handle back to application button"""
        try:
            await callback.answer()
            
            # Get current application
            data = await state.get_data()
            current_index = data.get('current_app_index', 0)
            applications = data.get('applications', [])
            
            if not applications or current_index >= len(applications):
                await callback.answer("Ariza topilmadi")
                return
            
            # Show application details again
            await show_application_details(callback, applications[current_index], applications, current_index)
            
        except Exception as e:
            print(f"Error in back_to_application_handler: {e}")
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "jm_back_to_inbox")
    async def back_to_inbox_handler(callback: CallbackQuery, state: FSMContext):
        """Handle back to inbox button"""
        try:
            await callback.answer()
            
            # Show inbox again
            await view_inbox(callback.message, state)
            
        except Exception as e:
            print(f"Error in back_to_inbox_handler: {e}")
            await callback.answer("Xatolik yuz berdi")

    return router

def get_applications_navigation_keyboard(current_index: int, total_applications: int):
    """Create navigation keyboard for applications"""
    keyboard = []
    
    # Navigation row
    nav_buttons = []
    
    # Previous button
    if current_index > 0:
        nav_buttons.append(InlineKeyboardButton(
            text="⬅️ Oldingi",
            callback_data="jm_prev_application"
        ))
    
    # Next button
    if current_index < total_applications - 1:
        nav_buttons.append(InlineKeyboardButton(
            text="Keyingi ➡️",
            callback_data="jm_next_application"
        ))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Action buttons row
    action_buttons = []
    
    # Contact client button
    action_buttons.append(InlineKeyboardButton(
        text="📞 Mijoz bilan bog'lanish",
        callback_data="jm_contact_client"
    ))
    
    # Send to controller button
    action_buttons.append(InlineKeyboardButton(
        text="📤 Controller'ga yuborish",
        callback_data="jm_send_to_controller"
    ))
    
    keyboard.append(action_buttons)
     
    return InlineKeyboardMarkup(inline_keyboard=keyboard)