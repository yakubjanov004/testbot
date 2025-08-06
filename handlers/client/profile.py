"""
Client Profile Handler - Optimized Implementation

This module handles client profile viewing and editing functionality.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from keyboards.client_buttons import get_main_menu_keyboard, get_profile_keyboard, get_back_keyboard
from states.client_states import ProfileStates, MainMenuStates
from utils.role_system import get_role_router
import logging

# Logger setup
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
        'phone_number': '+998901234567',
        'address': 'Toshkent, Chilonzor tumani',
        'email': 'client@example.com',
        'created_at': '2024-01-01'
    }

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    user = await get_user_by_telegram_id(telegram_id)
    return user.get('language', 'uz') if user else 'uz'

async def update_user_profile(user_id: int, field: str, value: str) -> bool:
    """Mock update user profile"""
    return True

def get_client_profile_router():
    """Get client profile router with optimized handlers"""
    router = get_role_router("client")

    @router.message(F.text.in_(["👤 Profil", "👤 Профиль"]))
    async def profile_menu_handler(message: Message, state: FSMContext):
        """Handle profile menu request"""
        try:
            # Get user data
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                logger.error(f"User not found: {message.from_user.id}")
                await message.answer("❌ Foydalanuvchi topilmadi.")
                return
            
            # Get language from state or user data
            state_data = await state.get_data()
            lang = state_data.get('user_lang', user.get('language', 'uz'))
            
            # Prepare profile text
            profile_text = (
                f"👤 <b>Sizning profilingiz</b>\n\n"
                f"📱 <b>Telefon:</b> {user['phone_number']}\n"
                f"👤 <b>To'liq ism:</b> {user['full_name']}\n"
                f"📍 <b>Manzil:</b> {user.get('address', 'Kiritilmagan')}\n"
                f"📧 <b>Email:</b> {user.get('email', 'Kiritilmagan')}\n"
                f"📅 <b>Ro'yxatdan o'tgan:</b> {user.get('created_at', 'N/A')}\n"
                f"🆔 <b>Telegram ID:</b> {user['telegram_id']}"
                if lang == 'uz' else
                f"👤 <b>Ваш профиль</b>\n\n"
                f"📱 <b>Телефон:</b> {user['phone_number']}\n"
                f"👤 <b>Полное имя:</b> {user['full_name']}\n"
                f"📍 <b>Адрес:</b> {user.get('address', 'Не указан')}\n"
                f"📧 <b>Email:</b> {user.get('email', 'Не указан')}\n"
                f"📅 <b>Зарегистрирован:</b> {user.get('created_at', 'N/A')}\n"
                f"🆔 <b>Telegram ID:</b> {user['telegram_id']}"
            )
            
            # Create profile keyboard
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✏️ Ismni tahrirlash" if lang == 'uz' else "✏️ Изменить имя",
                        callback_data="edit_profile_name"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📍 Manzilni tahrirlash" if lang == 'uz' else "📍 Изменить адрес",
                        callback_data="edit_profile_address"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📧 Emailni tahrirlash" if lang == 'uz' else "📧 Изменить email",
                        callback_data="edit_profile_email"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="◀️ Orqaga" if lang == 'uz' else "◀️ Назад",
                        callback_data="back_to_main_menu"
                    )
                ]
            ])
            
            await message.answer(
                text=profile_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
            await state.set_state(ProfileStates.viewing_profile)
            
            logger.info(f"User viewing profile: {user['telegram_id']}")
            
        except Exception as e:
            logger.error(f"Error in profile_menu_handler: {str(e)}", exc_info=True)
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "edit_profile_name", StateFilter(ProfileStates.viewing_profile))
    async def edit_name_handler(callback: CallbackQuery, state: FSMContext):
        """Handle name editing"""
        try:
            await callback.answer()
            
            # Get language from state
            state_data = await state.get_data()
            lang = state_data.get('user_lang', 'uz')
            
            edit_text = (
                "✏️ Yangi ismingizni kiriting:"
                if lang == 'uz' else
                "✏️ Введите новое имя:"
            )
            
            await callback.message.answer(
                text=edit_text,
                reply_markup=get_back_keyboard(lang)
            )
            
            await state.set_state(ProfileStates.editing_name)
            
        except Exception as e:
            logger.error(f"Error in edit_name_handler: {str(e)}", exc_info=True)
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "edit_profile_address", StateFilter(ProfileStates.viewing_profile))
    async def edit_address_handler(callback: CallbackQuery, state: FSMContext):
        """Handle address editing"""
        try:
            await callback.answer()
            
            # Get language from state
            state_data = await state.get_data()
            lang = state_data.get('user_lang', 'uz')
            
            edit_text = (
                "📍 Yangi manzilingizni kiriting:"
                if lang == 'uz' else
                "📍 Введите новый адрес:"
            )
            
            await callback.message.answer(
                text=edit_text,
                reply_markup=get_back_keyboard(lang)
            )
            
            await state.set_state(ProfileStates.editing_address)
            
        except Exception as e:
            logger.error(f"Error in edit_address_handler: {str(e)}", exc_info=True)
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "edit_profile_email", StateFilter(ProfileStates.viewing_profile))
    async def edit_email_handler(callback: CallbackQuery, state: FSMContext):
        """Handle email editing"""
        try:
            await callback.answer()
            
            # Get language from state
            state_data = await state.get_data()
            lang = state_data.get('user_lang', 'uz')
            
            edit_text = (
                "📧 Yangi email manzilingizni kiriting:"
                if lang == 'uz' else
                "📧 Введите новый email адрес:"
            )
            
            await callback.message.answer(
                text=edit_text,
                reply_markup=get_back_keyboard(lang)
            )
            
            await state.set_state(ProfileStates.editing_email)
            
        except Exception as e:
            logger.error(f"Error in edit_email_handler: {str(e)}", exc_info=True)
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.message(StateFilter(ProfileStates.editing_name))
    async def process_name_edit(message: Message, state: FSMContext):
        """Process name editing"""
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
            
            # Validate name
            new_name = message.text.strip()
            if len(new_name) < 3:
                await message.answer("⚠️ Ism kamida 3 ta belgidan iborat bo'lishi kerak!")
                return
            
            # Get user data
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("❌ Xatolik yuz berdi.")
                return
            
            # Update name (mock)
            success = await update_user_profile(user['id'], 'full_name', new_name)
            
            if success:
                # Get language
                state_data = await state.get_data()
                lang = state_data.get('user_lang', 'uz')
                
                success_text = (
                    f"✅ Ismingiz muvaffaqiyatli o'zgartirildi!\n\n"
                    f"Yangi ism: {new_name}"
                    if lang == 'uz' else
                    f"✅ Ваше имя успешно изменено!\n\n"
                    f"Новое имя: {new_name}"
                )
                
                await message.answer(
                    text=success_text,
                    reply_markup=get_main_menu_keyboard(lang)
                )
                
                await state.set_state(MainMenuStates.main_menu)
                
            else:
                await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
                
        except Exception as e:
            logger.error(f"Error in process_name_edit: {str(e)}", exc_info=True)
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(StateFilter(ProfileStates.editing_address))
    async def process_address_edit(message: Message, state: FSMContext):
        """Process address editing"""
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
            
            # Validate address
            new_address = message.text.strip()
            if len(new_address) < 5:
                await message.answer("⚠️ Manzil kamida 5 ta belgidan iborat bo'lishi kerak!")
                return
            
            # Get user data
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("❌ Xatolik yuz berdi.")
                return
            
            # Update address (mock)
            success = await update_user_profile(user['id'], 'address', new_address)
            
            if success:
                # Get language
                state_data = await state.get_data()
                lang = state_data.get('user_lang', 'uz')
                
                success_text = (
                    f"✅ Manzilingiz muvaffaqiyatli o'zgartirildi!\n\n"
                    f"Yangi manzil: {new_address}"
                    if lang == 'uz' else
                    f"✅ Ваш адрес успешно изменен!\n\n"
                    f"Новый адрес: {new_address}"
                )
                
                await message.answer(
                    text=success_text,
                    reply_markup=get_main_menu_keyboard(lang)
                )
                
                await state.set_state(MainMenuStates.main_menu)
                
            else:
                await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
                
        except Exception as e:
            logger.error(f"Error in process_address_edit: {str(e)}", exc_info=True)
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(StateFilter(ProfileStates.editing_email))
    async def process_email_edit(message: Message, state: FSMContext):
        """Process email editing"""
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
            
            # Validate email
            new_email = message.text.strip()
            if '@' not in new_email or '.' not in new_email:
                await message.answer("⚠️ Iltimos, to'g'ri email manzilini kiriting!")
                return
            
            # Get user data
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("❌ Xatolik yuz berdi.")
                return
            
            # Update email (mock)
            success = await update_user_profile(user['id'], 'email', new_email)
            
            if success:
                # Get language
                state_data = await state.get_data()
                lang = state_data.get('user_lang', 'uz')
                
                success_text = (
                    f"✅ Email manzilingiz muvaffaqiyatli o'zgartirildi!\n\n"
                    f"Yangi email: {new_email}"
                    if lang == 'uz' else
                    f"✅ Ваш email успешно изменен!\n\n"
                    f"Новый email: {new_email}"
                )
                
                await message.answer(
                    text=success_text,
                    reply_markup=get_main_menu_keyboard(lang)
                )
                
                await state.set_state(MainMenuStates.main_menu)
                
            else:
                await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
                
        except Exception as e:
            logger.error(f"Error in process_email_edit: {str(e)}", exc_info=True)
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    return router
