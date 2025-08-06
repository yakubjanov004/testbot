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
    zayavka_type_keyboard, geolocation_keyboard, confirmation_keyboard, media_attachment_keyboard,
    get_main_menu_keyboard, get_back_keyboard
)
from states.client_states import OrderStates, MainMenuStates
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

    @router.message(F.text.in_(["🔧 Texnik xizmat", "🔧 Техническая служба"]))
    async def new_service_request(message: Message, state: FSMContext):
        """New service request handler"""
        try:
            # Get user data from state or database
            state_data = await state.get_data()
            user_lang = state_data.get('user_lang', 'uz')
            
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("Xatolik: Foydalanuvchi ma'lumotlari topilmadi. Iltimos, qaytadan kiriting.")
                return
            
            # Clear previous order data
            await state.update_data(
                order_type=None,
                region=None,
                description=None,
                media=[],
                location=None,
                address=None,
                abonent_type=None,
                abonent_id=None
            )
            
            # Hududni so'rash
            region_text = (
                "📍 Hududingizni tanlang:"
                if user_lang == 'uz' else
                "📍 Выберите ваш регион:"
            )
            
            await message.answer(
                text=region_text,
                reply_markup=get_regions_keyboard()
            )
            
            await state.set_state(OrderStates.selecting_region)
            
        except Exception as e:
            logger.error(f"Error in new_service_request - User ID: {message.from_user.id}, Error: {str(e)}", exc_info=True)
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.startswith("region_"), StateFilter(OrderStates.selecting_region))
    async def select_region(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            region = callback.data.split("_", 1)[1]
            await state.update_data(region=region)
            
            # Get user language from state
            state_data = await state.get_data()
            user_lang = state_data.get('user_lang', 'uz')
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user:
                await callback.answer("Xatolik: Foydalanuvchi ma'lumotlari topilmadi.", show_alert=True)
                return
            
            # Abonent turini so'rash
            abonent_text = (
                "👤 Abonent turini tanlang:"
                if user_lang == 'uz' else
                "👤 Выберите тип абонента:"
            )
            
            await callback.message.edit_text(
                text=abonent_text,
                reply_markup=get_abonent_type_keyboard(user_lang)
            )
            
            await state.set_state(OrderStates.selecting_order_type)
            
        except Exception as e:
            logger.error(f"Error in select_region: {str(e)}", exc_info=True)
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.in_(["abonent_physical", "abonent_legal"]), StateFilter(OrderStates.selecting_order_type))
    async def select_abonent_type(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            abonent_type = "physical" if callback.data == "abonent_physical" else "legal"
            await state.update_data(abonent_type=abonent_type)
            
            # Get user language from state
            state_data = await state.get_data()
            user_lang = state_data.get('user_lang', 'uz')
            
            # Abonent ID so'rash
            abonent_id_text = (
                "🆔 Abonent ID raqamini kiriting:"
                if user_lang == 'uz' else
                "🆔 Введите ID абонента:"
            )
            
            await callback.message.edit_text(
                text=abonent_id_text,
                reply_markup=get_back_keyboard(user_lang)
            )
            
            await state.set_state(OrderStates.waiting_for_contact)
            
        except Exception as e:
            logger.error(f"Error in select_abonent_type: {str(e)}", exc_info=True)
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.message(StateFilter(OrderStates.waiting_for_contact))
    async def get_abonent_id(message: Message, state: FSMContext):
        try:
            # Check if it's a back button
            if message.text in ["🏠 Asosiy menyu", "🏠 Главное меню"]:
                await state.clear()
                await message.answer(
                    "🏠 Asosiy menyu",
                    reply_markup=get_main_menu_keyboard('uz')
                )
                await state.set_state(MainMenuStates.main_menu)
                return
            
            # Save abonent ID
            await state.update_data(abonent_id=message.text)
            
            # Get user language from state
            state_data = await state.get_data()
            user_lang = state_data.get('user_lang', 'uz')
            
            # Muammo tavsifini so'rash
            description_text = (
                "📝 Muammoni batafsil yozing:"
                if user_lang == 'uz' else
                "📝 Опишите проблему подробно:"
            )
            
            await message.answer(
                text=description_text,
                reply_markup=get_back_keyboard(user_lang)
            )
            
            await state.set_state(OrderStates.entering_description)
            
        except Exception as e:
            logger.error(f"Error in get_abonent_id: {str(e)}", exc_info=True)
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(StateFilter(OrderStates.entering_description))
    async def get_service_description(message: Message, state: FSMContext):
        try:
            # Check if it's a back button
            if message.text in ["🏠 Asosiy menyu", "🏠 Главное меню"]:
                await state.clear()
                await message.answer(
                    "🏠 Asosiy menyu",
                    reply_markup=get_main_menu_keyboard('uz')
                )
                await state.set_state(MainMenuStates.main_menu)
                return
            
            # Save description
            await state.update_data(description=message.text)
            
            # Get user language from state
            state_data = await state.get_data()
            user_lang = state_data.get('user_lang', 'uz')
            
            # Media qo'shishni so'rash
            media_text = (
                "📷 Rasm yoki video qo'shmoqchimisiz?"
                if user_lang == 'uz' else
                "📷 Хотите добавить фото или видео?"
            )
            
            await message.answer(
                text=media_text,
                reply_markup=media_attachment_keyboard(user_lang)
            )
            
            await state.set_state(OrderStates.asking_for_media)
            
        except Exception as e:
            logger.error(f"Error in get_service_description: {str(e)}", exc_info=True)
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.in_(["add_media", "skip_media"]), StateFilter(OrderStates.asking_for_media))
    async def handle_media_choice(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            
            # Get user language from state
            state_data = await state.get_data()
            user_lang = state_data.get('user_lang', 'uz')
            
            if callback.data == "add_media":
                media_instruction_text = (
                    "📸 Rasm yoki video yuboring (maksimum 5 ta):"
                    if user_lang == 'uz' else
                    "📸 Отправьте фото или видео (максимум 5):"
                )
                
                await callback.message.edit_text(
                    text=media_instruction_text
                )
                await state.set_state(OrderStates.waiting_for_media)
            else:
                # Skip media, go to address
                address_text = (
                    "📍 To'liq manzilingizni kiriting:"
                    if user_lang == 'uz' else
                    "📍 Введите ваш полный адрес:"
                )
                
                await callback.message.edit_text(
                    text=address_text
                )
                await state.set_state(OrderStates.entering_address)
                
        except Exception as e:
            logger.error(f"Error in handle_media_choice: {str(e)}", exc_info=True)
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.message(StateFilter(OrderStates.waiting_for_media))
    async def handle_media(message: Message, state: FSMContext):
        try:
            state_data = await state.get_data()
            media_list = state_data.get('media', [])
            user_lang = state_data.get('user_lang', 'uz')
            
            if message.photo:
                media_list.append({'type': 'photo', 'file_id': message.photo[-1].file_id})
            elif message.video:
                media_list.append({'type': 'video', 'file_id': message.video.file_id})
            else:
                await message.answer("⚠️ Faqat rasm yoki video yuboring!")
                return
            
            await state.update_data(media=media_list)
            
            if len(media_list) >= 5:
                # Maximum reached, go to address
                address_text = (
                    "📍 To'liq manzilingizni kiriting:"
                    if user_lang == 'uz' else
                    "📍 Введите ваш полный адрес:"
                )
                
                await message.answer(
                    text=address_text,
                    reply_markup=get_back_keyboard(user_lang)
                )
                await state.set_state(OrderStates.entering_address)
            else:
                # Ask for more media
                more_media_text = (
                    f"✅ {len(media_list)} ta media qo'shildi. Yana qo'shish yoki davom etish:"
                    if user_lang == 'uz' else
                    f"✅ Добавлено {len(media_list)} медиа. Добавить еще или продолжить:"
                )
                
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="➕ Yana qo'shish" if user_lang == 'uz' else "➕ Добавить еще",
                            callback_data="add_more_media"
                        ),
                        InlineKeyboardButton(
                            text="➡️ Davom etish" if user_lang == 'uz' else "➡️ Продолжить",
                            callback_data="continue_without_media"
                        )
                    ]
                ])
                
                await message.answer(more_media_text, reply_markup=keyboard)
                
        except Exception as e:
            logger.error(f"Error in handle_media: {str(e)}", exc_info=True)
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "continue_without_media", StateFilter(OrderStates.waiting_for_media))
    async def continue_without_media(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            
            # Get user language from state
            state_data = await state.get_data()
            user_lang = state_data.get('user_lang', 'uz')
            
            address_text = (
                "📍 To'liq manzilingizni kiriting:"
                if user_lang == 'uz' else
                "📍 Введите ваш полный адрес:"
            )
            
            await callback.message.answer(
                text=address_text,
                reply_markup=get_back_keyboard(user_lang)
            )
            await state.set_state(OrderStates.entering_address)
            
        except Exception as e:
            logger.error(f"Error in continue_without_media: {str(e)}", exc_info=True)
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.message(StateFilter(OrderStates.entering_address))
    async def get_service_address(message: Message, state: FSMContext):
        try:
            # Check if it's a back button
            if message.text in ["🏠 Asosiy menyu", "🏠 Главное меню"]:
                await state.clear()
                await message.answer(
                    "🏠 Asosiy menyu",
                    reply_markup=get_main_menu_keyboard('uz')
                )
                await state.set_state(MainMenuStates.main_menu)
                return
            
            # Save address
            await state.update_data(address=message.text)
            
            # Get user language from state
            state_data = await state.get_data()
            user_lang = state_data.get('user_lang', 'uz')
            
            # Geolokatsiya so'rash
            geo_text = (
                "📍 Geolokatsiyangizni yuboring (ixtiyoriy):"
                if user_lang == 'uz' else
                "📍 Отправьте вашу геолокацию (необязательно):"
            )
            
            await message.answer(
                text=geo_text,
                reply_markup=geolocation_keyboard(user_lang)
            )
            
            await state.set_state(OrderStates.asking_for_location)
            
        except Exception as e:
            logger.error(f"Error in get_service_address: {str(e)}", exc_info=True)
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(StateFilter(OrderStates.asking_for_location))
    async def get_geo(message: Message, state: FSMContext):
        try:
            if message.location:
                await state.update_data(
                    location={
                        'latitude': message.location.latitude,
                        'longitude': message.location.longitude
                    }
                )
            
            # Show confirmation
            await show_order_confirmation(message, state)
            
        except Exception as e:
            logger.error(f"Error in get_geo: {str(e)}", exc_info=True)
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "skip_geo", StateFilter(OrderStates.asking_for_location))
    async def skip_geo(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            await show_order_confirmation(callback.message, state)
            
        except Exception as e:
            logger.error(f"Error in skip_geo: {str(e)}", exc_info=True)
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    async def show_order_confirmation(message: Message, state: FSMContext):
        """Show order confirmation"""
        try:
            state_data = await state.get_data()
            user_lang = state_data.get('user_lang', 'uz')
            
            # Prepare confirmation text
            confirmation_text = (
                "✅ Buyurtmangiz tayyor:\n\n"
                f"📍 Hudud: {state_data.get('region', 'N/A')}\n"
                f"👤 Abonent turi: {'Jismoniy shaxs' if state_data.get('abonent_type') == 'physical' else 'Yuridik shaxs'}\n"
                f"🆔 Abonent ID: {state_data.get('abonent_id', 'N/A')}\n"
                f"📝 Muammo: {state_data.get('description', 'N/A')}\n"
                f"📍 Manzil: {state_data.get('address', 'N/A')}\n"
                f"📸 Media: {len(state_data.get('media', []))} ta\n"
                f"📍 Geolokatsiya: {'✅ Yuborildi' if state_data.get('location') else '❌ Yuborilmadi'}\n\n"
                "Tasdiqlaysizmi?"
                if user_lang == 'uz' else
                "✅ Ваш заказ готов:\n\n"
                f"📍 Регион: {state_data.get('region', 'N/A')}\n"
                f"👤 Тип абонента: {'Физическое лицо' if state_data.get('abonent_type') == 'physical' else 'Юридическое лицо'}\n"
                f"🆔 ID абонента: {state_data.get('abonent_id', 'N/A')}\n"
                f"📝 Проблема: {state_data.get('description', 'N/A')}\n"
                f"📍 Адрес: {state_data.get('address', 'N/A')}\n"
                f"📸 Медиа: {len(state_data.get('media', []))} шт\n"
                f"📍 Геолокация: {'✅ Отправлена' if state_data.get('location') else '❌ Не отправлена'}\n\n"
                "Подтверждаете?"
            )
            
            await message.answer(
                text=confirmation_text,
                reply_markup=confirmation_keyboard(user_lang)
            )
            
            await state.set_state(OrderStates.confirming_order)
            
        except Exception as e:
            logger.error(f"Error in show_order_confirmation: {str(e)}", exc_info=True)
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.in_(["confirm_order", "cancel_order"]), StateFilter(OrderStates.confirming_order))
    async def handle_order_confirmation(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            
            state_data = await state.get_data()
            user_lang = state_data.get('user_lang', 'uz')
            
            if callback.data == "confirm_order":
                # Create order (mock)
                order_id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                
                success_text = (
                    f"✅ Buyurtmangiz qabul qilindi!\n\n"
                    f"🆔 Buyurtma raqami: {order_id}\n\n"
                    f"Tez orada siz bilan bog'lanamiz!"
                    if user_lang == 'uz' else
                    f"✅ Ваш заказ принят!\n\n"
                    f"🆔 Номер заказа: {order_id}\n\n"
                    f"Мы свяжемся с вами в ближайшее время!"
                )
                
                await callback.message.edit_text(success_text)
                
                # Return to main menu after 3 seconds
                await asyncio.sleep(3)
                await callback.message.answer(
                    "🏠 Asosiy menyu" if user_lang == 'uz' else "🏠 Главное меню",
                    reply_markup=get_main_menu_keyboard(user_lang)
                )
                await state.clear()
                await state.set_state(MainMenuStates.main_menu)
                
            else:
                # Cancel order
                cancel_text = (
                    "❌ Buyurtma bekor qilindi"
                    if user_lang == 'uz' else
                    "❌ Заказ отменен"
                )
                
                await callback.message.edit_text(cancel_text)
                
                await callback.message.answer(
                    "🏠 Asosiy menyu" if user_lang == 'uz' else "🏠 Главное меню",
                    reply_markup=get_main_menu_keyboard(user_lang)
                )
                await state.clear()
                await state.set_state(MainMenuStates.main_menu)
                
        except Exception as e:
            logger.error(f"Error in handle_order_confirmation: {str(e)}", exc_info=True)
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

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

def get_abonent_type_keyboard(lang='uz'):
    """Abonent type keyboard"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="👤 Jismoniy shaxs" if lang == 'uz' else "👤 Физическое лицо",
                callback_data="abonent_physical"
            ),
            InlineKeyboardButton(
                text="🏢 Yuridik shaxs" if lang == 'uz' else "🏢 Юридическое лицо",
                callback_data="abonent_legal"
            )
        ]
    ])
    return keyboard

import asyncio
