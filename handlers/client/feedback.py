"""
Client Feedback Handler - Simplified Implementation

This module handles client feedback functionality.
"""

from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.client_states import FeedbackStates
from filters.role_filter import RoleFilter

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

async def get_user_role(user_id: int) -> str:
    """Mock get user role"""
    return 'client'

def get_client_feedback_router():
    """Get client feedback router with role filtering"""
    from aiogram import Router
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("client")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["💬 Fikr bildirish", "💬 Оставить отзыв"]))
    async def feedback_handler(message: Message, state: FSMContext):
        """Handle feedback request"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            lang = user.get('language', 'uz')
            
            feedback_text = (
                "💬 <b>Fikr bildirish</b>\n\n"
                "Sizning fikringiz biz uchun muhim! Iltimos, xizmatimiz haqida fikr bildiring.\n\n"
                "📝 Fikr yozish uchun quyidagi formatda yozing:\n"
                "• Xizmat sifatini baholang (1-5 yulduz)\n"
                "• Izoh qoldiring\n"
                "• Takliflar bo'lsa yozing\n\n"
                "Masalan:\n"
                "⭐⭐⭐⭐⭐\n"
                "Ajoyib xizmat! Tez va sifatli ishlar. Rahmat!"
                if lang == 'uz' else
                "💬 <b>Оставить отзыв</b>\n\n"
                "Ваше мнение важно для нас! Пожалуйста, оставьте отзыв о наших услугах.\n\n"
                "📝 Для написания отзыва используйте следующий формат:\n"
                "• Оцените качество услуги (1-5 звезд)\n"
                "• Оставьте комментарий\n"
                "• Напишите предложения, если есть\n\n"
                "Например:\n"
                "⭐⭐⭐⭐⭐\n"
                "Отличный сервис! Быстрая и качественная работа. Спасибо!"
            )
            
            from keyboards.client_buttons import get_cancel_keyboard
            keyboard = get_cancel_keyboard(lang)
            
            await message.answer(feedback_text, reply_markup=keyboard, parse_mode='HTML')
            await state.set_state(FeedbackStates.waiting_for_feedback)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(FeedbackStates.waiting_for_feedback)
    async def process_feedback(message: Message, state: FSMContext):
        """Process user feedback"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            lang = user.get('language', 'uz')
            
            feedback_text = message.text
            
            # Save feedback (mock)
            feedback_data = {
                'user_id': user['id'],
                'feedback': feedback_text,
                'timestamp': '2024-01-15 10:30:00'
            }
            
            success_text = (
                "✅ <b>Fikringiz qabul qilindi!</b>\n\n"
                "Rahmat, fikringiz biz uchun muhim. Sizning takliflaringiz xizmatimizni yaxshilashga yordam beradi.\n\n"
                "📞 Qo'shimcha savollaringiz bo'lsa, biz bilan bog'laning:\n"
                "• Telefon: +998 71 123 45 67\n"
                "• Telegram: @alfaconnect_support"
                if lang == 'uz' else
                "✅ <b>Ваш отзыв принят!</b>\n\n"
                "Спасибо, ваше мнение важно для нас. Ваши предложения помогают улучшить наш сервис.\n\n"
                "📞 Если у вас есть дополнительные вопросы, свяжитесь с нами:\n"
                "• Телефон: +998 71 123 45 67\n"
                "• Telegram: @alfaconnect_support"
            )
            
            from keyboards.client_buttons import get_back_keyboard
            keyboard = get_back_keyboard(lang)
            
            await message.answer(success_text, reply_markup=keyboard, parse_mode='HTML')
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
                "❌ Fikr bildirish bekor qilindi."
                if lang == 'uz' else
                "❌ Отзыв отменен."
            )
            
            from keyboards.client_buttons import get_back_keyboard
            keyboard = get_back_keyboard(lang)
            
            await callback.message.edit_text(cancel_text, reply_markup=keyboard)
            await state.clear()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router
