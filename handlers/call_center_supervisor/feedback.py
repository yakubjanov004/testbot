"""
Call Center Supervisor Feedback Handler - Simplified Implementation

This module implements feedback functionality for Call Center Supervisor role.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from states.call_center_supervisor_states import CallCenterSupervisorFeedbackStates

def get_call_center_supervisor_feedback_router():
    """Get router for call center supervisor feedback handlers - Simplified Implementation"""
    router = Router()

    @router.message(F.text.in_(["⭐️ Fikr-mulohaza", "⭐️ Обратная связь"]))
    async def call_center_supervisor_feedback(message: Message, state: FSMContext):
        """Call center supervisor feedback menu"""
        try:
            text = """
⭐️ Fikr-mulohaza bo'limi

Bu yerda siz:
• Tizim haqida fikr bildirishingiz
• Xodimlar ishlari haqida baholash berishingiz
• Taklif va shikoyatlar yuborishingiz mumkin

Quyidagi variantlardan birini tanlang:
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📝 Fikr yozish", callback_data="ccs_write_feedback")],
                [InlineKeyboardButton(text="📊 Fikrlarni ko'rish", callback_data="ccs_view_feedback")],
                [InlineKeyboardButton(text="⭐ Xizmatni baholash", callback_data="ccs_rate_service")]
            ])
            
            await message.answer(text, reply_markup=keyboard)
            await state.set_state(CallCenterSupervisorFeedbackStates.feedback)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.startswith("ccs_"))
    async def handle_feedback_callbacks(callback: CallbackQuery, state: FSMContext):
        """Handle feedback callback queries"""
        try:
            data = callback.data
            
            if data == "ccs_write_feedback":
                await _handle_write_feedback(callback, state)
            elif data == "ccs_view_feedback":
                await _handle_view_feedback(callback, state)
            elif data == "ccs_rate_service":
                await _handle_rate_service(callback, state)
            elif data.startswith("ccs_rate_"):
                rating = int(data.split("_")[-1])
                await _handle_rating_selection(callback, state, rating)
            elif data == "ccs_cancel_rating":
                await callback.message.edit_text(
                    "❌ Baholash bekor qilindi.",
                    reply_markup=get_feedback_keyboard()
                )
                await callback.answer()
            else:
                await callback.answer("❌ Noma'lum buyruq", show_alert=True)
                
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.message(CallCenterSupervisorFeedbackStates.writing_feedback)
    async def handle_feedback_text(message: Message, state: FSMContext):
        """Handle feedback text input"""
        try:
            feedback_text = message.text.strip()
            
            if len(feedback_text) < 10:
                await message.answer("❌ Fikr-mulohaza juda qisqa. Kamida 10 ta belgi kiriting.")
                return
            
            # Mock feedback submission
            text = f"""
✅ Fikr-mulohazangiz qabul qilindi!

📝 Matn: {feedback_text[:100]}{'...' if len(feedback_text) > 100 else ''}

Rahmat! Sizning fikringiz biz uchun muhim.
            """
            
            await message.answer(text)
            await state.clear()
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    return router


async def _handle_write_feedback(callback: CallbackQuery, state: FSMContext):
    """Handle write feedback action"""
    try:
        text = """
📝 Fikr-mulohaza yozish

Tizim ishlashi, xodimlar faoliyati yoki boshqa masalalar haqida 
o'z fikringizni yozing.

Fikr-mulohazangizni kiriting:
        """
        
        await callback.message.edit_text(text)
        await state.set_state(CallCenterSupervisorFeedbackStates.writing_feedback)
        await callback.answer()
        
    except Exception as e:
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


async def _handle_view_feedback(callback: CallbackQuery, state: FSMContext):
    """Handle view feedback action"""
    try:
        # Mock feedback data
        text = """
📊 Fikr-mulohazalar ko'rish

📈 OXIRGI BAHOLASHLAR:
• O'rtacha baho: 4.2/5 ⭐⭐⭐⭐
• Jami baholashlar: 15
• Ijobiy fikrlar: 12 (80%)
• Taklif va shikoyatlar: 3

🔝 ENG KO'P TILGA OLINGAN:
• Tizim tezligi: 85% ijobiy
• Xodimlar xizmati: 90% ijobiy
• Interfeys qulayligi: 75% ijobiy

📝 OXIRGI FIKRLAR:
• "Tizim juda qulay, rahmat!"
• "Xodimlar tez javob berishadi"
• "Ba'zi funksiyalar sekinroq ishlaydi"

Batafsil hisobot uchun admin bilan bog'laning.
        """
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📝 Fikr yozish", callback_data="ccs_write_feedback")],
            [InlineKeyboardButton(text="⭐ Xizmatni baholash", callback_data="ccs_rate_service")]
        ])
        
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()
        
    except Exception as e:
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


async def _handle_rate_service(callback: CallbackQuery, state: FSMContext):
    """Handle rate service action"""
    try:
        text = """
⭐ Xizmat sifatini baholash

Tizim va xodimlar ishini qanday baholaysiz?

1 - juda yomon, 5 - a'lo
        """
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="⭐", callback_data="ccs_rate_1"),
                InlineKeyboardButton(text="⭐⭐", callback_data="ccs_rate_2"),
                InlineKeyboardButton(text="⭐⭐⭐", callback_data="ccs_rate_3"),
                InlineKeyboardButton(text="⭐⭐⭐⭐", callback_data="ccs_rate_4"),
                InlineKeyboardButton(text="⭐⭐⭐⭐⭐", callback_data="ccs_rate_5")
            ],
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="ccs_cancel_rating")]
        ])
        
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()
        
    except Exception as e:
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


async def _handle_rating_selection(callback: CallbackQuery, state: FSMContext, rating: int):
    """Handle rating selection"""
    try:
        # Mock rating submission
        stars = "⭐" * rating
        text = f"""
✅ Baholash qabul qilindi!

Sizning bahongiz: {stars} ({rating}/5)

Rahmat! Sizning bahongiz biz uchun muhim.
        """
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📝 Fikr yozish", callback_data="ccs_write_feedback")],
            [InlineKeyboardButton(text="📊 Fikrlarni ko'rish", callback_data="ccs_view_feedback")]
        ])
        
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()
        
    except Exception as e:
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


def get_feedback_keyboard():
    """Get feedback keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Fikr yozish", callback_data="ccs_write_feedback")],
        [InlineKeyboardButton(text="📊 Fikrlarni ko'rish", callback_data="ccs_view_feedback")],
        [InlineKeyboardButton(text="⭐ Xizmatni baholash", callback_data="ccs_rate_service")]
    ])