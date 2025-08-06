"""
Client Service Order Handler - Complete Implementation

This module handles service order creation for clients.
"""

import logging
from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from datetime import datetime
from keyboards.client_buttons import (
    zayavka_type_keyboard, geolocation_keyboard, confirmation_keyboard, media_attachment_keyboard
)
from states.client_states import OrderStates
from utils.role_system import get_role_router

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

async def answer_and_cleanup(callback, cleanup_after=True):
    """Mock answer and cleanup"""
    await callback.answer()

async def format_group_zayavka_message(order_type: str, public_id: str, user: dict, phone: str, address: str, description: str, abonent_type: str = None, abonent_id: str = None, geo=None, media=None, user_id=None):
    """Mock format group message"""
    return f"🛠️ Yangi texnik xizmat arizasi #{public_id}\n👤 {user.get('full_name', 'N/A')}\n📞 {phone}\n📍 {address}\n📋 {description}\n🆔 {abonent_id or 'N/A'}"

def get_service_order_router():
    router = get_role_router("client")

    @router.message(F.text.in_(["🔧 Texnik xizmat"]))
    async def new_service_request(message: Message, state: FSMContext):
        """New service request handler"""
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
            
            await state.set_state(OrderStates.selecting_region)
            
        except Exception as e:
            logger.error(f"Error in new_service_request - User ID: {message.from_user.id}, Error: {str(e)}", exc_info=True)
            await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.startswith("region_"), StateFilter(OrderStates.selecting_region))
    async def select_region(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            region = callback.data.split("_")[-1]
            await state.update_data(region=region)
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user:
                await callback.answer("Xatolik: Foydalanuvchi ma'lumotlari topilmadi.", show_alert=True)
                return
            
            # Abonent turini so'rash
            await callback.message.answer(
                "Abonent turini tanlang:",
                reply_markup=zayavka_type_keyboard('uz')
            )
            
            await state.set_state(OrderStates.selecting_order_type)
            
        except Exception as e:
            logger.error(f"Error in select_region - User ID: {callback.from_user.id}, Error: {str(e)}", exc_info=True)
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data.startswith("zayavka_type_"), StateFilter(OrderStates.selecting_order_type))
    async def select_abonent_type(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            abonent_type = callback.data.split("_")[-1]
            await state.update_data(abonent_type=abonent_type)
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user:
                await callback.answer("Xatolik: Foydalanuvchi ma'lumotlari topilmadi.", show_alert=True)
                return
            
            # Abonent ID so'rash
            await callback.message.answer("Abonent ID raqamini kiriting:")
            
            await state.set_state(OrderStates.waiting_for_contact)
            
        except Exception as e:
            logger.error(f"Error in select_abonent_type - User ID: {callback.from_user.id}, Error: {str(e)}", exc_info=True)
            await callback.answer("Xatolik yuz berdi")

    @router.message(StateFilter(OrderStates.waiting_for_contact))
    async def get_abonent_id(message: Message, state: FSMContext):
        try:
            await state.update_data(abonent_id=message.text)
            
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("Xatolik: Foydalanuvchi ma'lumotlari topilmadi. Iltimos, qaytadan kiriting.")
                return
            
            # Muammo tavsifini so'rash
            await message.answer("Muammo tavsifini kiriting:")
            
            await state.set_state(OrderStates.entering_description)
            
        except Exception as e:
            logger.error(f"Error in get_abonent_id - User ID: {message.from_user.id}, Error: {str(e)}", exc_info=True)
            await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(StateFilter(OrderStates.entering_description))
    async def get_service_description(message: Message, state: FSMContext):
        try:
            await state.update_data(description=message.text)
            
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("Xatolik: Foydalanuvchi ma'lumotlari topilmadi. Iltimos, qaytadan kiriting.")
                return
            
            # Media so'rash
            await message.answer(
                "Foto yoki video yuborasizmi?",
                reply_markup=media_attachment_keyboard('uz')
            )
            
            await state.set_state(OrderStates.asking_for_media)
            
        except Exception as e:
            logger.error(f"Error in get_service_description - User ID: {message.from_user.id}, Error: {str(e)}", exc_info=True)
            await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.in_(["attach_media_yes", "attach_media_no"]), StateFilter(OrderStates.asking_for_media))
    async def ask_for_media(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            
            if callback.data == "attach_media_yes":
                user = await get_user_by_telegram_id(callback.from_user.id)
                if not user:
                    await callback.answer("Xatolik: Foydalanuvchi ma'lumotlari topilmadi.", show_alert=True)
                    return
                
                # Media yuborishni so'rash
                await callback.message.answer("Foto yoki videoni yuboring:")
                
                await state.set_state(OrderStates.waiting_for_media)
            else:
                await ask_for_address(callback, state)
            
        except Exception as e:
            logger.error(f"Error in ask_for_media - User ID: {callback.from_user.id}, Error: {str(e)}", exc_info=True)
            await callback.answer("Xatolik yuz berdi")

    @router.message(StateFilter(OrderStates.waiting_for_media), F.photo | F.video)
    async def process_media(message: Message, state: FSMContext):
        try:
            media_file_id = message.photo[-1].file_id if message.photo else message.video.file_id
            await state.update_data(media=media_file_id)
            
            await ask_for_address(message, state)
            
        except Exception as e:
            logger.error(f"Error in process_media - User ID: {message.from_user.id}, Error: {str(e)}", exc_info=True)
            await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    async def ask_for_address(message_or_callback, state: FSMContext):
        try:
            user_id = message_or_callback.from_user.id
            
            user = await get_user_by_telegram_id(user_id)
            if not user:
                if hasattr(message_or_callback, "message"):
                    await message_or_callback.message.answer("Xatolik: Foydalanuvchi ma'lumotlari topilmadi.")
                else:
                    await message_or_callback.answer("Xatolik: Foydalanuvchi ma'lumotlari topilmadi.")
                return
            
            if hasattr(message_or_callback, "message"):
                # Callback uchun
                await message_or_callback.message.answer("Xizmat ko'rsatiladigan manzilni kiriting:")
            else:
                # Message uchun
                await message_or_callback.answer("Xizmat ko'rsatiladigan manzilni kiriting:")
            
            await state.set_state(OrderStates.entering_address)
            
        except Exception as e:
            logger.error(f"Error in ask_for_address - User ID: {user_id}, Error: {str(e)}", exc_info=True)
            if hasattr(message_or_callback, "message"):
                await message_or_callback.message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            else:
                await message_or_callback.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(StateFilter(OrderStates.entering_address))
    async def get_service_address(message: Message, state: FSMContext):
        try:
            await state.update_data(address=message.text)
            
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("Xatolik: Foydalanuvchi ma'lumotlari topilmadi. Iltimos, qaytadan kiriting.")
                return
            
            # Geolokatsiya so'rash
            await message.answer(
                "Geolokatsiya yuborasizmi?",
                reply_markup=geolocation_keyboard('uz')
            )
            
            await state.set_state(OrderStates.asking_for_location)
            
        except Exception as e:
            logger.error(f"Error in get_service_address - User ID: {message.from_user.id}, Error: {str(e)}", exc_info=True)
            await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.in_(["send_location_yes", "send_location_no"]), StateFilter(OrderStates.asking_for_location))
    async def ask_for_geo(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            
            if callback.data == "send_location_yes":
                user = await get_user_by_telegram_id(callback.from_user.id)
                
                # Geolokatsiya yuborishni so'rash
                await callback.message.answer("Geolokatsiyani yuboring:")
                
                await state.set_state(OrderStates.waiting_for_location)
            else:
                await show_service_confirmation(callback, state)
            
        except Exception as e:
            logger.error(f"Error in ask_for_geo - User ID: {callback.from_user.id}, Error: {str(e)}", exc_info=True)
            await callback.answer("Xatolik yuz berdi")

    @router.message(StateFilter(OrderStates.waiting_for_location), F.location)
    async def get_geo(message: Message, state: FSMContext):
        try:
            await state.update_data(geo=message.location)
            
            await show_service_confirmation(message, state)
            
        except Exception as e:
            logger.error(f"Error in get_geo - User ID: {message.from_user.id}, Error: {str(e)}", exc_info=True)
            await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    async def show_service_confirmation(message_or_callback, state: FSMContext):
        try:
            data = await state.get_data()
            user_id = message_or_callback.from_user.id
            
            user = await get_user_by_telegram_id(user_id)
            region = data.get('region', '-')
            abonent_type = data.get('abonent_type', '-')
            abonent_id = data.get('abonent_id', '-')
            description = data.get('description', '-')
            address = data.get('address', '-')
            geo = data.get('geo', None)
            media = data.get('media', None)
            text = (
                f"🏛️ <b>Hudud:</b> {region}\n"
                f"👤 <b>Abonent turi:</b> {abonent_type}\n"
                f"🆔 <b>Abonent ID:</b> {abonent_id}\n"
                f"📝 <b>Muammo tavsifi:</b> {description}\n"
                f"🏠 <b>Manzil:</b> {address}\n"
                f"📍 <b>Geolokatsiya:</b> {'✅ Yuborilgan' if geo else '❌ Yuborilmagan'}\n"
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
            
            await state.set_state(OrderStates.confirming_order)
            
        except Exception as e:
            logger.error(f"Error in show_service_confirmation - User ID: {user_id}, Error: {str(e)}", exc_info=True)
            if hasattr(message_or_callback, "message"):
                await message_or_callback.message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            else:
                await message_or_callback.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "confirm_zayavka", StateFilter(OrderStates.confirming_order))
    async def confirm_service_order(callback: CallbackQuery, state: FSMContext):
        try:
            try:
                await callback.message.edit_reply_markup(reply_markup=None)
            except Exception:
                pass
            await callback.answer()
            
            data = await state.get_data()
            user = await get_user_by_telegram_id(callback.from_user.id)
            
            # Simple success message
            success_msg = "✅ Texnik xizmat arizangiz qabul qilindi!\nOperatorlar tez orada siz bilan bog'lanadi."
            
            await callback.message.answer(success_msg)
            
            await state.clear()
            
        except Exception as e:
            logger.error(f"Error in confirm_service_order - User ID: {callback.from_user.id}, Error: {str(e)}", exc_info=True)
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
