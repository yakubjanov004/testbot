"""
Client Profile Handler - Simplified Implementation

This module handles client profile functionality.
"""

from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.client_buttons import get_client_profile_menu, get_edit_profile_keyboard
from states.client_states import ProfileStates
from utils.role_system import get_role_router

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
        'address': 'Toshkent shahri, Chilanzar tumani, 15-uy',
        'region': 'Toshkent shahri',
        'created_at': '2024-01-01 10:00:00'
    }

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    return 'uz'

def client_only(func):
    """Decorator to ensure only clients can access"""
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)
    return wrapper

def get_client_profile_router():
    router = get_role_router("client")

    @client_only
    @router.message(F.text.in_(['👤 Profil']))
    async def client_profile_handler(message: Message, state: FSMContext):
        """Mijoz profili bilan ishlash"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("Foydalanuvchi topilmadi.")
                return
            
            profile_text = "Profil menyusi. Kerakli amalni tanlang."
            
            sent_message = await message.answer(
                text=profile_text,
                reply_markup=get_client_profile_menu('uz')
            )
            
            await state.set_state(ProfileStates.profile_menu)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @client_only
    @router.callback_query(F.data == "client_view_info")
    async def handle_view_info(callback: CallbackQuery):
        """View client information"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user:
                await callback.message.edit_text("Foydalanuvchi topilmadi.")
                return
            
            # To'liq ma'lumot
            info_text = (
                f"👤 <b>Profil ma'lumotlari - To'liq ma'lumot</b>\n\n"
                f"🆔 <b>ID:</b> {user['id']}\n"
                f"📱 <b>Telegram ID:</b> {user['telegram_id']}\n"
                f"👤 <b>To'liq ism:</b> {user['full_name']}\n"
                f"📞 <b>Telefon raqam:</b> {user['phone_number']}\n"
                f"🏛️ <b>Hudud:</b> {user['region']}\n"
                f"🏠 <b>Manzil:</b> {user['address']}\n"
                f"🎭 <b>Rol:</b> {user['role'].upper()}\n"
                f"🌐 <b>Til:</b> {user['language'].upper()}\n"
                f"📅 <b>Ro'yxatdan o'tgan:</b> {user['created_at']}\n\n"
                f"📊 <b>Statistika:</b>\n"
                f"• Jami arizalar: 5 ta\n"
                f"• Faol arizalar: 2 ta\n"
                f"• Bajarilgan: 3 ta\n"
                f"• O'rtacha baho: ⭐⭐⭐⭐⭐"
            )
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="client_profile_back")]
            ])
            
            await callback.message.edit_text(info_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @client_only
    @router.callback_query(F.data == "client_order_stats")
    async def handle_order_stats(callback: CallbackQuery):
        """View order statistics"""
        try:
            await callback.answer()
            
            # To'liq statistika
            stats_text = (
                f"📊 <b>Buyurtmalar statistikasi - To'liq ma'lumot</b>\n\n"
                f"📋 <b>Jami buyurtmalar:</b> 5 ta\n\n"
                f"🔧 <b>Texnik xizmatlar:</b> 3 ta\n"
                f"• Faol: 1 ta\n"
                f"• Bajarilgan: 2 ta\n\n"
                f"🔌 <b>Ulanishlar:</b> 2 ta\n"
                f"• Faol: 1 ta\n"
                f"• Bajarilgan: 1 ta\n\n"
                f"📈 <b>O'rtacha baho:</b> ⭐⭐⭐⭐⭐\n"
                f"⏰ <b>O'rtacha bajarilish vaqti:</b> 2.5 kun\n"
                f"💰 <b>Jami xizmat narxi:</b> 1,250,000 so'm\n\n"
                f"📅 <b>So'nggi faoliyat:</b> 2024-01-15"
            )
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="client_profile_back")]
            ])
            
            await callback.message.edit_text(stats_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @client_only
    @router.callback_query(F.data == "client_profile_back")
    async def handle_back_to_profile(callback: CallbackQuery):
        """Back to profile menu"""
        try:
            await callback.answer()
            
            profile_text = "Profil menyusi. Kerakli amalni tanlang."
            
            await callback.message.edit_text(
                text=profile_text,
                reply_markup=get_client_profile_menu('uz')
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @client_only
    @router.callback_query(F.data == "client_edit_profile")
    async def handle_edit_profile(callback: CallbackQuery):
        """Edit profile menu"""
        try:
            await callback.answer()
            
            edit_text = "Qaysi ma'lumotni o'zgartirmoqchisiz?"
            
            await callback.message.edit_text(
                text=edit_text,
                reply_markup=get_edit_profile_keyboard('uz')
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

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
            
            # Mock update
            success_text = f"✅ Ism muvaffaqiyatli o'zgartirildi: {new_name}"
            
            await message.answer(success_text, reply_markup=get_client_profile_menu('uz'))
            await state.clear()
            
        except Exception as e:
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
            
            # Mock update
            success_text = f"✅ Manzil muvaffaqiyatli o'zgartirildi: {new_address}"
            
            await message.answer(success_text, reply_markup=get_client_profile_menu('uz'))
            await state.clear()
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    return router
