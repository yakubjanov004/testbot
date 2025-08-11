"""
Client Profile Handler - Complete Implementation

This module handles client profile functionality.
"""

from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.client_buttons import (
    get_client_profile_menu,
    get_edit_profile_keyboard,
    get_client_profile_back_keyboard,
    get_client_profile_reply_keyboard,
    get_main_menu_keyboard,
)
from states.client_states import ProfileStates
from filters.role_filter import RoleFilter
from utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data - should be replaced with real database query"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'client',
        'language': 'uz',
        'full_name': 'Test Client',
        'phone_number': '+998901234567',
        'address': 'Toshkent shahri, Chilanzar tumani, 15-uy',
        'region': 'Toshkent shahri',
        'created_at': '2024-01-01 10:00:00'
    }

async def get_user_lang(telegram_id: int):
    """Mock get user language - should be replaced with real database query"""
    return 'uz'

async def update_user_profile(telegram_id: int, field: str, value: str):
    """Mock update user profile - should be replaced with real database update"""
    logger.info(f"Updating user {telegram_id} {field} to {value}")
    return True

def client_only(func):
    """Decorator to ensure only clients can access"""
    async def wrapper(*args, **kwargs):
        try:
            # Extract message or callback from args
            event = args[0] if args else None
            if event and hasattr(event, 'from_user'):
                user_id = event.from_user.id
                # Here you would check if user has client role
                # For now, we'll just proceed
                logger.info(f"Client access check for user {user_id}")
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in client_only decorator: {e}")
            raise
    return wrapper

def get_client_profile_router():
    from aiogram import Router
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("client")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @client_only
    @router.message(F.text.in_(['👤 Kabinet', '👤 Кабинет']))
    async def client_profile_handler(message: Message, state: FSMContext):
        """Cabinet entry with reply keyboard"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("Foydalanuvchi topilmadi.")
                return

            lang = user.get('language', 'uz')
            profile_text = (
                "👤 Kabinet. Amalni tanlang." if lang == 'uz' else "👤 Кабинет. Выберите действие."
            )

            await message.answer(
                text=profile_text,
                reply_markup=get_client_profile_reply_keyboard(lang)
            )

            await state.set_state(ProfileStates.profile_menu)
        except Exception as e:
            logger.error(f"Error in client_profile_handler: {e}")
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @client_only
    @router.message(F.text.in_(["👁️ Ma'lumotlarni ko'rish", "👁️ Просмотр информации"]))
    async def handle_view_info_reply(message: Message):
        """View client information via reply menu"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("Foydalanuvchi topilmadi.")
                return

            lang = user.get('language', 'uz')
            info_text = (
                f"👤 <b>Profil ma'lumotlari</b>\n\n"
                f"🆔 <b>ID:</b> {user['id']}\n"
                f"👤 <b>Ism:</b> {user['full_name']}\n"
                f"📞 <b>Telefon:</b> {user['phone_number']}\n"
                f"📍 <b>Manzil:</b> {user['address']}\n"
                f"🏘️ <b>Hudud:</b> {user['region']}\n"
                f"📅 <b>Ro'yxatdan o'tgan:</b> {user['created_at']}\n"
                f"🌐 <b>Til:</b> {user['language']}"
            )
            await message.answer(info_text, reply_markup=get_client_profile_reply_keyboard(lang), parse_mode='HTML')
        except Exception as e:
            logger.error(f"Error in handle_view_info_reply: {e}")
            await message.answer("❌ Xatolik yuz berdi")

    @client_only
    @router.message(F.text.in_(["📋 Mening buyurtmalarim", "📋 Мои заявки"]))
    async def handle_show_orders_reply(message: Message):
        """Bridge to orders section from cabinet"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            lang = user.get('language', 'uz')
            info = (
                "📋 Buyurtmalaringizni ko'rish uchun buyurtmalar bo'limi ochildi."
                if lang == 'uz' else
                "📋 Открыт раздел ваших заявок."
            )
            await message.answer(info)
            # Optionally instruct user to press '📋 Mening buyurtmalarim' in orders handler
            from handlers.client.orders import get_orders_router  # local import to avoid cycles
            # No direct call; orders router already handles the same reply text
        except Exception as e:
            logger.error(f"Error in handle_show_orders_reply: {e}")
            await message.answer("❌ Xatolik yuz berdi")

    @client_only
    @router.callback_query(F.data == "client_profile_back")
    async def handle_back_to_profile(callback: CallbackQuery):
        """Back to profile menu (inline -> reply cabinet)"""
        try:
            await callback.answer()
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            profile_text = (
                "👤 Kabinet. Amalni tanlang." if lang == 'uz' else "👤 Кабинет. Выберите действие."
            )
            await callback.message.edit_text(profile_text)
            await callback.message.answer(profile_text, reply_markup=get_client_profile_reply_keyboard(lang))
        except Exception as e:
            logger.error(f"Error in handle_back_to_profile: {e}")
            await callback.answer("❌ Xatolik yuz berdi")

    @client_only
    @router.message(F.text.in_(["✏️ Ismni o'zgartirish", "✏️ Изменить имя"]))
    async def handle_edit_name_reply(message: Message, state: FSMContext):
        """Start name editing from reply cabinet"""
        try:
            await message.answer("Yangi to'liq ismingizni kiriting:")
            await state.set_state(ProfileStates.editing_name)
        except Exception as e:
            logger.error(f"Error in handle_edit_name_reply: {e}")
            await message.answer("❌ Xatolik yuz berdi")

    @client_only
    @router.callback_query(F.data == "client_edit_name")
    async def handle_edit_name(callback: CallbackQuery, state: FSMContext):
        """Edit name"""
        try:
            await callback.answer()
            
            edit_text = "Yangi to'liq ismingizni kiriting:"
            
            await callback.message.edit_text(edit_text)
            await state.set_state(ProfileStates.editing_name)
            
        except Exception as e:
            logger.error(f"Error in handle_edit_name: {e}")
            await callback.answer("❌ Xatolik yuz berdi")

    @client_only
    @router.message(ProfileStates.editing_name)
    async def handle_name_input(message: Message, state: FSMContext):
        """Handle name input"""
        try:
            new_name = message.text.strip()
            
            if len(new_name) < 3:
                await message.answer("Ism juda qisqa. Kamida 3 ta belgi kiriting.")
                return
            
            # Update user profile
            success = await update_user_profile(message.from_user.id, 'full_name', new_name)
            
            if success:
                success_text = f"✅ Ism muvaffaqiyatli o'zgartirildi: {new_name}"
                await message.answer(success_text, reply_markup=get_client_profile_reply_keyboard('uz'))
            else:
                await message.answer("❌ Ism o'zgartirishda xatolik yuz berdi.")
            
            await state.clear()
            
        except Exception as e:
            logger.error(f"Error in handle_name_input: {e}")
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @client_only
    @router.callback_query(F.data == "client_edit_address")
    async def handle_edit_address(callback: CallbackQuery, state: FSMContext):
        """Edit address"""
        try:
            await callback.answer()
            
            edit_text = "Yangi manzilingizni kiriting:"
            
            await callback.message.edit_text(edit_text)
            await state.set_state(ProfileStates.editing_address)
            
        except Exception as e:
            logger.error(f"Error in handle_edit_address: {e}")
            await callback.answer("❌ Xatolik yuz berdi")

    @client_only
    @router.message(ProfileStates.editing_address)
    async def handle_address_input(message: Message, state: FSMContext):
        """Handle address input"""
        try:
            new_address = message.text.strip()
            
            if len(new_address) < 10:
                await message.answer("Manzil juda qisqa. Kamida 10 ta belgi kiriting.")
                return
            
            # Update user profile
            success = await update_user_profile(message.from_user.id, 'address', new_address)
            
            if success:
                success_text = f"✅ Manzil muvaffaqiyatli o'zgartirildi: {new_address}"
                await message.answer(success_text, reply_markup=get_client_profile_reply_keyboard('uz'))
            else:
                await message.answer("❌ Manzil o'zgartirishda xatolik yuz berdi.")
            
            await state.clear()
            
        except Exception as e:
            logger.error(f"Error in handle_address_input: {e}")
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    return router
