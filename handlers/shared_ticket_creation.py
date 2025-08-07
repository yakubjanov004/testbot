"""
Shared Ticket Creation Module

This module provides shared functionality for ticket creation across all roles.
It handles both connection requests and technical service requests.
"""

import logging
from datetime import datetime
from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from keyboards.client_buttons import (
    zayavka_type_keyboard, geolocation_keyboard, confirmation_keyboard, media_attachment_keyboard
)

logger = logging.getLogger(__name__)

# Mock functions for database operations
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'client',
        'language': 'uz',
        'full_name': 'Test User',
        'phone_number': '+998901234567'
    }

async def create_ticket_in_database(ticket_data: dict):
    """Mock database ticket creation"""
    ticket_id = f"TICKET_{datetime.now().timestamp()}"
    return {
        'id': ticket_id,
        'public_id': ticket_id[:8],
        'status': 'new',
        'created_by': ticket_data['created_by'],
        'created_at': datetime.now(),
        **ticket_data
    }

async def send_ticket_to_role(ticket_data: dict, target_role: str):
    """Mock sending ticket to specific role"""
    logger.info(f"Sending ticket {ticket_data.get('public_id')} to role: {target_role}")
    return True

class SharedTicketStates(StatesGroup):
    """Shared states for ticket creation"""
    selecting_region = State()
    selecting_ticket_type = State()
    selecting_connection_type = State()
    selecting_tariff = State()
    entering_abonent_id = State()
    entering_description = State()
    asking_for_media = State()
    waiting_for_media = State()
    entering_address = State()
    asking_for_geo = State()
    waiting_for_geo = State()
    confirming_ticket = State()

def get_regions_keyboard():
    """Hududlar keyboard"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Toshkent shahri", callback_data="region_tashkent_city"),
            InlineKeyboardButton(text="Toshkent viloyati", callback_data="region_tashkent_region")
        ],
        [
            InlineKeyboardButton(text="Andijon", callback_data="region_andijon"),
            InlineKeyboardButton(text="Farg'ona", callback_data="region_fergana")
        ],
        [
            InlineKeyboardButton(text="Namangan", callback_data="region_namangan"),
            InlineKeyboardButton(text="Sirdaryo", callback_data="region_sirdaryo")
        ],
        [
            InlineKeyboardButton(text="Jizzax", callback_data="region_jizzax"),
            InlineKeyboardButton(text="Samarqand", callback_data="region_samarkand")
        ],
        [
            InlineKeyboardButton(text="Buxoro", callback_data="region_bukhara"),
            InlineKeyboardButton(text="Navoiy", callback_data="region_navoi")
        ],
        [
            InlineKeyboardButton(text="Qashqadaryo", callback_data="region_kashkadarya"),
            InlineKeyboardButton(text="Surxondaryo", callback_data="region_surkhandarya")
        ],
        [
            InlineKeyboardButton(text="Xorazm", callback_data="region_khorezm"),
            InlineKeyboardButton(text="Qoraqalpog'iston", callback_data="region_karakalpakstan")
        ]
    ])
    return keyboard

def get_ticket_type_keyboard(role: str, lang: str = 'uz'):
    """Get ticket type keyboard based on role permissions"""
    connection_text = "🔌 Ulanish uchun ariza" if lang == "uz" else "🔌 Заявка на подключение"
    technical_text = "🔧 Texnik xizmat" if lang == "uz" else "🔧 Техническая служба"
    
    keyboard = []
    
    # Role-based permissions
    if role in ['client', 'manager', 'controller', 'call_center', 'call_center_supervisor']:
        # All roles can create both types
        keyboard = [
            [
                InlineKeyboardButton(text=connection_text, callback_data="ticket_type_connection"),
                InlineKeyboardButton(text=technical_text, callback_data="ticket_type_technical")
            ]
        ]
    elif role == 'junior_manager':
        # Junior manager can only create connection requests
        keyboard = [
            [InlineKeyboardButton(text=connection_text, callback_data="ticket_type_connection")]
        ]
    else:
        # Default: both types
        keyboard = [
            [
                InlineKeyboardButton(text=connection_text, callback_data="ticket_type_connection"),
                InlineKeyboardButton(text=technical_text, callback_data="ticket_type_technical")
            ]
        ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def start_ticket_creation(message: Message, state: FSMContext, role: str):
    """Start ticket creation process for any role"""
    try:
        user = await get_user_by_telegram_id(message.from_user.id)
        if not user:
            await message.answer("Xatolik: Foydalanuvchi ma'lumotlari topilmadi.")
            return
        
        # Store role information
        await state.update_data(created_by_role=role, created_by_user_id=message.from_user.id)
        
        # Ask for region
        await message.answer(
            "Hududni tanlang:",
            reply_markup=get_regions_keyboard()
        )
        
        await state.set_state(SharedTicketStates.selecting_region)
        
    except Exception as e:
        logger.error(f"Error in start_ticket_creation - User ID: {message.from_user.id}, Error: {str(e)}", exc_info=True)
        await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

async def handle_region_selection(callback: CallbackQuery, state: FSMContext):
    """Handle region selection"""
    try:
        await callback.answer()
        region = callback.data.split("_")[-1]
        await state.update_data(region=region)
        
        data = await state.get_data()
        role = data.get('created_by_role', 'client')
        
        # Ask for ticket type
        await callback.message.answer(
            "Ariza turini tanlang:",
            reply_markup=get_ticket_type_keyboard(role)
        )
        
        await state.set_state(SharedTicketStates.selecting_ticket_type)
        
    except Exception as e:
        logger.error(f"Error in handle_region_selection - User ID: {callback.from_user.id}, Error: {str(e)}", exc_info=True)
        await callback.answer("Xatolik yuz berdi", show_alert=True)

async def handle_ticket_type_selection(callback: CallbackQuery, state: FSMContext):
    """Handle ticket type selection"""
    try:
        await callback.answer()
        ticket_type = callback.data.split("_")[-1]
        await state.update_data(ticket_type=ticket_type)
        
        if ticket_type == "connection":
            # Connection request flow
            await callback.message.answer(
                "Ulanish turini tanlang:",
                reply_markup=zayavka_type_keyboard('uz')
            )
            await state.set_state(SharedTicketStates.selecting_connection_type)
        else:
            # Technical service flow
            await callback.message.answer("Abonent ID raqamini kiriting:")
            await state.set_state(SharedTicketStates.entering_abonent_id)
        
    except Exception as e:
        logger.error(f"Error in handle_ticket_type_selection - User ID: {callback.from_user.id}, Error: {str(e)}", exc_info=True)
        await callback.answer("Xatolik yuz berdi")

async def handle_connection_type_selection(callback: CallbackQuery, state: FSMContext):
    """Handle connection type selection"""
    try:
        await callback.answer()
        connection_type = callback.data.split("_")[-1]
        await state.update_data(connection_type=connection_type)
        
        # Ask for tariff
        await callback.message.answer(
            "Tariflardan birini tanlang:",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Standard", callback_data="tariff_standard"),
                        InlineKeyboardButton(text="Yangi", callback_data="tariff_new")
                    ]
                ]
            )
        )
        await state.set_state(SharedTicketStates.selecting_tariff)
        
    except Exception as e:
        logger.error(f"Error in handle_connection_type_selection - User ID: {callback.from_user.id}, Error: {str(e)}", exc_info=True)
        await callback.answer("Xatolik yuz berdi")

async def handle_tariff_selection(callback: CallbackQuery, state: FSMContext):
    """Handle tariff selection"""
    try:
        await callback.answer()
        tariff = "Standard" if callback.data == "tariff_standard" else "Yangi"
        await state.update_data(selected_tariff=tariff)
        
        await callback.message.answer("Manzilingizni kiriting:")
        await state.set_state(SharedTicketStates.entering_address)
        
    except Exception as e:
        logger.error(f"Error in handle_tariff_selection - User ID: {callback.from_user.id}, Error: {str(e)}", exc_info=True)
        await callback.answer("Xatolik yuz berdi")

async def handle_abonent_id_input(message: Message, state: FSMContext):
    """Handle abonent ID input for technical service"""
    try:
        await state.update_data(abonent_id=message.text)
        
        await message.answer("Muammo tavsifini kiriting:")
        await state.set_state(SharedTicketStates.entering_description)
        
    except Exception as e:
        logger.error(f"Error in handle_abonent_id_input - User ID: {message.from_user.id}, Error: {str(e)}", exc_info=True)
        await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

async def handle_description_input(message: Message, state: FSMContext):
    """Handle description input"""
    try:
        await state.update_data(description=message.text)
        
        data = await state.get_data()
        ticket_type = data.get('ticket_type')
        
        if ticket_type == "technical":
            # For technical service, ask for media
            await message.answer(
                "Foto yoki video yuborasizmi?",
                reply_markup=media_attachment_keyboard('uz')
            )
            await state.set_state(SharedTicketStates.asking_for_media)
        else:
            # For connection request, ask for address
            await message.answer("Manzilingizni kiriting:")
            await state.set_state(SharedTicketStates.entering_address)
        
    except Exception as e:
        logger.error(f"Error in handle_description_input - User ID: {message.from_user.id}, Error: {str(e)}", exc_info=True)
        await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

async def handle_media_question(callback: CallbackQuery, state: FSMContext):
    """Handle media attachment question"""
    try:
        await callback.answer()
        
        if callback.data == "attach_media_yes":
            await callback.message.answer("Foto yoki videoni yuboring:")
            await state.set_state(SharedTicketStates.waiting_for_media)
        else:
            await callback.message.answer("Xizmat ko'rsatiladigan manzilni kiriting:")
            await state.set_state(SharedTicketStates.entering_address)
        
    except Exception as e:
        logger.error(f"Error in handle_media_question - User ID: {callback.from_user.id}, Error: {str(e)}", exc_info=True)
        await callback.answer("Xatolik yuz berdi")

async def handle_media_input(message: Message, state: FSMContext):
    """Handle media input"""
    try:
        media_file_id = message.photo[-1].file_id if message.photo else message.video.file_id
        await state.update_data(media=media_file_id)
        
        await message.answer("Xizmat ko'rsatiladigan manzilni kiriting:")
        await state.set_state(SharedTicketStates.entering_address)
        
    except Exception as e:
        logger.error(f"Error in handle_media_input - User ID: {message.from_user.id}, Error: {str(e)}", exc_info=True)
        await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

async def handle_address_input(message: Message, state: FSMContext):
    """Handle address input"""
    try:
        await state.update_data(address=message.text)
        
        await message.answer(
            "Geolokatsiya yuborasizmi?",
            reply_markup=geolocation_keyboard('uz')
        )
        
        await state.set_state(SharedTicketStates.asking_for_geo)
        
    except Exception as e:
        logger.error(f"Error in handle_address_input - User ID: {message.from_user.id}, Error: {str(e)}", exc_info=True)
        await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

async def handle_geo_question(callback: CallbackQuery, state: FSMContext):
    """Handle geolocation question"""
    try:
        await callback.answer()
        
        if callback.data == "send_location_yes":
            await callback.message.answer("Geolokatsiyani yuboring:")
            await state.set_state(SharedTicketStates.waiting_for_geo)
        else:
            await show_ticket_confirmation(callback, state)
        
    except Exception as e:
        logger.error(f"Error in handle_geo_question - User ID: {callback.from_user.id}, Error: {str(e)}", exc_info=True)
        await callback.answer("Xatolik yuz berdi")

async def handle_geo_input(message: Message, state: FSMContext):
    """Handle geolocation input"""
    try:
        await state.update_data(geo=message.location)
        
        await show_ticket_confirmation(message, state)
        
    except Exception as e:
        logger.error(f"Error in handle_geo_input - User ID: {message.from_user.id}, Error: {str(e)}", exc_info=True)
        await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

async def show_ticket_confirmation(message_or_callback, state: FSMContext):
    """Show ticket confirmation"""
    try:
        data = await state.get_data()
        user_id = message_or_callback.from_user.id if hasattr(message_or_callback, 'from_user') else message_or_callback.message.from_user.id
        
        user = await get_user_by_telegram_id(user_id)
        region = data.get('region', '-')
        ticket_type = data.get('ticket_type', '-')
        
        if ticket_type == "connection":
            connection_type = data.get('connection_type', '-')
            tariff = data.get('selected_tariff', '-')
            address = data.get('address', '-')
            
            text = (
                f"🏛️ <b>Hudud:</b> {region}\n"
                f"🔌 <b>Ulanish turi:</b> {connection_type}\n"
                f"💳 <b>Tarif:</b> {tariff}\n"
                f"🏠 <b>Manzil:</b> {address}\n"
                f"📍 <b>Geolokatsiya:</b> {'✅ Yuborilgan' if data.get('geo') else '❌ Yuborilmagan'}"
            )
        else:
            abonent_id = data.get('abonent_id', '-')
            description = data.get('description', '-')
            address = data.get('address', '-')
            media = data.get('media', None)
            
            text = (
                f"🏛️ <b>Hudud:</b> {region}\n"
                f"👤 <b>Abonent ID:</b> {abonent_id}\n"
                f"📝 <b>Muammo tavsifi:</b> {description}\n"
                f"🏠 <b>Manzil:</b> {address}\n"
                f"📍 <b>Geolokatsiya:</b> {'✅ Yuborilgan' if data.get('geo') else '❌ Yuborilmagan'}\n"
                f"🖼 <b>Media:</b> {'✅ Yuborilgan' if media else '❌ Yuborilmagan'}"
            )
        
        if hasattr(message_or_callback, "message"):
            # Callback uchun
            await message_or_callback.message.answer(
                text,
                parse_mode='HTML',
                reply_markup=confirmation_keyboard('uz')
            )
        else:
            # Message uchun
            await message_or_callback.answer(
                text,
                parse_mode='HTML',
                reply_markup=confirmation_keyboard('uz')
            )
        
        await state.set_state(SharedTicketStates.confirming_ticket)
        
    except Exception as e:
        logger.error(f"Error in show_ticket_confirmation - User ID: {user_id}, Error: {str(e)}", exc_info=True)
        if hasattr(message_or_callback, "message"):
            await message_or_callback.message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
        else:
            await message_or_callback.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

async def confirm_ticket_creation(callback: CallbackQuery, state: FSMContext):
    """Confirm and create ticket"""
    try:
        try:
            await callback.message.edit_reply_markup(reply_markup=None)
        except Exception:
            pass
        await callback.answer()
        
        data = await state.get_data()
        user = await get_user_by_telegram_id(callback.from_user.id)
        
        # Create ticket in database
        ticket_data = {
            'created_by': callback.from_user.id,
            'created_by_role': data.get('created_by_role', 'client'),
            'region': data.get('region'),
            'ticket_type': data.get('ticket_type'),
            'address': data.get('address'),
            'geo': data.get('geo'),
            'media': data.get('media'),
            'description': data.get('description'),
            'abonent_id': data.get('abonent_id'),
            'connection_type': data.get('connection_type'),
            'tariff': data.get('selected_tariff'),
            'status': 'new',
            'created_at': datetime.now()
        }
        
        ticket = await create_ticket_in_database(ticket_data)
        
        # Determine target role based on ticket type and workflow
        target_role = determine_target_role(data.get('ticket_type'), data.get('created_by_role'))
        
        # Send ticket to appropriate role
        await send_ticket_to_role(ticket, target_role)
        
        # Success message
        ticket_type_text = "Ulanish arizasi" if data.get('ticket_type') == "connection" else "Texnik xizmat arizasi"
        success_msg = (
            f"✅ {ticket_type_text} qabul qilindi!\n"
            f"Ariza ID: {ticket['public_id']}\n"
            f"Operatorlar tez orada siz bilan bog'lanadi."
        )
        
        await callback.message.answer(success_msg)
        
        await state.clear()
        
    except Exception as e:
        logger.error(f"Error in confirm_ticket_creation - User ID: {callback.from_user.id}, Error: {str(e)}", exc_info=True)
        await callback.answer("Xatolik yuz berdi")

def determine_target_role(ticket_type: str, created_by_role: str) -> str:
    """Determine which role should receive the ticket based on workflow"""
    if ticket_type == "connection":
        if created_by_role == "client":
            return "manager"  # Client -> Manager
        elif created_by_role == "call_center":
            return "manager"  # Call Center -> Manager
        else:
            return "controller"  # Other roles -> Controller
    else:  # technical
        return "controller"  # All technical requests -> Controller

def get_shared_ticket_router():
    """Get shared ticket creation router"""
    from aiogram import Router
    router = Router()
    
    # Region selection
    router.callback_query(F.data.startswith("region_"), StateFilter(SharedTicketStates.selecting_region))(handle_region_selection)
    
    # Ticket type selection
    router.callback_query(F.data.startswith("ticket_type_"), StateFilter(SharedTicketStates.selecting_ticket_type))(handle_ticket_type_selection)
    
    # Connection type selection
    router.callback_query(F.data.startswith("zayavka_type_"), StateFilter(SharedTicketStates.selecting_connection_type))(handle_connection_type_selection)
    
    # Tariff selection
    router.callback_query(F.data.in_(["tariff_standard", "tariff_new"]), StateFilter(SharedTicketStates.selecting_tariff))(handle_tariff_selection)
    
    # Abonent ID input
    router.message(StateFilter(SharedTicketStates.entering_abonent_id))(handle_abonent_id_input)
    
    # Description input
    router.message(StateFilter(SharedTicketStates.entering_description))(handle_description_input)
    
    # Media question
    router.callback_query(F.data.in_(["attach_media_yes", "attach_media_no"]), StateFilter(SharedTicketStates.asking_for_media))(handle_media_question)
    
    # Media input
    router.message(StateFilter(SharedTicketStates.waiting_for_media), F.photo | F.video)(handle_media_input)
    
    # Address input
    router.message(StateFilter(SharedTicketStates.entering_address))(handle_address_input)
    
    # Geo question
    router.callback_query(F.data.in_(["send_location_yes", "send_location_no"]), StateFilter(SharedTicketStates.asking_for_geo))(handle_geo_question)
    
    # Geo input
    router.message(StateFilter(SharedTicketStates.waiting_for_geo), F.location)(handle_geo_input)
    
    # Confirmation
    router.callback_query(F.data == "confirm_zayavka", StateFilter(SharedTicketStates.confirming_ticket))(confirm_ticket_creation)
    
    return router