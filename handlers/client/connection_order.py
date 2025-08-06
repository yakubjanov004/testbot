"""
Client Connection Order Handler - Complete Implementation

This module handles connection order creation for clients.
"""

import logging
from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from datetime import datetime
from keyboards.client_buttons import (
    zayavka_type_keyboard, geolocation_keyboard, confirmation_keyboard
)
from states.client_states import ConnectionOrderStates
from filters.role_filter import RoleFilter

# Logger sozlash
logger = logging.getLogger(__name__)

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'client',
        'language': 'uz',
        'full_name': 'Test Client',
        'phone_number': '+998901234567'
    }

async def get_users_by_role(role: str):
    """Mock users by role"""
    return [
        {
            'id': 1,
            'full_name': 'Manager 1',
            'role': 'manager',
            'telegram_id': 123456789
        },
        {
            'id': 2,
            'full_name': 'Manager 2',
            'role': 'manager',
            'telegram_id': 987654321
        }
    ]

async def get_user_language(user_id: int) -> str:
    """Mock user language"""
    return 'uz'

async def format_group_zayavka_message(order_type: str, public_id: str, user: dict, phone: str, address: str, description: str, tariff: str, geo=None, media=None):
    """Mock format group message"""
    return f"🔌 Yangi ulanish arizasi #{public_id}\n👤 {user.get('full_name', 'N/A')}\n📞 {phone}\n📍 {address}\n📋 {description}\n💳 {tariff}"

def get_connection_order_router():
    from aiogram import Router
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("client")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🔌 Ulanish uchun ariza"]))
    async def start_connection_order(message: Message, state: FSMContext):
        """Yangi ulanish uchun ariza jarayonini boshlash"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("Xatolik: Foydalanuvchi ma'lumotlari topilmadi. Iltimos, qaytadan kiriting.")
                return
            
            # Hududni so'rash
            await message.answer(
                "Hududni tanlang:",
                reply_markup=get_regions_keyboard()
            )
            
            await state.set_state(ConnectionOrderStates.selecting_region)
            
        except Exception as e:
            logger.error(f"Error in start_connection_order - User ID: {message.from_user.id}, Error: {str(e)}", exc_info=True)
            await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.startswith("region_"), StateFilter(ConnectionOrderStates.selecting_region))
    async def select_region(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            region = callback.data.split("_")[-1]
            await state.update_data(region=region)
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user:
                await callback.answer("Xatolik: Foydalanuvchi ma'lumotlari topilmadi.", show_alert=True)
                return
            
            # Ulanish turini so'rash
            await callback.message.answer(
                "Ulanish turini tanlang:",
                reply_markup=zayavka_type_keyboard('uz')
            )
            
            await state.set_state(ConnectionOrderStates.selecting_connection_type)
            
        except Exception as e:
            logger.error(f"Error in select_region - User ID: {callback.from_user.id}, Error: {str(e)}", exc_info=True)
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("zayavka_type_"), StateFilter(ConnectionOrderStates.selecting_connection_type))
    async def select_connection_type(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            connection_type = callback.data.split("_")[-1]
            await state.update_data(connection_type=connection_type)
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user:
                await callback.answer("Xatolik: Foydalanuvchi ma'lumotlari topilmadi.", show_alert=True)
                return
            
            # Tarifni so'rash
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
            await state.set_state(ConnectionOrderStates.selecting_tariff)
            
        except Exception as e:
            logger.error(f"Error in select_connection_type - User ID: {callback.from_user.id}, Error: {str(e)}", exc_info=True)
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data.in_(["tariff_standard", "tariff_new"]))
    async def select_tariff(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            tariff = "Standard" if callback.data == "tariff_standard" else "Yangi"
            await state.update_data(selected_tariff=tariff)
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user:
                await callback.answer("Xatolik: Foydalanuvchi ma'lumotlari topilmadi.", show_alert=True)
                return
            
            # Manzilni so'rash
            await callback.message.answer("Manzilingizni kiriting:")
            
            await state.set_state(ConnectionOrderStates.entering_address)
            
        except Exception as e:
            logger.error(f"Error in select_tariff - User ID: {callback.from_user.id}, Error: {str(e)}", exc_info=True)
            await callback.answer("Xatolik yuz berdi")

    @router.message(StateFilter(ConnectionOrderStates.entering_address))
    async def get_connection_address(message: Message, state: FSMContext):
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("Xatolik: Foydalanuvchi ma'lumotlari topilmadi. Iltimos, qaytadan kiriting.")
                return
            
            await state.update_data(address=message.text)
            
            # Geolokatsiya so'rash
            await message.answer(
                "Geolokatsiya yuborasizmi?",
                reply_markup=geolocation_keyboard('uz')
            )
            
            await state.set_state(ConnectionOrderStates.asking_for_geo)
            
        except Exception as e:
            logger.error(f"Error in get_connection_address - User ID: {message.from_user.id}, Error: {str(e)}", exc_info=True)
            await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.in_(["send_location_yes", "send_location_no"]), StateFilter(ConnectionOrderStates.asking_for_geo))
    async def ask_for_geo(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            
            if callback.data == "send_location_yes":
                user = await get_user_by_telegram_id(callback.from_user.id)
                if not user:
                    await callback.answer("Xatolik: Foydalanuvchi ma'lumotlari topilmadi.", show_alert=True)
                    return
                
                # Geolokatsiya yuborishni so'rash
                await callback.message.answer("Geolokatsiyani yuboring:")
                
                await state.set_state(ConnectionOrderStates.waiting_for_geo)
            else:
                await finish_connection_order(callback, state, geo=None)
            
        except Exception as e:
            logger.error(f"Error in ask_for_geo - User ID: {callback.from_user.id}, Error: {str(e)}", exc_info=True)
            await callback.answer("Xatolik yuz berdi")

    @router.message(StateFilter(ConnectionOrderStates.waiting_for_geo), F.location)
    async def get_geo(message: Message, state: FSMContext):
        try:
            await state.update_data(geo=message.location)
            
            await finish_connection_order(message, state, geo=message.location)
            
        except Exception as e:
            logger.error(f"Error in get_geo - User ID: {message.from_user.id}, Error: {str(e)}", exc_info=True)
            await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    async def finish_connection_order(message_or_callback, state: FSMContext, geo=None):
        """Complete connection request submission"""
        try:
            data = await state.get_data()
            user_id = message_or_callback.from_user.id if hasattr(message_or_callback, 'from_user') else message_or_callback.message.from_user.id
            
            user = await get_user_by_telegram_id(user_id)
            region = data.get('region', '-')
            connection_type = data.get('connection_type', 'standard')
            tariff = data.get('selected_tariff', 'Standard')
            address = data.get('address', '-')
            
            # Tasdiqlash xabari
            text = (
                f"🏛️ <b>Hudud:</b> {region}\n"
                f"🔌 <b>Ulanish turi:</b> {connection_type}\n"
                f"💳 <b>Tarif:</b> {tariff}\n"
                f"🏠 <b>Manzil:</b> {address}\n"
                f"📍 <b>Geolokatsiya:</b> {'✅ Yuborilgan' if geo else '❌ Yuborilmagan'}"
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
            
            await state.set_state(ConnectionOrderStates.confirming_connection)
            
        except Exception as e:
            logger.error(f"Error in finish_connection_order - User ID: {user_id}, Error: {str(e)}", exc_info=True)
            if hasattr(message_or_callback, "message"):
                await message_or_callback.message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            else:
                await message_or_callback.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "confirm_zayavka", StateFilter(ConnectionOrderStates.confirming_connection))
    async def confirm_connection_order(callback: CallbackQuery, state: FSMContext):
        try:
            try:
                await callback.message.edit_reply_markup(reply_markup=None)
            except Exception:
                pass
            await callback.answer()
            
            data = await state.get_data()
            user = await get_user_by_telegram_id(callback.from_user.id)
            
            # Generate request ID
            request_id = f"UL_{callback.from_user.id}_{int(datetime.now().timestamp())}"
            
            # Success message
            success_msg = (
                f"✅ Ulanish arizangiz qabul qilindi!\n"
                f"Ariza ID: {request_id[:8]}\n"
                f"Menejerlar tez orada siz bilan bog'lanadi."
            )
            
            await callback.message.answer(success_msg)
            
            await state.clear()
            
        except Exception as e:
            logger.error(f"Error in confirm_connection_order - User ID: {callback.from_user.id}, Error: {str(e)}", exc_info=True)
            await callback.answer("Xatolik yuz berdi")

    return router

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
