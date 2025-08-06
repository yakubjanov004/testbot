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

async def send_and_track(message: Message, text: str, reply_markup=None):
    """Mock send and track"""
    return await message.answer(text, reply_markup=reply_markup)

async def edit_and_track(message, text: str, reply_markup=None):
    """Mock edit and track"""
    return await message.edit_text(text, reply_markup=reply_markup)

async def answer_and_cleanup(callback: CallbackQuery, text: str = None):
    """Mock answer and cleanup"""
    await callback.answer(text)

def get_client_feedback_router():
    router = get_role_router("client")

    @router.message(F.text.in_(["📝 Fikr-mulohaza", "📝 Обратная связь"]))
    async def client_feedback_handler(message: Message, state: FSMContext):
        """Client feedback handler with enhanced workflow tracking"""
        try:
            # Rate limiting check
            if not await rate_limiter.check_rate_limit(f"client_feedback_{message.from_user.id}", 5, 60):
                await message.answer("Iltimos, biroz kutib turing.")
                return
            
            # Start enhanced time tracking for feedback access
            await time_tracker.start_role_tracking(
                request_id=f"client_feedback_{message.from_user.id}",
                user_id=message.from_user.id,
                role='client',
                workflow_stage="feedback_accessed"
            )
            
            # Track workflow transition for feedback access
            await workflow_manager.track_workflow_transition(
                request_id=f"client_feedback_{message.from_user.id}",
                from_role="main_menu",
                to_role="feedback",
                user_id=message.from_user.id,
                notes='Client accessing feedback section'
            )
            
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
            
            # Use send_and_track for inline cleanup
            sent_message = await send_and_track(
                message=message,
                text=feedback_text,
                reply_markup=get_feedback_keyboard(lang)
            )
            
            await state.set_state(FeedbackStates.waiting_for_feedback)
            
            # Track application handling
            await application_tracker.track_application_handling(
                application_id=f"client_feedback_{message.from_user.id}",
                handler_id=message.from_user.id,
                action="feedback_accessed"
            )
            
            # Update enhanced statistics
            await statistics_manager.generate_role_based_statistics('client', 'daily')
            
            # Log feedback access
            await audit_logger.log_user_action(
                user_id=message.from_user.id,
                action="feedback_accessed",
                details={"language": lang}
            )
            
            # End enhanced time tracking
            await time_tracker.end_role_tracking(
                request_id=f"client_feedback_{message.from_user.id}",
                user_id=message.from_user.id,
                notes="Feedback access completed successfully"
            )
            
        except Exception as e:
            await audit_logger.log_system_event(
                event_type="client_feedback_handler_error",
                description=f"Error in client_feedback_handler: {str(e)}",
                severity="error"
            )
            await message.answer("Xatolik yuz berdi")

    @router.message(StateFilter(FeedbackStates.waiting_for_feedback))
    async def process_feedback(message: Message, state: FSMContext):
        """Process feedback message"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("Foydalanuvchi topilmadi.")
                return
            
            lang = user.get('language', 'uz')
            feedback_text = message.text.strip()
            
            if len(feedback_text) < 10:
                error_text = (
                    "Fikr-mulohaza juda qisqa. Kamida 10 ta belgi kiriting."
                    if lang == 'uz' else
                    "Обратная связь слишком короткая. Введите минимум 10 символов."
                )
                await message.answer(error_text)
                return
            
            # Track feedback submission
            await application_tracker.track_application_handling(
                application_id=f"client_feedback_{message.from_user.id}",
                handler_id=message.from_user.id,
                action="feedback_submitted"
            )
            
            # Log feedback submission
            await audit_logger.log_user_action(
                user_id=message.from_user.id,
                action="feedback_submitted",
                details={"feedback_length": len(feedback_text), "language": lang}
            )
            
            success_text = (
                "✅ Fikr-mulohazangiz qabul qilindi!\n\n"
                "Rahmat, fikr-mulohazangiz uchun."
            ) if lang == 'uz' else (
                "✅ Ваша обратная связь принята!\n\n"
                "Спасибо за вашу обратную связь."
            )
            
            await message.answer(success_text)
            await state.clear()
            
        except Exception as e:
            await audit_logger.log_system_event(
                event_type="process_feedback_error",
                description=f"Error in process_feedback: {str(e)}",
                severity="error"
            )
            lang = await get_user_lang(message.from_user.id)
            error_text = "Xatolik yuz berdi" if lang == 'uz' else "Произошла ошибка"
            await message.answer(error_text)

    return router
