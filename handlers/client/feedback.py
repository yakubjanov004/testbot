"""
Client Feedback Handler - Simplified Implementation

This module handles client feedback functionality.
"""

from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from keyboards.client_buttons import get_feedback_keyboard, get_main_menu_keyboard
from states.client_states import FeedbackStates
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
        'phone_number': '+998901234567'
    }

async def get_user_lang(user_id: int) -> str:
    """Mock get user language"""
    return 'uz'

def get_client_feedback_router():
    router = get_role_router("client")

    @router.message(F.text.in_(["📝 Fikr-mulohaza", "📝 Обратная связь"]))
    async def client_feedback_handler(message: Message, state: FSMContext):
        """Client feedback handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("Foydalanuvchi topilmadi.")
                return
            
            lang = user.get('language', 'uz')
            feedback_text = (
                "Fikr-mulohaza yuborish uchun matnni kiriting:"
                if lang == 'uz' else
                "Введите текст для отправки обратной связи:"
            )
            
            sent_message = await message.answer(
                text=feedback_text,
                reply_markup=get_feedback_keyboard(lang)
            )
            
            await state.set_state(FeedbackStates.waiting_for_feedback)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(StateFilter(FeedbackStates.waiting_for_feedback))
    async def process_feedback(message: Message, state: FSMContext):
        """Process feedback message"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            lang = user.get('language', 'uz')
            
            # Save feedback (mock)
            feedback_text = message.text
            user_name = message.from_user.full_name or message.from_user.first_name
            
            success_text = (
                f"✅ Fikr-mulohaza muvaffaqiyatli yuborildi!\n\n"
                f"📝 Sizning fikringiz: {feedback_text[:100]}{'...' if len(feedback_text) > 100 else ''}\n\n"
                f"Rahmat, {user_name}! Sizning fikringiz biz uchun muhim."
                if lang == 'uz' else
                f"✅ Обратная связь успешно отправлена!\n\n"
                f"📝 Ваш отзыв: {feedback_text[:100]}{'...' if len(feedback_text) > 100 else ''}\n\n"
                f"Спасибо, {user_name}! Ваше мнение важно для нас."
            )
            
            await message.answer(success_text, reply_markup=get_main_menu_keyboard(lang))
            await state.clear()
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "cancel_feedback")
    async def cancel_feedback(callback: CallbackQuery, state: FSMContext):
        """Cancel feedback"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            cancel_text = (
                "❌ Fikr-mulohaza bekor qilindi."
                if lang == 'uz' else
                "❌ Обратная связь отменена."
            )
            
            await callback.message.edit_text(
                text=cancel_text,
                reply_markup=get_main_menu_keyboard(lang)
            )
            
            await state.clear()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    return router
